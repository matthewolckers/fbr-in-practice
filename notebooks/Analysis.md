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
import pickle

# Plotting
import matplotlib.pyplot as plt
import seaborn as sns

# HodgeRank
from Hodge import *
```

Set the random seed so results can replicate. I used [random.org](https://www.random.org/integers/?num=1&min=0&max=1000000000&col=1&base=10&format=html&rnd=new) to generate the seed.

```python
seed = 833913377
```

## Load data

```python
# Load networks
infile = open("../data/data_dict.pickle",'rb')
data_dict = pickle.load(infile)
infile.close()
```

```python
# Load self-assessment data
df_SA = pd.read_csv("../data/self_assessed_wealth.csv")
```

```python
# Poverty rankings determined at community meetings
df_CBT = pd.read_csv("../data/community_meeting.csv")
```

## Friend-Based Ranking vs Community-Based Targeting


Steps:
1. Extract only the nine nodes networks, plot those to check for variation
2. Apply HodgeRank
    - Need three colum numpy array.
3. Compare to consumption figures

```python
def extract_dataframe_of_comparisons(hamlet, data_dict):
    '''
    hamlet: str, name of hamlet, eg. hamlet_1
    data_dict: dictionary of extracted data
    
    return: Pandas dataframe
    '''
    chosen = data_dict[hamlet]["chosen"]
    
    edge_list = []
    for i in chosen:
        for j in chosen:
            if i<j:
                edge_list.append((i,j))
                
    df = pd.DataFrame(index=pd.MultiIndex.from_tuples(edge_list, names=["i","j"]),
                      columns=chosen) 
    
    for ind in chosen:
        for edge in edge_list:
            rank_i = data_dict[hamlet]["guess_rank"][ind][edge[0]]
            rank_j = data_dict[hamlet]["guess_rank"][ind][edge[1]]
            if (rank_i!=999) & (rank_j!=999):
                df.loc[edge][ind] = (rank_j - rank_i)//abs(rank_j - rank_i)
    
    id_to_hodge = {}
    hodge_to_id = {}
    
    x = 0
    for ind in chosen:
        id_to_hodge[ind] = x
        hodge_to_id[x] = ind
        x+=1
        
    df.reset_index(inplace=True)
    df["i_hodge"] = df.i.map(id_to_hodge)
    df["j_hodge"] = df.j.map(id_to_hodge)
    
    return (df, id_to_hodge, hodge_to_id, chosen)
```

```python
def use_HodgeRank(i):
    '''
    i: integer for hamlet number
    
    
    '''
    np.random.seed(seed=seed)
    
    hamlet = "hamlet_" + str(i)
    (df, id_to_hodge, hodge_to_id, chosen) = extract_dataframe_of_comparisons(hamlet, data_dict)
    
    hodge_scores = pd.DataFrame()
    for ind in chosen:
        included = list(set(chosen)-set([ind]))
        df["mean_over_ind"] = df[included].mean(axis=1)
        # df["sum_over_ind"] = df[included].mean(axis=1, min_count=1)
        R = df[df.mean_over_ind.notnull()][["i_hodge","j_hodge"]].values
        Y = df[df.mean_over_ind.notnull()].mean_over_ind.values
        W = np.ones(len(Y))
        (s, I, H) = doHodge(R, W, Y)

        
        hs_ind = pd.DataFrame()
        hs_ind["hodge_id"] = np.array(range(0,len(s)))
        hs_ind["hodge_s"] =  s
        hs_ind["id"] = hs_ind.hodge_id.map(hodge_to_id) # Need to be careful this mapping is done accurately
        hs_ind["excluded"] = ind
        
        (a, b, c) = getConsistencyRatios(Y, I, H, W)
        hs_ind["local_inconsistency"] = b
        hs_ind["global_inconsistency"] = c
        
        hodge_scores = pd.concat([hodge_scores,hs_ind])
    
    consumption = pd.DataFrame.from_dict(data_dict[hamlet]["consumption"], orient='index', columns=["consumption"])
    consumption.reset_index(inplace=True)
    consumption.rename(columns={'index':'id'}, inplace=True)
    
    result = pd.merge(consumption,hodge_scores,on='id')
    
    result = pd.merge(result,df_SA[df_SA.hamlet==i][['id','self_assessed_wealth']],on='id')
    
    try:
        result = pd.merge(result,df_CBT[df_CBT.hamlet==i],on='id')
    except:
        result['ranking_meeting'] = np.nan
        result['quota_final'] = np.nan
        result['nhhrank'] = np.nan

    return result
```

### Complete analysis

```python
df = pd.DataFrame()
for h in range(1,640):
    try:
        df_h = use_HodgeRank(h)
        df_h = df_h[df_h.id==df_h.excluded].copy()
        df = pd.concat([df,df_h])
    except:
        continue
;
```

A few of the hamlets did not work:

```python
df_CBT.hamlet.nunique() - df.hamlet.nunique()
```

Clean up rounding errors for some of measures.

```python
df[['hodge_s',
    'local_inconsistency',
    'global_inconsistency']] = df[['hodge_s','local_inconsistency','global_inconsistency']].round(10)
```

```python
df['ranking_meeting_norm'] = df.ranking_meeting/df.nhhrank
```

### Descriptive statistics

```python
df[['consumption','hodge_s','local_inconsistency','hamlet',
    'maintreatment','elite_meeting','ranking_meeting_norm']].describe()
```

```python
df[['consumption','self_assessed_wealth','hodge_s','ranking_meeting_norm']].corr(method="spearman")
```

```python
df[df.elite_meeting==0][['consumption','self_assessed_wealth','hodge_s','ranking_meeting_norm']].corr(method="spearman")
```

```python
df[df.elite_meeting==1][['consumption','self_assessed_wealth','hodge_s','ranking_meeting_norm']].corr(method="spearman")
```

## Targeting

```python
df[df.ranking_meeting>df.quota_final].consumption.describe()
```

```python
df[df.ranking_meeting<=df.quota_final].consumption.describe()
```

```python
cutoff = -0.274
```

The exact hodge scores depend on the random seed in the least squares solver.

```python
df[df.hodge_s<cutoff].consumption.describe()
```

```python
df[df.hodge_s>=cutoff].consumption.describe()
```

```python
df[["hodge_s","ranking_meeting","consumption"]].describe()
```

And now self assessed

```python
df[df.ranking_meeting>df.quota_final].self_assessed_wealth.describe()
```

```python
df[df.ranking_meeting<=df.quota_final].self_assessed_wealth.describe()
```

```python
df[df.hodge_s<cutoff].self_assessed_wealth.describe()
```

```python
df[df.hodge_s>cutoff].self_assessed_wealth.describe()
```

Create variables for targeting

```python
df["HodgeCBT_targets"] = np.where(df.hodge_s<cutoff,"Included","Excluded")
```

```python
df["tradCBT_targets"] = np.where(df.ranking_meeting<=df.quota_final,"Included","Excluded")
```

```python
pd.crosstab(df.HodgeCBT_targets,df.tradCBT_targets)
```

**HodgeCBT scores by hamlet**

Even though the HodgeRank algorithm sets the mean of the scores to zero, we exclude the reports of $i$ when determining the score of $i$. This mean each observation is based on slightly different ranking data and the mean scores do not always exactly equal zero.

```python
df.groupby('hamlet').hodge_s.describe().round(4).sample(10)
```

Export dataframe

```python
df.to_csv("../data/analysis.csv", index=False)
```

---


## Hamlet level

```python
df_ham = pd.DataFrame()
```

```python
df_ham["count_hh"] = df.groupby('hamlet').id.count()
```

```python
df_ham["corr_SAW_hodge"] = df.groupby('hamlet').apply(lambda df: df['self_assessed_wealth'].corr(df['hodge_s'], 
                                                                                                 method='spearman'))
```

```python
df_ham["corr_SAW_meet"] =df.groupby('hamlet').apply(lambda df: df['self_assessed_wealth'].corr(df['ranking_meeting'], 
                                                                                               method='spearman'))
```

```python
df_ham["corr_consum_hodge"] = df.groupby('hamlet').apply(lambda df: df['consumption'].corr(df['hodge_s'], 
                                                                                                 method='pearson'))
```

```python
df_ham["corr_consum_meet"] =df.groupby('hamlet').apply(lambda df: df['consumption'].corr(df['ranking_meeting_norm'], 
                                                                                               method='pearson'))
```

```python
df_ham["consum_sd"] =df.groupby('hamlet').consumption.std()
```

## Cycle ratio

```python
df_ham["local_incon"]  = df.groupby('hamlet').local_inconsistency.mean()
```

```python
df_ham["global_incon"]  = df.groupby('hamlet').global_inconsistency.mean().round(3)
```

Note that in complete ranking graphs, the measure of global inconsistencies is zero by definition. This is because the algorithm first measures cycles of length 3 and then considers any remaining cycles.

```python
df_ham["cycle_ratio"] = df_ham["local_incon"] + df_ham["global_incon"]
```

```python
df_ham[["corr_consum_hodge","corr_SAW_hodge","cycle_ratio","consum_sd"]].corr()
```

```python
plt.figure(figsize=(14,5))
df_ham.cycle_ratio.hist(bins=50) ;
```

Notice the outliers with high cycle ratios. Inspect these hamlets.

```python
list(df_ham[df_ham.local_incon>0.5].index.values)
```

```python
for num in list(df_ham[df_ham.local_incon>0.5].index.values):
        try:
            key = "hamlet_" + str(num)
            graph = data_dict[key]["graph"]
            chosen = data_dict[key]["chosen"]
            print("----------------------------------------------------------------------------")
            print(key)
            print("----------------------------------------------------------------------------")
            
            nx.draw(graph.subgraph(chosen))
            
            plt.show()
        except:
            print(key)
```

Is the connectivity of the outlier networks lower than the other networks? 

```python

```

Export data

```python
df_ham.to_csv("../data/analysis_hamlet_level.csv", index=False)
```

---

## Graph networks

```python
x = 0
for key in data_dict.keys():
    if x <= 5:
        try:
            graph = data_dict[key]["graph"]
            chosen = data_dict[key]["chosen"]
            print("----------------------------------------------------------------------------")
            print(key)
            print("----------------------------------------------------------------------------")
            
            nx.draw(graph.subgraph(chosen))
            
            plt.show()
        except:
            print(key)
            continue
        x+= 1
```

---

## Additional analysis


### Correlation

```python
sns.set(style="ticks")
```

```python
df_ham[df_ham.corr_SAW_meet<df_ham.corr_SAW_hodge].count_hh.count()
```

```python
df_ham[df_ham.corr_SAW_meet>=df_ham.corr_SAW_hodge].count_hh.count()
```

```python
# Show the joint distribution using kernel density estimation
g = sns.jointplot(df_ham.corr_SAW_meet, df_ham.corr_SAW_hodge, kind="hex", color="#4CB391")

x0, x1 = g.ax_joint.get_xlim()
y0, y1 = g.ax_joint.get_ylim()
lims = [1,-1]
g.ax_joint.plot(lims, lims, ':k');
```

```python
comp_bins = np.linspace(-1.01,1.01,20)
```

```python
df_ham.corr_SAW_hodge.hist(bins=comp_bins)
df_ham.corr_SAW_meet.hist(bins=comp_bins, color='r',alpha=0.5)
```

```python
df_ham.corr_SAW_meet.hist()
```

```python
sns.jointplot(df[df.consumption<1000].consumption, df[df.consumption<1000].hodge_s, 
              kind="hex", color="#4CB391")
```

```python
sns.jointplot(df[df.consumption<1000].consumption, df[df.consumption<1000].ranking_meeting_norm, 
              kind="hex", color="#4CB391")
```
