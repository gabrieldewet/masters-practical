# Data wrangling:

Ready data for use in constructing BN's.

### Notes:

* Maximum number of repeated modules are 6 (occuring twice)
* Repeated modules are marked with *(R)* in the course code
* All postgraduate modules are removed
* When module was taken is indicated in the course code column as:
	* S1 	-> First Semester & Winter School
	* S2 	-> Second Semester & Summer School
	* Y 	-> Year
	* Q1:Q4	-> Quarter1 to Quarter 4
	* SE	-> Special Examination
* In cases where a student repeats a module more than once, the max mark is used
* Removed attendance modules

### Dimensions for final csv files
* Based on thresholds of empty values per module (e.g. 340 modules had at least 10 non-empty values)
* Missing values in output are indicated with "NA"
* Self discretized files see "NA" as own category

Threshold | Students | Modules
----------|----------|--------
0 | 1114 | 1219
10 | 1114 | 340
20 | 1114 | 231
50 | 1114 | 157
100 | 1114 | 118
150 | 1114 | 82
200 | 1114 | 57
300 | 1114 | 38

### Target variables reference

Target | Meaning
----------|---------
Graduated_x | Graduated BEng in minimum + x years 
Graduated (T) | Transferred from BEng and then graduated
Active (BEng) | Student still active in BEng as of 2017
Active (Other) | Student still active in other programme as of 2017
Discontinued | Self-explanatory

* Important notes on different data sets:
Another folder was added (NoDisc) that removes discontinued students. This was done because the reason for discontinued studies isn't necessarily apparent unless it is related to poor academic performance. 
Since advising a student to discontinue their studies is not in the scope of interventions for this study, the modelling could rather be focussing on students that performed poorly yet still made it in the end.
