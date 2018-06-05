""" Clean data to return csv of all students in program (eg BEng) """

#=============================================================================#
# Set working directory to current folder containing script
#=============================================================================#
import os
cwd = os.path.dirname(os.path.realpath(__file__))
os.chdir(cwd)

#=============================================================================#
# Read in data:
#=============================================================================#
import cf_module as cf

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


