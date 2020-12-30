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
import numpy as np
import pandas as pd
```

```python
pd.set_option('display.max_columns', None)
```

## Self-assessed wealth

From Alatas et al (2012)

```python
df_SA =  pd.read_stata("../data/112522-V1/Targeting_Indonesia/codeddata/intermediate_data/selfassessment.dta")
```

    // Subjective Rank questions

    use "$data\baseline\hh_sw.dta", clear
    keep hhid sw02 sw03

    recode sw02 (8=.)
    recode sw03 (7=.)

    gen RANK_sw02= sw02/6
    gen RANK_sw03= sw03/5

```python
df_SA.RANK_sw02.value_counts()
```

```python
df_SA["self_assessed_wealth"] = df_SA.RANK_sw02*6
```

```python
df_SA["self_assessed_wealth"].value_counts()
```

Stata code used to define `hhid`:
    
    rename hhid idrt
    tostring idrt, replace
    replace idrt = "00" + idrt if length(idrt)==1
    replace idrt = "0" + idrt if length(idrt)==2

    gen hhid = hhea + idrt

```python
df_SA["hamlet"] = df_SA.hhid.astype('str').str[:-3]
```

```python
df_SA["hamlet"] = df_SA["hamlet"].astype(int)
```

```python
df_SA["id"] = df_SA.hhid.astype('str').str[-3:]
```

```python
df_SA["id"] = df_SA["id"].astype(int)
```

```python
df_SA[['hamlet','id','self_assessed_wealth']].to_csv("../data/self_assessed_wealth.csv", index=False)
```

## CBT Ranking


### Normal

```python
df_CBT =  pd.read_stata("../data/112522-V1/Targeting_Indonesia/codeddata/intermediate_data/RTS_community.dta")
```

```python
df_CBT.rename(columns={'hhea':'hamlet','idrt':'id'}, inplace=True)
```

```python
df_CBT['id'] = df_CBT.id.astype('int')
```

### Hybrid

```python
df_hybrid =  pd.read_stata("../data/112522-V1/Targeting_Indonesia/codeddata/intermediate_data/rts_hybrid.dta")
```

```python
df_hybrid.rename(columns={'hhea':'hamlet','idrt':'id','nhhrank_2':'nhhrank'}, inplace=True)
```

```python
df_hybrid['id'] = df_hybrid.id.astype('int')
```

```python
chosen_vars = ['hamlet','id','ranking_meeting','nhhrank','quota_final','maintreatment']
```

```python
df_CBT_combined = pd.concat([df_CBT[chosen_vars],df_hybrid[chosen_vars]]) 
```

### Hamlet level variables

```python
df_targeting =  pd.read_stata("../data/119802-V1/Final Data/TargetingTables.dta")
```

```python
df_targeting[df_targeting.ELITE==1].maintreatment.value_counts()
```

```python
df_targeting[df_targeting.ELITE==0].maintreatment.value_counts()
```

```python
itr = pd.read_stata("../data/119802-V1/Final Data/TargetingTables.dta", iterator=True)
itr.variable_labels()
```

```python
df_targeting.rename(columns={'village':'hamlet','ELITE':'elite_meeting'}, inplace=True) 
```

```python
df_targeting['hamlet'] = df_targeting['hamlet'].astype('int')
```

```python
df_CBT_combined = df_CBT_combined.merge(df_targeting[['hamlet','elite_meeting']],on='hamlet',how='left')
```

```python
df_CBT_combined.head()
```

### Export

```python
df_CBT_combined.to_csv("../data/community_meeting.csv", index=False)
```
