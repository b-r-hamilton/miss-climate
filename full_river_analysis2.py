# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 17:07:17 2019
Same as full_river_analysis but uses top ten dates as is 
@author: bydd1
"""

#custom libraries
import env_methods as em
import vis_methods as vm 

#python libraries 
import os 
import datetime as dt
import numpy as np

#where we are saving generated images to
image_folder = r'C:\Users\bydd1\Documents\Research\reanalysis 3 images_correct 2'
num_months = 6 #number of months prior to peak streamflow date to get data for 
top_days = 10 #produce images for 10 dates with highest discharge 

#location of NCEP-NCAR Reanalysis 3 data - air temp (@ 2m, corollary for SST), precip, and SLP  
ncep_folder = r'C:\Users\bydd1\Documents\Research\Data\NCEP NCAR Reanalysis 3\Monthly Means'
ncep_files = ['air.2m.mon.mean.nc','prate.mon.mean.nc', 'pres.sfc.mon.mean.nc']
ncep_ltm = ['air.2m.mon.ltm.nc','prate.mon.ltm.nc', 'pres.sfc.mon.ltm.nc']

#netCDF variable names - in order of file names above!
var_names = ['air', 'prate', 'pres']

#get 3rd reanalysis data 
time, lat, lon, air = em.get_3rd_reanalysis(ncep_folder, ncep_files[0], var_names[0]) #time, lat, lon equivalent between datasets
#_, _, _, prate = em.get_3rd_reanalysis(ncep_folder, ncep_files[1], var_names[1])
#_, _, _, pres = em.get_3rd_reanalysis(ncep_folder, ncep_files[2], var_names[2])

#bounding box for ENSO region 
lat_bounds_enso = [-25, 25]
lon_bounds_enso = [-50, 110]

#Atlantic
lat_bounds_gom = [14, 44]
lon_bounds_gom = [80, 150]

#lat_bounds_gom = [16, 31]
#lon_bounds_gom = [78, 100]

lat_bounds_full = [min(lat), max(lat)]
lon_bounds_full = [min(lon), max(lon)]

#ROIS 
regions = ['enso', 'gom', 'full']
lat_bounds = [lat_bounds_enso, lat_bounds_gom, lat_bounds_full]
lon_bounds = [lon_bounds_enso, lon_bounds_gom, lon_bounds_full]
 
#get streamflow data - returns as dictionary, then extract important data (dates + discharges)
locations = ['hermann', 'louisville', 'vicksburg']
#dictionary = rm.get_streamflow_data(river_folder, river_files, locations)
#dis_dates = []
#dis = []

river_file = r'C:\Users\bydd1\Documents\Research\Data\river data\USGS\top_ten.csv'
import pandas as pd 
dis_dates0 = pd.read_csv(river_file)
dis_dates = []
for name in locations:
    vals = dis_dates0[name].tolist()
    for val in vals:
        new = dt.datetime.strptime(val, "%m/%d/%Y")
        vals[vals.index(val)] = new 
    dis_dates.append(vals)
    
    
time_greg = [(x - dt.datetime(1800, 1, 1, 0, 0, 0)).days for x in time] #convert time to gregorian digits for easy math 

#%%
for geospatial_subset in range(len(regions)):

    lb1 = lat_bounds[geospatial_subset]
    lb2 = lon_bounds[geospatial_subset]
    lb2_con = [x + 180 for x in lb2]
    air_sub, lat_sub, lon_sub = em.subset_data_one(air, lat, lon, time, lb1, lb2_con, normalize = True)
        
    for i in range(len(locations)): #iterate through each locations 
        dates = dis_dates[i]
        
        folder = os.path.join(image_folder, locations[i]) #go to sub-folder for location
        
        frames1 = [] #for air 
        
        for d in dates: #iterate through top 10 dates 
            
            month = d.month 
            year = d.year
            fname = str(i) + '_' + str(month) + '_' + str(year) + '.png' #make file name: index_month_year.png 
            path = os.path.join(folder, fname) #make file path: location folder + file_name 
            
            #find time index within NCEP-NCAR dataset - convert to days since 1/1/1800, subtract from time_greg
            time_index = em.find_closest_val((d - dt.datetime(1800, 1, 1, 0, 0, 0)).days, time_greg)
            
            #find the mean of the x months before the date 
            frame1 = np.mean(air_sub[time_index - num_months :time_index, :, :], axis = 0)
            
#            if geospatial_subset == len(regions) - 1: #only generate these images for full-world 
#                vm.generate_3_var_img(frame1, frame2, frame3, time[time_index], path, lat_sub, lon_sub)
            
            #append to means for that location 
            frames1.append(frame1)
            
            
        if geospatial_subset != len(regions) - 1:
#            print('geospatial subset = ' + str(geospatial_subset))
            #convert to array 
            frames1 = np.asarray(frames1)
            
            #take temporal mean 
            frames1 = np.mean(frames1, axis = 0)
            
#            for x in [frame1, frame2, frame3]:
#                if np.nanmax(x) > 1: print('error, max = ' + str(np.nanmax(x)))
#                if np.nanmin(x) < -1: print('error, min = ' + str(np.nanmin(x)))
            
            #generate 3 var image 
            fname = 'top_ten_anomaly_mean_' + regions[geospatial_subset] + '_' + str(i) + '.png'
            path = os.path.join(folder, fname)
            
            plot_lat = np.linspace(lb1[0], lb1[1], num = len(lat_sub) + 1)
            plot_lon = np.linspace(lb2[0], lb2[1], num = len(lon_sub) + 1)

            vm.single_mesh(frames1, plot_lat, plot_lon, path, 
                           'Std. Temp. Averaged @ Top 10 Discharge Dates @ ' + str(locations[i]))