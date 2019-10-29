# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 17:44:03 2019

@author: bydd1
"""
import datetime as dt
import env_methods as em
import generate_doi 
import numpy as np
import os 

start_date = dt.datetime(1973, 5, 1)
stop_date = dt.datetime(1973, 5, 10)

gph_location = r'C:\Users\bydd1\Documents\Research\GPH and Temp Images\GPH'
air_location = r'C:\Users\bydd1\Documents\Research\GPH and Temp Images\Temp'

_, dois = generate_doi.get() #smart!

location_index = 2

doi = dois[location_index]

lat_bounds = [48, 27]
lon_bounds = [360 - 100, 360 - 70]

for stop_date in doi: #now iterate over the dates, generate an image for each date with mean/stdev for temp + gph 
    
    if 1948 <= stop_date.year <= 2019: 
    
        start_date = stop_date - dt.timedelta(days = 7)
        air, gph, time, lat, lon = em.get_air_and_gph(start_date, stop_date)
        
        lat_ind = [em.find_closest_val(lat_bounds[0], lat), em.find_closest_val(lat_bounds[1], lat)]
        lon_ind = [em.find_closest_val(lon_bounds[0], lon), em.find_closest_val(lon_bounds[1], lon)]
        
        lat = lat[lat_ind[0]:lat_ind[1]]
        lon = lon[lon_ind[0]:lon_ind[1]]
        air = air[:, lat_ind[0]:lat_ind[1], lon_ind[0]:lon_ind[1]]
        gph = gph[:, lat_ind[0]:lat_ind[1], lon_ind[0]:lon_ind[1]]
        air_mean = np.nanmean(air, axis = 0)
        air_stdev = np.std(air, axis = 0)
        
        gph_mean = np.nanmean(gph, axis = 0)
        gph_stdev = np.std(gph, axis = 0)
    
        file_name = str(location_index) + '_' + str(stop_date.year) + '_' + str(stop_date.month) + '_' + str(stop_date.day)
        filepath_gph = os.path.join(gph_location, file_name)
        filepath_air = os.path.join(air_location, file_name)
        
        title_air = '6 days of air temp preceding ' + str(stop_date)
        title_gph = '6 days of gph preceding ' + str(stop_date)
        
        em.plot_images(air_mean, air_stdev, lat, lon, filepath_air, title_air, 'deg C')
        em.plot_images(gph_mean, gph_stdev, lat, lon, filepath_gph, title_gph, 'm')
        
        
    
    else: print('year out of range')
    
    