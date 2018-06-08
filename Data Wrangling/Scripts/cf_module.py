""" Module that contains all functions to be used in data wrangling """

import pandas as pd
import sys


# Number of years a student has been in a particular programme
def n_years(row):
    if int(str(row["Commencement"])[4:6]) >= 5:
        yr = int(str(row["Commencement"])[0:4]) + 1
    else:
        yr = int(str(row["Commencement"])[0:4])
    return 1 + int(row["Term"]) - yr


# Function to filter academic programmes.
def filters(df, pcode=False, startwith=False, contains=False, ncontains=False):
    # Insert filters as lists (so that multiple filters can be applied)

    original_df = df.copy()
    df = df[df["MinGrad"] > 2]
    df = df.sort_values("Academic Plan")

    if pcode:
        df = df.loc[df["QualiCode"].isin(pcode)]

    if startwith:
        df = df.loc[df["Academic Plan"].str.startswith(startwith)]

    if contains:
        df = df.loc[df["Academic Plan"].str.contains(contains)]

    if ncontains:
        df = df.loc[~df["Academic Plan"].str.contains(ncontains)]

    return df, original_df


# Functions to read student flatfiles:
def read_plan(files, **kwargs):
    # Specify filters in dictionary format

    cols = [(0,15),(106,171), (98, 99)]
    colnames = ["QualiCode","Academic Plan","MinGrad"]

    mast = pd.DataFrame()
    for f in files:
        temp_df = pd.read_fwf(f, colspecs=cols, names=colnames)
        mast = mast.append(temp_df.drop_duplicates(["QualiCode"]))

    return filters(mast, **kwargs)


# Functions to read student flatfiles:
def read_student(files, cohort, code_df, all_df):

    cols = [(0,15),(30,45),(45,53),(88,89)]
    colnames = ["Student Number", "QualiCode", "Commencement", "Quali. Status"]
    years = ["2011", "2012", "2013", "2014", "2015", "2016", "2017"]
    codelist = list(code_df["QualiCode"].unique()) #List of codes
    mingrad = 3

    code_dict = dict(zip(all_df["QualiCode"], all_df["Academic Plan"]))
    keepcol = ["Student Number", "Term", "Quali. Status",
               "PlanDesc", "Number of Years"]

    df = pd.DataFrame()
    for y,f in zip(years, files):
        temp_df = pd.read_fwf(f, colspecs=cols, names=colnames)
        temp_df.sort_values(['Student Number', 'Commencement'], inplace=True)
        temp_df.drop_duplicates(["Student Number"], inplace=True)
        temp_df["Term"] = int(y)
        temp_df.dropna(subset=['Commencement'],inplace=True)
        df = df.append(temp_df, ignore_index=True)

    df["Number of Years"] = df.apply(lambda row: n_years(row), axis=1)

    # Lambda function for early grads removal
    mapfunc = df["Quali. Status"].map(lambda x: x == "F")

    # First year student numbers:
    sn_fy = df.loc[(df["QualiCode"].isin(codelist)) &
                   (df["Term"] == cohort), "Student Number"]

    # Early grad student numbers
    sn_eg = pd.Series()
    for i in range(mingrad-1):
        sn_i = df.loc[(df["Student Number"].isin(sn_fy)) &
                       (df["Term"] == cohort + i) &
                       mapfunc, "Student Number"]

        sn_eg = sn_eg.append(sn_i)

    # Get cohort student numbers
    sn = df.loc[(~df["Student Number"].isin(sn_eg)) &
                (df["QualiCode"].isin(codelist)) &
                (df["Number of Years"] == 1) &
                (df["Term"] == cohort), "Student Number"]


    if len(sn)>0:
        df = df.loc[(df["Student Number"].isin(sn)) &
                      (df["Term"].astype(int) >= int(cohort))]

        df["PlanDesc"] = df["QualiCode"].apply(lambda row: code_dict[row])

        return df.loc[:,keepcol]

    else:
        return pd.DataFrame()


# Function for reading csv's and returning pivited data
def read_marks(files, snumbers):

    df = pd.DataFrame()
    for f in files:
        temp_df = pd.read_csv(f, sep=';')
        temp_df = temp_df.loc[temp_df["Student Number"].isin(snumbers),:]
        df = df.append(temp_df)

    # Do some additional filtering to remove students that moved from a similar
    # program (ie having exemptions and starting straight into the second year)
    cohort = min(df["Term"])

    # Bool series of students who have >1st year mods in 1sy year
    mapfunc = df["Course Code"].map(lambda x: int(str(x)[4]) != 1)

    # Get stud numbs of 1st years that are not registered for > 1st year mods
    snums = df.loc[(df["Term"]==cohort) &
                   mapfunc, "Student Number"]

    # Get dataframe containing only students from cohort
    df = df.loc[(~df["Student Number"].isin(snums))]

    return df


# Function to filter out unwanted modules and rename others
def adjust_modules(df_in):
    # Use this function inside of read_marks function to return final df

    # Keep these columns:
    keep = ["Student Number", "Term", "Course Code", "Final Mark"]

    # To do:
    # 1) Drop nan final marks (deregistered)
    df = df_in.dropna(subset = ["Final Mark"]).copy()

    # 2) Equate code 997/996 to 0 (unsatisfactory attendance) or discretize
    # 3) For code 988, let final mark = min(semestermark/2;zero) (Not admitted)
    # 4) For code 987, let final mark = min(semestermark/2;zero) (Absent)
    # 5) For code 992, let final mark = min(semestermark/2;zero) (Exam too low)
    df["Final Mark"] = df.apply(lambda row: adj_codes(row), axis=1)

    # 6) Drop code 950 (Exemption exam passed) or discretize with rest
    # 7) Drop codes 995,984,977,985,976,989,967,981 (Unknown codes)
    to_drop = [950, 995, 984, 977, 985, 976, 989, 967, 981, 997, 996]
    df = df.loc[~df["Final Mark"].isin(to_drop),:]

    # 8) Remove postgrad modules (code>4)
    mapfunc = df["Course Code"].map(lambda x: int(str(x)[4]) < 4)
    df = df.loc[mapfunc,:]

    # 9) Rename mods with labels from Session Desc
    # 10) Rename mods with (R) for repeats (normal, summer school, and special)
    df["Duped"] = df["Course Code"].shift() == df["Course Code"]
    df["Course Code"] = df.apply(lambda row: rename_mods(row), axis=1)

    df = df.reset_index()
    return df.loc[:,keep]


# Adjusts final marks with speical codes
def adj_codes(row):
#    if row["Final Mark"] in (997, 996):
#        return 0
    if row["Final Mark"] in (988, 987, 992):
        return min([row["Semester Mark"],0])
    else:
        return row["Final Mark"]


# Rename modules for clarity & repaated modules
def rename_mods(row):
    when = abbreviate(row)
    if row["Duped"]:
        return row["Course Code"] + " (R) " + when
    else:
        return row["Course Code"] + " " + when


# Function that returns abbreviations for Session Desc
def abbreviate(row):
    if row["Session Desc"] in ("First Semester", "Winter School"):
        return "(S1)"
    elif row["Session Desc"] in ("Second Semester",
                                 "Summer School Reg Students"):
        return "(S2)"
    elif row["Session Desc"] == "Year":
        return "(Y)"
    elif row["Session Desc"] == "Examination after 1 semester":
        return "(SE)"
    elif row["Session Desc"] == "Quarter One":
        return "(Q1)"
    elif row["Session Desc"] == "Quarter Two":
        return "(Q2)"
    elif row["Session Desc"] == "Quarter Three":
        return "(Q3)"
    elif row["Session Desc"] == "Quarter Four":
        return "(Q4)"


# Check plan
def get_plan(df,term):
    plan = df.loc[df["Term"]==term,"PlanDesc"].str.startswith("BEng").values[0]
    return plan


# Add target variable from cohort_df and return dictionary
def target(df,mingrad):
    base_year = min(df["Term"])
    last_year = max(df["Term"])

    # Keep only undergrad instances (postgrad confuses things)
    df = df.loc[((df["PlanDesc"].str.startswith("B")) |
                (df["PlanDesc"].str.startswith("L"))) &
                (~df["PlanDesc"].str.contains("Hons")),:]

    length = len(df["Student Number"].unique())
    i = 1
    out = {}
    for sn in df["Student Number"].unique():
        prog = int(i/length*100)
        pstr = "[" + "#"*prog + " "*(100-prog) + "] {}%".format(str(prog))
        sys.stdout.write("\r{0}".format(pstr))
        sys.stdout.flush()
        temp = df.loc[df["Student Number"] == sn,:].reset_index(drop=True)

        if "F" in temp["Quali. Status"].values:
            grad_term = temp.iloc[(temp["Quali. Status"] == "F")\
                                  .idxmax(),:]["Term"]
            if get_plan(temp, grad_term):
                grad_time = str(grad_term-base_year-mingrad+1)
                target = "Graduated_{}".format(grad_time)
            else:
                target = "Graduated (T)"

        else:
            last_term = max(temp["Term"])
            if get_plan(temp, last_term):
                if last_term == last_year:
                    target = "Active (BEng)"
                else:
                    target = "Discontinued"
            else:
                if last_term == last_year:
                    target = "Active (Other)"
                else:
                    target = "Discontinued"
        i += 1
        out[sn] = target

    return out


