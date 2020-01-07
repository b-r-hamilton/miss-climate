# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 14:23:59 2019

@author: bydd1
"""
import datetime as dt 
import river_methods as rm 

top_days = 10 
#locations of river data 
river_folder = r'C:\Users\bydd1\Documents\Research\Data\river data\USGS'
river_files = ['hermann_peak_discharges.xlsx', 'louisville_peak_discharges.xlsx', 'vicksburg_peak_discharges.xlsx']

#get streamflow data - returns as dictionary, then extract important data (dates + discharges)
locations = ['hermann', 'louisville', 'vicksburg']
dictionary = rm.get_streamflow_data(river_folder, river_files, locations)
dis_dates = []
dis = []

for i in range(len(locations)): #iterate over locations, get peak streamflow dates and discharges
    dis_dates.append(dictionary[locations[i] + '_dates'])
    dis.append(dictionary[locations[i] + '_discharges'])

dates_list = [] 
for i in range(len(locations)): #iterate through each locations 
        dates = dis_dates[i] #get dates for that location
        discharges = dis[i] #get discharges for that location 
        z = sorted(zip(discharges, dates), reverse = True) #zip, sort by highest discharges 
        z = z[0:top_days] #get top x discharge dates 
        discharges, dates = zip(*(z)) #unzip to original variables 
        
        dates_list.append(dates)
        
        