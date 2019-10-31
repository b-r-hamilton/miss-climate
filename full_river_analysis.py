# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 09:24:29 2019

@author: bydd1
"""
import env_methods as em
import river_methods as rm 
import vis_methods as vm 

import os 
import datetime as dt
import numpy as np

ncep_folder = r'C:\Users\bydd1\Documents\Research\Data\NCEP NCAR Reanalysis 3\Monthly Means'
ncep_files = ['air.2m.mon.mean.nc','prate.mon.mean.nc', 'pres.sfc.mon.mean.nc']
ncep_ltm = ['air.2m.mon.ltm.nc','prate.mon.ltm.nc', 'pres.sfc.mon.ltm.nc']

var_names = ['air', 'prate', 'pres']
river_folder = r'C:\Users\bydd1\Documents\Research\Data\river data\USGS'
river_files = ['hermann_peak_discharges.xlsx', 'louisville_peak_discharges.xlsx', 'vicksburg_peak_discharges.xlsx']

time, lat, lon, air = em.get_3rd_reanalysis(ncep_folder, ncep_files[0], var_names[0]) #time, lat, lon equivalent between datasets
_, _, _, prate = em.get_3rd_reanalysis(ncep_folder, ncep_files[1], var_names[1])
_, _, _, pres = em.get_3rd_reanalysis(ncep_folder, ncep_files[2], var_names[2])

#%%
air = em.normalize_data(air, time)
pres = em.normalize_data(pres, time)
prate = em.normalize_data(prate, time)
 
#%%
location_names = ['hermann', 'louisville', 'vicksburg']
dictionary = rm.get_streamflow_data(river_folder, river_files, location_names)
dis_dates = [dictionary[location_names[0]], dictionary[location_names[1]], dictionary[location_names[2]]]

#%%
locations = ['hermann', 'louisville', 'vicksburg']
image_folder = r'C:\Users\bydd1\Documents\Research\reanalyiss 3 images'

num_months = 6

time_greg = [(x - dt.datetime(1800, 1, 1, 0, 0, 0)).days for x in time]

for i in range(len(dis_dates)):
    dates = dis_dates[i]
    folder = os.path.join(image_folder, locations[i])
    
    for d in dates:
        
        month = d.month
        year = d.year
        fname = str(i) + '_' + str(month) + '_' + str(year) + '.png'
        path = os.path.join(folder, fname)
        
        time_index = em.find_closest_val((d - dt.datetime(1800, 1, 1, 0, 0, 0)).days, time_greg)
        
        frame1 = np.mean(air[time_index - num_months :time_index, :, :], axis = 0)
        frame2 = np.mean(pres[time_index - num_months :time_index, :, :], axis = 0)
        frame3 = np.mean(prate[time_index - num_months :time_index, :, :], axis = 0)
        
        vm.generate_3_var_img(frame1, frame2, frame3, time[time_index], path, lat, lon)
