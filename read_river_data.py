# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 22:13:10 2019

@author: bydd1
"""
import river_methods as rm 
import time
import numpy as np 

start_time = time.time()

#%% GET ALL USGS AND USACE DATA
#locations of all USACE stage data 
directory = r'C:\Users\bydd1\Documents\Research\Data\river data'
file_vicks = r'VicksburgHistoricStage.xlsx'
file_ark = r'ArkansasCityHistoricStage.xlsx'
file_hel = r'HelenaHistoricStage.xlsx'

#location of all USGS peak streamflow data 
p_directory = r'C:\Users\bydd1\Documents\Research\Data\river data\USGS'
p_file = r'peak_discharges.pickle'

meta_v, dates_v, stages_v = rm.get_river_data(directory, file_vicks)
meta_a, dates_a, stages_a = rm.get_river_data(directory, file_ark)
meta_h, dates_h, stages_h = rm.get_river_data(directory, file_hel)

#get flood stage levels for each location
    #note, this probably isn't a great static variable because river morphology changes over time
directory = r'C:\Users\bydd1\Documents\Research\Data\river data'
file_stage = r'FloodStage.xlsx'
a_flood, h_flood, v_flood = rm.get_flood_stages(directory, file_stage, 'arkansas', 'helena', 'vicksburg')

#intersection code, can be used if I want to temporally synchronize things 
#int_dates = rm.intersection(dates_v, dates_a)
#int_dates = rm.intersection(int_dates, dates_h)
#deltas, mode = rm.remove_nlin_inc(int_dates) 

#for each location, return every date/stage pair that is above the stage threshold
a_ext_dates, a_ext_stages = rm.find_flood_events(dates_a, stages_a, a_flood)
h_ext_dates, h_ext_stages = rm.find_flood_events(dates_h, stages_h, h_flood)
v_ext_dates, v_ext_stages = rm.find_flood_events(dates_v, stages_v, v_flood)

#get all dates where the streamflow values exceed maximum threshold 
    #USGS, annual date of maximum stream flow (not for all years, sad face)
#a_dis_dates, h_dis_dates, v_dis_dates = rm.get_peak_streamflow_dates(p_directory, p_file)

dis_dates_a, dis_dates_h, dis_dates_v = rm.get_peak_streamflow_dates(p_directory, p_file)


#%% ALL VISUALIZATIONS 
rm.plot_river_exceedences(a_ext_dates, a_ext_stages, h_ext_dates, h_ext_stages, 
                           v_ext_dates, v_ext_stages, 0)

rm.plot_river_data(h_ext_dates, h_ext_stages, 0, len(h_ext_dates) - 1, 1)

dates_diffed, stages_diffed = rm.plot_first_derivative(dates_h, stages_h, 2)
 
rm.plot_two_river_datasets(h_ext_dates, dates_diffed, h_ext_stages, stages_diffed, h_flood, 4)

rm.date_comparison(dates_h, h_ext_dates, dates_diffed, 5)

rm.date_comparison_3_dates(dates_h, h_ext_dates, dates_diffed, dis_dates_h, 6)

print("--- %s seconds ---" % (time.time() - start_time))