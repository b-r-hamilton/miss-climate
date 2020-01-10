# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 10:29:01 2020

@author: bydd1
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:11:45 2020
Pull Copernicus data from 
https://cds.climate.copernicus.eu/cdsapp#!/dataset/10.24381/cds.a4fdd6b9?tab=overview

Calculate 
    1. average of mean annual flow (per pixel) 
    2. average of peak annual flow (maximum per year, average maximum)
    3. average of minimum annual flow (min per year, average) 

@author: bydd1
"""

from netCDF4 import Dataset
import os 
import numpy as np 
import env_methods as em 
import vis_methods as vm 
import datetime as dt 
import time as python_time
import pickle 
start_time = python_time.time()

def convert_datetime(val):
    origin = dt.datetime(1979, 1, 1)
    date = origin + dt.timedelta(hours = val)
    return date

directory = r'C:\Users\bydd1\Documents\Research\Data\GFAS Data (Copernicus)\dec1_tarr'
files = os.listdir(directory)

save_path = r'C:\Users\bydd1\Documents\Research\Data\Pickles\all_cds_river.pickle'

#initialize data variables 
dis_ov = np.empty(0)
time_ov = np.empty(0)
lat = np.empty(0)
lon = np.empty(0)

first_flag = False #this flag shows whether or not we've initialized the data values 


#iterate through all files in directory 
for name in files: 
    
    path = os.path.join(directory, name)
    dataset = Dataset(path, 'r', format = 'NETCDF4')
    
    time = dataset['time'][:].data
    time = convert_datetime(time[0]) #convert time to datetime object 
    dis = dataset['dis24'][:,:,:].data
    dis[dis == 1e+20] = np.nan
    
    #initialize data on first run through 
    if not first_flag:
        first_flag = True #set flag to True (we've initialized)
    
        lat = dataset['lat'][:].data #get latitude data (should be same for all files )
        lon = dataset['lon'][:].data #get longitude data 
        
        time_ov = np.array(time) #append time value to array
        dis_ov = dis
    
    #if not on first run, don't need to get lat/lon - just get new dis data and date
    else:
        time_ov = np.append(time_ov, time)
        dis_ov = np.append(dis_ov, dis, axis = 0)
    
    #print timing update (takes 0.5 seconds per file on my laptop)
    file_number = files.index(name)
    num_files = len(files)
    print(str(file_number) +' of ' + str(num_files) + ' extracted')
        

#%%
#save all data in pickle 
dictionary = {'dis' : dis,
              'time' : time_ov,
              'lat' : lat,
              'lon' : lon}


pickle.dump(dictionary, open(save_path, "wb" ) )
#open with pickle.load( open( save_path, "rb" ) )

print("--- %s seconds ---" % (python_time.time() - start_time))