# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 18:30:03 2019
Methods used to handle NCEP-NCAR 4D datasets 
@author: bydd1
"""
from netCDF4 import Dataset
import os 
import datetime as dt 
import numpy as np 
import sys

#convert time from cardinal to datetime obj, if values in array are time in days 
def convert_time_days(arr, origin):
    arr = [origin + dt.timedelta(days = i) for i in arr]
    return arr

#convert time from cardinal to datetime obj, if values in array are time in hours 
def convert_time_hours(arr, origin):
    arr = [origin + dt.timedelta(hours = i) for i in arr]
    return arr

#retrieve monthly gridded mean SST data - this works for 1st reanalysis data 
def get_sst_mon_mean(directory, file, var):
    f = Dataset(os.path.join(directory, file), 'r', format = 'NETCDF4')
    lat = f['lat'][:].data
    lon = f['lon'][:].data
    time = f['time'][:].data
    sst = f[var][:].data
    sst[sst > 1000] = np.nan
    if var == 'sst':
        origin = dt.datetime(1891, 1, 1, 0, 0, 0) #for sst 
        time = convert_time_days(time, origin)
    
    if var == 'rhum': 
        origin = dt.datetime(1800, 1, 1, 0, 0, 0) #for rhum
        time = convert_time_hours(time, origin)
    sd = dt.datetime.strftime(time[0], '%b %d, %Y')
    ed= dt.datetime.strftime(time[-1], '%b %d, %Y')
    print(str(len(time)) + ' entries from ' +sd + ' to ' +ed)
    return time, lat, lon, sst

#retrieve 3rd reanalysis data - very similar to above method 
def get_3rd_reanalysis(directory, file, var_name):
    f = Dataset(os.path.join(directory, file), 'r', format = 'NETCDF4')
    lat = f['lat'][:].data
    lon = f['lon'][:].data
    time = f['time'][:].data

    var = f[var_name][:].data
    var[var < -10000] = np.nan
    
    origin = dt.datetime(1800, 1, 1, 0, 0, 0) 
    time = convert_time_hours(time, origin)
    sd = dt.datetime.strftime(time[0], '%b %d, %Y')
    ed = dt.datetime.strftime(time[-1], '%b %d, %Y')
    print(str(len(time)) + ' entries from ' +sd + ' to ' +ed)

    return time, lat, lon, var



#find the closest value to some specified value in an array 
def find_closest_val(val, arr):
    diff = [abs(x - val) for x in arr]
    index = diff.index(min(diff))
    return index 


    
#return all air temp and pressure data between two date ranges 
    #this should be used for any dataset where the files have to be downloaded individually 
def get_air_and_gph(start_date, stop_date):
    if start_date.year != stop_date.year:
        sys.exit('dates must be in same year for em.get_air_temp()')
    if 1948 >= start_date.year >= 2019:
        sys.exit('temp/pressure data only available for 1948 - 2019')
    
    directory1 = r'C:\Users\bydd1\Documents\Research\Data\ncep ncar reanalysis air surface 4 times daily'
    directory2 = r'C:\Users\bydd1\Documents\Research\Data\ncep ncar reanalysis gph 4 times daily'
    
    file1 = 'air.sig995.' + str(start_date.year) + '.nc'
    file2 = 'hgt.' + str(start_date.year) +'.nc'
    
    print(os.path.join(directory1, file1))

    dataset_air = Dataset(os.path.join(directory1, file1), 'r', format = 'NETCDF4')
    dataset_gph = Dataset(os.path.join(directory2, file2), 'r', format = 'NETCDF4')
    
    #time/lat/lon appear to be same between datasets, this could cause problem in future
    time = dataset_air['time'][:].data
    lat = dataset_air['lat'][:].data
    lon = dataset_air['lon'][:].data
    
    time_new = air_time_converter(time) #get datetime obj
    
    start_ind = find_closest_val(air_time_converter_to_greg(start_date), time) #use cylindrical time to figure this out
    stop_ind = find_closest_val(air_time_converter_to_greg(stop_date), time)
    
    time_new = time_new[start_ind:stop_ind]
    
    air = dataset_air['air'][start_ind:stop_ind, :, :]
    
    gph = dataset_gph['hgt'][start_ind:stop_ind, 0, :, :] #at zeroth level
    
    air = np.asarray(air) #necessary so its not a masked array
    air = np.subtract(air, 273.15) #convert from kelvin to celsius
    gph = np.asarray(gph)
    
    return air, gph, time_new, lat, lon

def air_time_converter(arr):
    origin = dt.datetime(1800, 1, 1, 0, 0, 0)
    new_array = [origin + dt.timedelta(hours = x) for x in arr]
    return new_array

def air_time_converter_to_greg(date):
    origin = dt.datetime(1800, 1, 1, 0, 0, 0 )
    hours = (date - origin).days * 24
    return hours


def normalize_data(var, time):
    mean_monthly = []
    stdev_monthly = []
    
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
                                     stdev_monthly[month - 1])
        var[time.index(date), :, :] = normalized_frame
    
    return var
        

#geospatially subset and normalize data 
def subset_data(air, pres, prate, lat, lon, time, lat_bounds, lon_bounds):
    #cut data to bounding box 
    lat_ind = [find_closest_val(lat_bounds[0], lat), find_closest_val(lat_bounds[1], lat)]
    lon_ind = [find_closest_val(lon_bounds[0], lon), find_closest_val(lon_bounds[1], lon)]
#    print('lat_ind = ' +str(lat_ind))
#    print('lon_ind = ' +str(lon_ind))
    lat = lat[lat_ind[0]:lat_ind[1]]
    lon = lon[lon_ind[0]:lon_ind[1]]
    air = air[:, lat_ind[0]:lat_ind[1], lon_ind[0]:lon_ind[1]]
    pres = pres[:, lat_ind[0]:lat_ind[1], lon_ind[0]:lon_ind[1]]
    prate = prate[:, lat_ind[0]:lat_ind[1], lon_ind[0]:lon_ind[1]]
    
    #normalize data 
    air = normalize_data(air, time)
    pres = normalize_data(pres, time)
    prate = normalize_data(prate, time)
    
    return air, pres, prate, lat, lon 
    
    