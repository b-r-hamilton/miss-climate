# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 17:52:30 2019

@author: bydd1
"""
import env_methods as em
import generate_doi
import time as module_time
import datetime as dt 
import numpy as np
import os

start_time = module_time.time()

directory = r'C:\Users\bydd1\Documents\Research\Data\gridded environmental'
file = r'sst.mon.mean.nc'
image_folder = r'C:\Users\bydd1\Documents\Research\SST Images'

time, lat, lon, var = em.get_sst_mon_mean(directory, file, 'sst')

lat_bounds = [29.6, 18]
lon_bounds = [360 -98, 360 - 75.8]
#lat_bounds = [max(lat), min(lat)]
#lon_bounds = [min(lon), max(lon)]
lat_ind = [em.find_closest_val(lat_bounds[0], lat), em.find_closest_val(lat_bounds[1], lat)]
lon_ind = [em.find_closest_val(lon_bounds[0], lon), em.find_closest_val(lon_bounds[1], lon)]

mois, _ = generate_doi.get() #retrieve mois from generate_doi 

print("--- %s seconds ---" % (module_time.time() - start_time))

location_index = 2 #alphabetical, 0 for arkansas city, 1 for helena, 2 for vicksburg

moi = mois[location_index]

months_before = 6

time_ordinal = [dt.date.toordinal(x) for x in time]

for m in moi:
    date = dt.date(m[1], m[0], 1) #make date object holding month, year, on 1st day 
    date = dt.date.toordinal(date) #convert to ordinal
    time_index = em.find_closest_val(date, time_ordinal) #find closest index
    
    image = var[time_index:time_index + months_before, lat_ind[0]:lat_ind[1], lon_ind[0]:lon_ind[1]]
    mean_image = np.nanmean(image, axis = 0)
    stdev_image = np.std(image, axis = 0)

    file_name = str(location_index) + '_' +str(m[1]) +'_' + str(m[0]) + '.png'
    filepath = os.path.join(image_folder, file_name)
    title = '6 months preceding ' +str(m[1]) + '/' +str(m[0])
    em.plot_images(mean_image, stdev_image, 
                   lat[lat_ind[0]:lat_ind[1]], 
                   lon[lon_ind[0]:lon_ind[1]], filepath, title, 'deg C')
    
#september is typically the driest month, so for each location, print 3 random years of analysis for September
years = [1930, 1960, 1990]

for y in years:
    
    date_obj = dt.date(y, 9, 1)
    date = dt.date.toordinal(date_obj)
    time_index = em.find_closest_val(date, time_ordinal)
    image = var[time_index:time_index + months_before, lat_ind[0]:lat_ind[1], lon_ind[0]:lon_ind[1]]
    mean_image = np.nanmean(image, axis = 0)
    stdev_image = np.std(image, axis = 0)
    
    file_name = 'dry_' + str(location_index)  +'_' + str(date_obj.year) + '.png'
    filepath = os.path.join(image_folder, file_name)
    title = '6 months preceding ' +str(date_obj)
    em.plot_images(mean_image, stdev_image, 
                   lat[lat_ind[0]:lat_ind[1]], 
                   lon[lon_ind[0]:lon_ind[1]],
                   filepath, title, 'deg C')
    
    



    
    
    
    