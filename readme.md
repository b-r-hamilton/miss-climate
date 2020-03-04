# ___ESSENTIALLY DEPRECATED, MISS-ATMO IS BETTER___
# Overview
code used to analyze/visualize river and environmental datasets including

- USACE river gage data
- NCEP-NCAR reanalysis data (specifically version 3)


## Packages

- env_methods: methods used to import/read/analyze 3+ dimensional environmental datasets (NCEP-NCAR) 
- vis_methods: methods used to visualize all results 
- river_methods: methods used to read USAC river gage data
- generate_doi: get() method for shortterm_climate_analysis/longterm_climate_analysis programs

## Scripts
sorted by project (and in order of age of development) 
- NCEP-NCAR to USACE analysis programs
	- shortterm_climate_analysis
	- longterm_climate_analysis
	- full_river_analysis
	- full_river_analysis2
	- print top dates: used to try to start to debug weird problem 
	- miss_pca: principal component analysis 

## known bugs

 1. something is going on with generate_doi()/river_methods - full_river_analysis2 replaces this with janky excel reading method