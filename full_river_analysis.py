# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 09:24:29 2019
Generates mean anomaly images for a specific date range 
@author: bydd1
"""
#custom libraries
import env_methods as em
import river_methods as rm 
import vis_methods as vm 

#python libraries 
import os 
import datetime as dt
import numpy as np

#where we are saving generated images to
image_folder = r'C:\Users\bydd1\Documents\Research\reanalyiss 3 images'
num_months = 6 #number of months prior to peak streamflow date to get data for 
top_days = 10 #produce images for 10 dates with highest discharge 

#locations of river data 
river_folder = r'C:\Users\bydd1\Documents\Research\Data\river data\USGS'
river_files = ['hermann_peak_discharges.xlsx', 'louisville_peak_discharges.xlsx', 'vicksburg_peak_discharges.xlsx']

#location of NCEP-NCAR Reanalysis 3 data - air temp (@ 2m, corollary for SST), precip, and SLP  
ncep_folder = r'C:\Users\bydd1\Documents\Research\Data\NCEP NCAR Reanalysis 3\Monthly Means'
ncep_files = ['air.2m.mon.mean.nc','prate.mon.mean.nc', 'pres.sfc.mon.mean.nc']
ncep_ltm = ['air.2m.mon.ltm.nc','prate.mon.ltm.nc', 'pres.sfc.mon.ltm.nc']

#netCDF variable names - in order of file names above!
var_names = ['air', 'prate', 'pres']

#get 3rd reanalysis data 
time, lat, lon, air = em.get_3rd_reanalysis(ncep_folder, ncep_files[0], var_names[0]) #time, lat, lon equivalent between datasets
_, _, _, prate = em.get_3rd_reanalysis(ncep_folder, ncep_files[1], var_names[1])
_, _, _, pres = em.get_3rd_reanalysis(ncep_folder, ncep_files[2], var_names[2])

#bounding box for ENSO region 
lat_bounds_enso = [-25, 25]
lon_bounds_enso = [181, 181 + 110]

lat_bounds_gom = [16, 31]
lon_bounds_gom = [180 + 78, 180 + 100]

lat_bounds_full = [min(lat), max(lat)]
lon_bounds_full = [min(lon), max(lon)]

#ROIS 
regions = ['enso', 'gom', 'full']
lat_bounds = [lat_bounds_enso, lat_bounds_gom, lat_bounds_full]
lon_bounds = [lon_bounds_enso, lon_bounds_gom, lon_bounds_full]
 
#get streamflow data - returns as dictionary, then extract important data (dates + discharges)
locations = ['hermann', 'louisville', 'vicksburg']
dictionary = rm.get_streamflow_data(river_folder, river_files, locations)
dis_dates = []
dis = []

for i in range(len(locations)): #iterate over locations, get peak streamflow dates and discharges
    dis_dates.append(dictionary[locations[i] + '_dates'])
    dis.append(dictionary[locations[i] + '_discharges'])

time_greg = [(x - dt.datetime(1800, 1, 1, 0, 0, 0)).days for x in time] #convert time to gregorian digits for easy math 

for geospatial_subset in range(len(regions)):

    lb1 = lat_bounds[geospatial_subset]
    lb2 = lon_bounds[geospatial_subset]
    air_sub, pres_sub, prate_sub, lat_sub, lon_sub = em.subset_data(air, pres, prate, lat, lon, time, lb1, lb2)
        
    for i in range(len(locations)): #iterate through each locations 
        dates = dis_dates[i] #get dates for that location
        discharges = dis[i] #get discharges for that location 
        z = sorted(zip(discharges, dates)) #zip, sort by highest discharges 
        z = z[:top_days] #get top x discharge dates 
        discharges, dates = zip(*(z)) #unzip to original variables 
        
        folder = os.path.join(image_folder, locations[i]) #go to sub-folder for location
        
        frames1 = [] #for air 
        frames2 = [] #for pres 
        frames3 = [] #for prate 
        
        for d in dates: #iterate through top 10 dates 
            
            month = d.month 
            year = d.year
            fname = str(i) + '_' + str(month) + '_' + str(year) + '.png' #make file name: index_month_year.png 
            path = os.path.join(folder, fname) #make file path: location folder + file_name 
            
            #find time index within NCEP-NCAR dataset - convert to days since 1/1/1800, subtract from time_greg
            time_index = em.find_closest_val((d - dt.datetime(1800, 1, 1, 0, 0, 0)).days, time_greg)
            
            #find the mean of the x months before the date 
            frame1 = np.mean(air_sub[time_index - num_months :time_index, :, :], axis = 0)
            frame2 = np.mean(pres_sub[time_index - num_months :time_index, :, :], axis = 0)
            frame3 = np.mean(prate_sub[time_index - num_months :time_index, :, :], axis = 0)
            
            if geospatial_subset == len(regions) - 1: #only generate these images for full-world 
                vm.generate_3_var_img(frame1, frame2, frame3, time[time_index], path, lat_sub, lon_sub)
            
            #append to means for that location 
            frames1.append(frame1)
            frames2.append(frame2)
            frames3.append(frame3)
            
            
        if geospatial_subset != len(regions) - 1:
#            print('geospatial subset = ' + str(geospatial_subset))
            #convert to array 
            frames1 = np.asarray(frames1)
            frames2 = np.asarray(frames2)
            frames3 = np.asarray(frames3)
            
            #take temporal mean 
            frames1 = np.mean(frames1, axis = 0)
            frames2 = np.mean(frames2, axis = 0)
            frames3 = np.mean(frames3, axis = 0)
            
#            for x in [frame1, frame2, frame3]:
#                if np.nanmax(x) > 1: print('error, max = ' + str(np.nanmax(x)))
#                if np.nanmin(x) < -1: print('error, min = ' + str(np.nanmin(x)))
            
            #generate 3 var image 
            fname = str(i) + 'top_ten_anomaly_mean_' + regions[geospatial_subset] + '.png'
            path = os.path.join(folder, fname)
            vm.generate_3_var_img(frames1, frames2, frames3, time[time_index], path, lat_sub, lon_sub)
