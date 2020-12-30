# Source: https://github.com/ctralie/WiMIR2019_HodgeRanking

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
import scipy
from scipy import sparse
from scipy.sparse.linalg import lsqr, cg, eigsh
import time
from CliqueAlgorithms import *


def makeDelta0(R):
    """
    Return the delta0 coboundary matrix
    :param R: NEdges x 2 matrix specifying edges, where orientation
    is taken from the first column to the second column
    R specifies the "natural orientation" of the edges, with the
    understanding that the ranking will be specified later
    It is assumed that there is at least one edge incident
    on every vertex
    """
    NVertices = int(np.max(R)) + 1
    NEdges = R.shape[0]

    #Two entries per edge
    I = np.zeros((NEdges, 2))
    I[:, 0] = np.arange(NEdges)
    I[:, 1] = np.arange(NEdges)
    I = I.flatten()

    J = R[:, 0:2].flatten()

    V = np.zeros((NEdges, 2))
    V[:, 0] = -1
    V[:, 1] = 1
    V = V.flatten()

    Delta = sparse.coo_matrix((V, (I, J)), shape=(NEdges, NVertices)).tocsr()
    return Delta


def makeDelta1(R, verbose):
    """Make the delta1 coboundary matrix
    :param R: Edge list NEdges x 2. It is assumed that
    there is at least one edge incident on every vertex
    """
    NEdges = R.shape[0]
    NVertices = int(np.max(R))+1
    #Make a list of edges for fast lookup
    Edges = []
    for i in range(NVertices):
        Edges.append({})
    for i in range(R.shape[0]):
        [a, b] = [int(R[i, 0]), int(R[i, 1])]
        Edges[a][b] = i
        Edges[b][a] = i

    tic = time.time()
    (I, J, V) = get3CliquesBrute(Edges)
    toc = time.time()
    if verbose:
        print("Elapsed time 3 cliques brute: %g"%(toc - tic))
    [I, J, V] = [a.flatten() for a in [I, J, V]]
    TriNum = int(len(I)/3)
    Delta1 = sparse.coo_matrix((V, (I, J)), shape = (TriNum, NEdges)).tocsr()

    return Delta1


def doHodge(R, W, Y, verbose = False):
    """
    Given
    :param R: NEdges x 2 matrix specfiying comparisons that have been made
    :param W: A flat array of NEdges weights parallel to the rows of R
    :param Y: A flat array of NEdges specifying preferences
    :returns: (s, I, H): s is scalar function, I is local inconsistency vector,
        H is global inconsistency vector
    """
    #Step 1: Get s
    if verbose:
        print("Making Delta0...")
    tic = time.time()
    D0 = makeDelta0(R)
    toc = time.time()
    if verbose:
        print("Elapsed Time: %g seconds"%(toc-tic))
    wSqrt = np.sqrt(W).flatten()
    WSqrt = scipy.sparse.spdiags(wSqrt, 0, len(W), len(W))
    WSqrtRecip = scipy.sparse.spdiags(1/wSqrt, 0, len(W), len(W))
    A = WSqrt*D0
    b = WSqrt.dot(Y)
    s = lsqr(A, b)[0]

    #Step 2: Get local inconsistencies
    if verbose:
        print("Making Delta1...")
    tic = time.time()
    D1 = makeDelta1(R, verbose)
    toc = time.time()
    if verbose:
        print("Elapsed Time: %g seconds"%(toc-tic))
    B = WSqrtRecip*D1.T
    resid = Y - D0.dot(s)  #This has been verified to be orthogonal under <resid, D0*s>_W

    u = wSqrt*resid
    if verbose:
        print("Solving for Phi...")
    tic = time.time()
    Phi = lsqr(B, u)[0]
    toc = time.time()
    if verbose:
        print("Elapsed Time: %g seconds"%(toc-tic))
    I = WSqrtRecip.dot(B.dot(Phi)) #Delta1* dot Phi, since Delta1* = (1/W) Delta1^T

    #Step 3: Get harmonic cocycle
    H = resid - I
    return (s, I, H)

def getWNorm(X, W):
    return np.sqrt(np.sum(W*X*X))

def getConsistencyRatios(Y, I, H, W, verbose=False):
    normD0s = getWNorm(Y-H-I, W)

    [normY, normI, normH] = [getWNorm(Y, W), getWNorm(I, W), getWNorm(H, W)]
    a = (normD0s/normY)**2
    b = (normI/normY)**2
    c = (normH/normY)**2
    if verbose:
        print("|D0s/Y| = %g"%a)
        print("Local Inconsistency = %g"%b)
        print("Global Inconsistency = %g"%c)
        print("a + b + c = %g"%(a + b + c))
    return (a, b, c)
