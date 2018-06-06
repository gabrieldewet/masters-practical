#%%
import pandas as pd
df = pd.DataFrame({
    'A' : 1.,
    'name' :  pd.Categorical(["hello","hello","hello","hello"]),
    'col_2' : pd.Categorical(["2","2","12","Nan"]),
    'col_3' : pd.Categorical(["11","1","3","Nan"])})

#%%
name_index = df[['col_2', 'col_3']].apply(pd.to_numeric, errors='coerce').ge(10).any(axis=1).cumsum()
df['name'] = df['name'].astype(str) + '_' + name_index.astype(str)
print(df)