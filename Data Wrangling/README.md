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

### Dimensions for final csv files
* Based on thresholds of empty values per module (e.g. 340 modules had at least 10 non-empty values)

Threshold | Students | Modules
----------|----------|--------
- | 1114 | 1219
10 | 1114 | 340
20 | 1114 | 231
50 | 1114 | 157
100 | 1114 | 118
150 | 1114 | 82
200 | 1114 | 57
300 | 1114 | 38