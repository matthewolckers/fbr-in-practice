---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.8.0
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# HodgeRank

Testing and exploring the HodgeRank method. Initial code source from [ctralie](https://github.com/ctralie/WiMIR2019_HodgeRanking/).

```python
from Hodge import *
```

```python
import networkx as nx
```

Load file of preferences

```python
def test_HodgeRank(x):
    '''
    x: string representing the filename of
    '''
    R = np.loadtxt("example/" + x + ".txt")
    Z = R.copy()
    [R, Y] = [R[:, 0:2], R[:, 2]]
    print(Y)
    W = np.ones(len(Y))
    (s, I, H) = doHodge(R, W, Y)
    print("scores are: " + str(s))
    print("I vector is:" + str(I))
    print("H vector is:" + str(H))
    getConsistencyRatios(Y, I, H, W, verbose=True)
    # When drawing the graph, you cannot use negative weights so I need to swop i and j
    # when the weight happens to be negative. This is connected to a broader problem
    # in the HodgeRank algorithm which requires the i j to all be in the same order.
    print(Z)
    if len(Z[Z<0])>0:
        Z[Z[:,2]<0] = Z[Z[:,2]<0,[1, 0, 2]]
        Z[Z<0] = Z[Z<0]*-1
    G = nx.from_edgelist(Z.astype(int).tolist(), create_using=nx.MultiDiGraph)
    plt.figure(figsize=(3, 3))
    nx.draw(G, with_labels=True, pos=nx.spring_layout(G), node_size=600)
```

## Test HodgeRank


The algorithm requires that the nodes always be ordered with the lower number first.

```python
test_HodgeRank("ex1")
```

Note that there is a problem in the code of subtracting close to one or zero. The global inconsistency should be zero.

```python
test_HodgeRank("ex2")
```

```python
test_HodgeRank("ex3")
```

```python
test_HodgeRank("ex4")
```
