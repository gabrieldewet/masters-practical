""" Clean & restructure data to return csv of all students in program """

import cf_module as cf
import os
import pandas as pd

# Read in file names:
names = ["Marks", "Qualifications", "Students"]
file_names = {name: ["../Data/{0}/{1}".format(name,f) for f in
               os.listdir('../Data/{0}'.format(name))] for
                     name in names}

# Get df containing plan codes & names
filt_dict = {'startwith':"BEng", 'ncontains':"Engage"} #Set filters
# Return dfs with filtered and unfiltered plans
fplan_df, plan_df = cf.read_plan(file_names["Qualifications"], **filt_dict)

# Get cohort df
cohort_df = cf.read_student(file_names["Students"], 2011, fplan_df, plan_df)

# Unique student numbers from cohort
snums = list(cohort_df["Student Number"].unique())

# Read in mark files
marks_df = cf.read_marks(file_names["Marks"], snums).dropna(subset = ["Final Mark"])
marks_df.sort_values(["Student Number", "Course Code", "Term"],inplace=True)


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

# df to test with:
print(marks_df.loc[marks_df["Final Mark"]>100,"Final Mark"].value_counts())
print(marks_df["Session Desc"].value_counts())

