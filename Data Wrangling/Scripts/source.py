""" Clean & restructure data to return csv of all students in program """

import cf_module as cf
import os

folder = "../Out/NoDisc"

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
marks_df = cf.read_marks(file_names["Marks"], snums)
marks_df.sort_values(["Student Number", "Course Code", "Term"],inplace=True)
marks_df = cf.adjust_modules(marks_df,5)

df = marks_df.pivot_table(index='Student Number',
                              columns='Course Code',
                              values='Final Mark',
                              aggfunc=max).reset_index().copy()

cohort_df = cohort_df.loc[cohort_df["Student Number"]\
                          .isin(marks_df["Student Number"].unique()),:]

target_dict = cf.target(cohort_df,4)

# Uncomment for binary target variable
#target_dict = cf.bin_target(cohort_df)

df.loc[:,"Target"] = df.apply(lambda row: \
            target_dict[int(row["Student Number"])], axis=1)

# Uncomment below if no discontinued students are wanted
df = cf.remove_disc(df)

## Write to csv

# All modules
df.fillna("NA").to_csv("{}/all_modules.csv".format(folder),
                      sep=";",index=False)
cf.discretize(df.fillna(999)).to_csv("{}/all_modules_(dsc).csv".format(folder),
                         sep=";", index=False)

# Various thresholds
thresh = [10,20,50,100,150,200,300]

for t in thresh:
    thresh_df = df.dropna(thresh=t, axis='columns').copy()
    print("\n{0} : {1}".format(t,(thresh_df.shape)))
    thresh_df.fillna("NA").to_csv("{0}/{1}_modules.csv".format(folder,t),
                     sep=";",index=False)
    cf.discretize(thresh_df.fillna(999))\
                 .to_csv("{0}/{1}_modules_(dsc).csv"\
                         .format(folder,t), sep=";", index=False)









