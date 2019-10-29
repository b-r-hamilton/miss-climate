# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 18:30:03 2019

@author: bydd1
"""
from netCDF4 import Dataset
import os 
import datetime as dt 
import matplotlib.pyplot as plt 
import numpy as np 
from matplotlib.animation import FuncAnimation
import pandas as pd
from pydap.client import open_url 
import sys

#convert time from cardinal to datetime obj
def convert_time_days(arr, origin):
    arr = [origin + dt.timedelta(days = i) for i in arr]
    return arr

def convert_time_hours(arr, origin):
    arr = [origin + dt.timedelta(hours = i) for i in arr]
    return arr

#retrieve monthly gridded mean SST data 
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
    ed= dt.datetime.strftime(time[-1], '%b %d, %Y')
    print(str(len(time)) + ' entries from ' +sd + ' to ' +ed)

    return time, lat, lon, var

#make a movie of sst var over time 
def generate_animation(time, lat, lon, var):
    fig, ax = plt.subplots(figsize=(10, 8))
    min_var = np.nanmin(var)
    max_var = np.nanmax(var)
    mesh = ax.pcolormesh(lon, lat, var[0, :, :], vmin = min_var, vmax = max_var, cmap = 'coolwarm')
    cb = plt.colorbar(mesh)
    cb.set_label('temp (deg C)')
    ax.set_xlabel('deg longitude')
    ax.set_ylabel('deg latitude')
    ax.set_title('sst data: ' +str(time[0]))
    
    def animate(i):
        ax.clear()
        ax.pcolormesh(lon, lat, var[i, :, :], vmin = min_var, vmax = max_var, cmap = 'coolwarm')
        ax.set_xlabel('deg longitude')
        ax.set_ylabel('deg latitude')
        ax.set_title(dt.datetime.strftime(time[i], '%b %d, %Y'))
        
    anim = FuncAnimation(fig, animate, interval=1, frames=len(time)-1)
    return anim

def find_closest_val(val, arr):
    diff = [abs(x - val) for x in arr]
    index = diff.index(min(diff))
    return index 

def plot_images(mean_image, stdev_image, lat, lon, filepath, title, units):
   
    
    plt.figure(figsize = (14, 4))
    plt.subplot(1,2,1)
    mesh = plt.pcolormesh(lon, lat, mean_image, cmap = 'coolwarm')
    cbar = plt.colorbar(mesh)
    cbar.set_label(units)
    plt.title('mean')
    plt.xlabel('longitude')
    plt.ylabel('latitude')

    plt.suptitle(title)
    plt.subplot(1,2,2)
    mesh = plt.pcolormesh(lon, lat, stdev_image, cmap ='coolwarm')
    cbar = plt.colorbar(mesh)
    cbar.set_label(units)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.title('STDEV')
    plt.savefig(filepath)
    
#return all air temp and pressure data between two date ranges 
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
        