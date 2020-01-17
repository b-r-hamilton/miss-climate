code used to analyze/visualize river and environmental datasets including
	USACE river gage data
	NCEP-NCAR reanalysis data (specifically version 3)
	GLOFAS river discharge data 

packages
	env_methods: methods used to import/read/analyze 3+ dimensional environmental datasets (NCEP-NCAR)
	vis_methods: methods used to visualize all results 
	river_methods: methods used to read USACE river gage data 
	generate_doi: get() method for shortterm_climate_analysis/longterm_climate_analysis programs 

programs, sorted by project (and in order of age of development) 
	NCEP-NCAR to USACE analysis programs
		shortterm_climate_analysis
		longterm_climate_analysis
		full_river_analysis
		full_river_analysis2
		print top dates: used to try to start to debug weird problem 
		miss_pca: principal component analysis 
	
	GLOFAS river discharge data project
		copernicus_data_extraction: processes the 300GB of river discharge data, finds means/peaks/mins annually

known bugs
	something is going on with generate_doi()/river_methods - full_river_analysis2 replaces this with janky excel reading method