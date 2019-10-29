# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 09:24:29 2019

@author: bydd1
"""
import env_methods as em

ncep_folder = r'C:\Users\bydd1\Documents\Research\Data\NCEP NCAR Reanalysis 3\Monthly Means'
ncep_files = ['air.2m.mon.mean.nc','prate.mon.mean.nc', 'pres.sfc.mon.mean.nc']
ncep_ltm = ['air.2m.mon.ltm.nc','prate.mon.ltm.nc', 'pres.sfc.mon.ltm.nc']

var_names = ['air', 'prate', 'pres']
river_folder = r'C:\Users\bydd1\Documents\Research\Data\river data\USGS'
river_file = 'peak_discharges_full_river.pickle'

time, lat, lon, air = em.get_3rd_reanalysis(ncep_folder, ncep_files[0], var_names[0]) #time, lat, lon equivalent between datasets
_, _, _, prate = em.get_3rd_reanalysis(ncep_folder, ncep_files[1], var_names[1])
_, _, _, pres = em.get_3rd_reanalysis(ncep_folder, ncep_files[2], var_names[2])


#%%
def normalize_data(var, time):
    import numpy as np
    mean_monthly = []
    stdev_monthly = []
    
    normalized = []
    for i in np.arange(1,13): #iterate through months
        monthly_subset = []
        
        for date in time: #iterate through all time values
            if date.month == i: #collect data from month in question
                monthly_subset.append(var[time.index(date), :, :])
            
        monthly_subset = np.asarray(monthly_subset)
            
        mean_monthly.append(np.mean(monthly_subset, axis = 0)) #average wrt time
        stdev_monthly.append(np.std(monthly_subset, axis = 0)) #stdev wrt time
    
    for date in time: #for every time value, normalize
        month = date.month
    
        frame = var[time.index(date), :, :]
        
        #normalization formula = (x - mean) / stdev
        normalized_frame = np.divide(np.subtract(frame, mean_monthly[month - 1]), 
                                     stdev_monthly[month -1])
        var[time.index(date), :, :] = normalized_frame
    
    return var
    

        
air = normalize_data(air, time)
pres = normalize_data(pres, time)
prate = normalize_data(prate, time)
 
#%%
import river_methods as rm 
dis_dates_h, dis_dates_l, dis_dates_v = rm.get_peak_streamflow_dates(river_folder, river_file, 'hermann', 'louisville', 'vicksburg')
dis_dates = [dis_dates_h, dis_dates_l, dis_dates_v]

#%%
def generate_3_var_img(frame1, frame2, frame3, date, path):
    import matplotlib.pyplot as plt
    
    plt.figure(figsize = (12, 18))
    plt.suptitle(str(date))
    print(str(date))
    plt.subplot(3,1,1)
    plt.title('normed temperature')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    mesh1 = plt.pcolormesh(lon, lat, frame1, cmap = 'coolwarm')
    plt.colorbar(mesh1)
    plt.subplot(3,1,2)
    plt.title('normed pressure')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    mesh2 = plt.pcolormesh(lon, lat, frame2, cmap = 'coolwarm')
    plt.colorbar(mesh2)
    plt.subplot(3,1,3)
    plt.title('normed precip')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    mesh3 = plt.pcolormesh(lon, lat, frame3, cmap = 'coolwarm')
    plt.colorbar(mesh1)
    
    if type(path) == str: plt.savefig(path)
    
time_index = 30   
#generate_3_var_img(air[time_index, :, :], pres[time_index, :, :], prate[time_index, :, : ], time[time_index])

import os 
import datetime as dt
import numpy as np

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
        fname = str(i) + '_' + str(month) + '_' + str(year) + '.jpg'
        path = os.path.join(folder, fname)
        
        time_index = em.find_closest_val((d - dt.datetime(1800, 1, 1, 0, 0, 0)).days, time_greg)
        
        frame1 = np.mean(air[time_index - num_months :time_index, :, :], axis = 0)
        frame2 = np.mean(pres[time_index - num_months :time_index, :, :], axis = 0)
        frame3 = np.mean(prate[time_index - num_months :time_index, :, :], axis = 0)
        
        generate_3_var_img(frame1, frame2, frame3, time[time_index], path)
