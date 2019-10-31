# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:06:27 2019
This program generates dates of interest for usage in shortterm_climate_analysis.py and longterm_climate_analysis.py

Dates are saved as datetime.date objects, so they have no hourly component 
Dates of Interest criteria
    peak streamflow dates from USGS 
    any peak streamflow month where stage is exceeded [[x]] times
    
@author: bydd1
"""

import river_methods as rm #package of data handling + visualization methods

#locations of all USACE stage data 
directory = r'C:\Users\bydd1\Documents\Research\Data\river data'
file_vicks = r'VicksburgHistoricStage.xlsx'
file_ark = r'ArkansasCityHistoricStage.xlsx'
file_hel = r'HelenaHistoricStage.xlsx'


file_a = r'USGS\arkansas_city_peak_discharges.xlsx'
file_h = r'USGS\helena_peak_discharges.xlsx'
file_v = r'USGS\vicksburg_peak_discharges.xlsx'

peak_files = [file_a, file_h, file_v]
peak_vars = ['arkansas', 'helena', 'vicksburg']

#USACE flood stage threshold 
file_stage = r'FloodStage.xlsx'

def get():
    #get peak streamflow dates 
    dictionary = rm.get_streamflow_data(directory, peak_files, peak_vars)
    dis_dates = [dictionary[peak_vars[0]], dictionary[peak_vars[1]], dictionary[peak_vars[2]]]
    
    #get all stage data 
    _, dates_a, stages_a = rm.get_river_data(directory, file_ark)
    _, dates_h, stages_h = rm.get_river_data(directory, file_hel)
    _, dates_v, stages_v = rm.get_river_data(directory, file_vicks)
    
    stage_dates = [dates_a, dates_h, dates_v]
    stages = [stages_a, stages_h, stages_v]
    
    a_flood, h_flood, v_flood = rm.get_flood_stages(directory, file_stage)
    thresholds = [a_flood, h_flood, v_flood]
    
    #for each location, return every date/stage pair that is above the stage threshold
    a_ext_dates, a_ext_stages = rm.find_flood_events(dates_a, stages_a, a_flood)
    h_ext_dates, h_ext_stages = rm.find_flood_events(dates_h, stages_h, h_flood)
    v_ext_dates, v_ext_stages = rm.find_flood_events(dates_v, stages_v, v_flood)
    
    
    #%%
    mois = []
    #find all months with multiple high first derivative values
    for i in range(len(stages)): #iterate through locations
        stage_d = stage_dates[i]
        dis_d = dis_dates[i]
        s = stages[i]
        threshold = thresholds[i]
        
        #find all dates when abs first derivative of stage exceeds 3 stdev above mean
        high_dates, _ = rm.high_first_derivative(stage_d, s, 1) 
        ext_dates, _ = rm.find_flood_events(stage_d, s, threshold)
        
        moi = [] #months of interest 
        for d1 in dis_d: #iterate through all dates with peak streamflow (one per year, ish)
            year1 = d1.year
            month1 = d1.month
            
            counter = 0 
            flag = False
            
            for d2 in ext_dates: #iterate through all dates with high first derivative stage 
                year2 = d2.year
                month2 = d2.month
                
                if year1 == year2 and month1 == month2:
                    counter += 1
                
                if not flag and counter > 3: #if we get more than 5 high first derviatives, save the month/year tuple
                    flag = True
                    moi.append((month1, year1))
        print('num moi = ' + str(len(moi)))
        mois.append(moi)   

    return mois, dis_dates
                
        

    
    