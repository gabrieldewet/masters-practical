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

""" Some methods for exploratory analysis:

#print("Cohort DF:",cohort_df.columns)
#print("Marks DF:", marks_df.columns)
#
#print(marks_df["Session Desc"].value_counts())
#print(marks_df["Course Code"].value_counts())
#
#
#for y in range(2011,2017):
#    plot_df = marks_df.loc[marks_df["Term"]==y,:]
#    plot_df = pd.DataFrame(plot_df["Course Code"].value_counts(), index=None)
#    print(len(plot_df.loc[plot_df["Course Code"]>50,:]))
#    plot_df.loc[plot_df["Course Code"]>10,:].plot.bar()

"""

#for y in range(2011,2016):
#    plot_df = df_new.loc[df_new["Term"]==y,:]
#    plot_df = pd.DataFrame(plot_df["Course Code"].value_counts(), index=None)
#    print(len(plot_df.loc[plot_df["Course Code"]>30,:]))
#    plot_df.loc[plot_df["Course Code"]>30,:].plot.bar()