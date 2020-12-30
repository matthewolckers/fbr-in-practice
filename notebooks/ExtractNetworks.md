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

```python
# Import packages
import numpy as np
import scipy as sp
import networkx as nx
import pandas as pd
import datetime
import pickle

# To import Matlab matrices
import scipy.io

# Plotting
import matplotlib.pyplot as plt
import seaborn as sns
```

```python
datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

Fields are:
- index
- problem_village
- graph
- key
- chosen
- guess_rank
- true_rank
- dontknow
- consumption

```python
# Extract directly from Matlab files
def IndonesiaData():
    '''
    Over 600 villages in Indonesia from Alatas Banerjee Chandrasekhar Hanna and Olken 2016 AER
    
    Return a dictionary of networks.
    '''
    result = {}
    dataset_matlab = scipy.io.loadmat('../data/119802-V1/Network Data/Network Data/finalData')
    for i in range(0,633):
        village = str(dataset_matlab['finalData']['index'][0][0][0][i])
        graph = nx.from_numpy_matrix(dataset_matlab['finalData']['graph'][i][0])
        hhid = [item for sublist in dataset_matlab['finalData']['key'][i][0].tolist() for item in sublist]
        mapping = dict(zip(graph, hhid))
        graph = nx.relabel_nodes(graph, mapping)
        num_chosen = len(dataset_matlab['finalData']['chosen'][i][0])
        chosen = [dataset_matlab['finalData']['chosen'][i][0][x][0] for x in range(num_chosen)]
        guess_rank = {}
        true_rank = {}
        for k in range(num_chosen):
            r_guess = dataset_matlab['finalData']['guess_rank'][i][0][k].tolist()
            r_true = dataset_matlab['finalData']['true_rank'][i][0][k].tolist()
            guess_rank[chosen[k]] = dict(zip(chosen, r_guess))
            true_rank[chosen[k]] = dict(zip(chosen, r_true))
        consum_list = dataset_matlab['finalData']['consumption'][i][0].tolist()
        consum_dict = {}
        for y in consum_list:
            consum_dict[int(y[0])] = y[1]
        result["hamlet_"+str(village)] = {"graph":graph,
                                          "chosen":chosen,
                                          "guess_rank":guess_rank,
                                          "true_rank":true_rank,
                                          "consumption":consum_dict}
    return result
```

```python
data_dict = IndonesiaData()
```

Plot some of the networks

```python
x = 0
for key in data_dict.keys():
    if x <= 50:
        try:
            graph = data_dict[key]["graph"]
            graph.remove_nodes_from(list(nx.isolates(graph)))
            chosen = data_dict[key]["chosen"]
            pos_g = nx.circular_layout(graph)
            plt.figure(figsize=(10,5))
            nx.draw(graph, with_labels=True, pos=pos_g)
            nx.draw_networkx_nodes(graph,pos=pos_g,
                                   nodelist=chosen, node_color='r',node_size=400)
            plt.show()
        except:
            print(key)
            continue
        x+= 1
```

Export the data as a pickle file

```python
with open('../data/data_dict.pickle', 'wb') as handle:
    pickle.dump(data_dict, handle)
```
