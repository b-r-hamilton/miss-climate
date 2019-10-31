# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 23:35:00 2019
Methods used to import, format, and display USACE and USGS river stage data
Note: USGS data must first be fed through the read_
@author: bydd1
"""

import os
import pandas as pd
import numpy as np
import datetime as dt

import statistics
import datetime
import pickle 

#__________________________________METHODS_____________________________________

#retrieve river data from 
    #http://rivergages.mvr.usace.army.mil/WaterControl/shefgraph-historic.cfm?sid=CE40FF58
    #will download in Excel '97 file, reformat to .xlsx workbook in Excel so pandas can tak to it
    #may need to change '11' index (slices at end of metadata) for actuall implementation with real files
def get_river_data(directory, file):
    x = pd.read_excel(os.path.join(directory, file))
    meta = x[:11] #pull out metadata as a DataFrame
    col = list(x.columns) # get column names - stupid long strings
    data = x[11:-1] #get all data, excluding 
    
    #check to see if date values are in datetime objects, convert if not 
    if not isinstance(data.loc[11, col[0]], datetime.datetime):
        data.loc[:, col[0]] = pd.to_datetime(data.loc[:, col[0]])

    data = np.asarray(data) #convert to array 
    
    #remove any rows that have string values for the stage height (specifically helena uses 'M' as a NaN)
    data_new = []
    for i in range(np.shape(data)[0]):
        if not isinstance(data[i, 1], str):
            data_new.append(data[i, :])
    data_new = np.asarray(data_new)
    data = data_new
    
    #convert to lists 
    dates = data[:, 0].tolist()
    stages = data[:, 1].tolist()
    
    #print the start and end date of the lists 
    start_date = dt.datetime.strftime(dates[0], '%b %d, %Y')
    end_date = dt.datetime.strftime(dates[-1], '%b %d, %Y')
    print(str(len(dates)) +' entries available from ' +start_date +' to ' +end_date)
    
    #returnsDataFrame with metadata, and list of dates/stages 
    return meta, dates, stages

#get peak discharge data - output files from read_peak_streamflow.py, which formats USGS peak streamflow data
#returns pickled dict 


#def get_peak_streamflow_dates_and_vals(directory, file, n1, n2, n3):
#    f = open(os.path.join(directory, file), 'rb')
#    data = pickle.load(f)
#    x1 = data[n1]
#    x2 = data[n2]
#    x3 = data[n3]
#    
#    return x1, x2, x3



#get the intersection of two lists 
def intersection(lst1, lst2): 
    # Use of hybrid method 
    temp = set(lst2) 
    lst3 = [value for value in lst1 if value in temp] 
    return lst3 

#for a list of date objects 
def remove_nlin_inc(dates):
    deltas = []
    for i in range(len(dates) - 1):
        deltas.append((dates[i+1] - dates[i]).total_seconds())
    mode = statistics.mode(deltas)
    return deltas, mode

def get_flood_stages(directory, file):
    x = pd.read_excel(os.path.join(directory, file))
    
    a = x.loc[0, 'Flood Stage (ft)']
    h = x.loc[1, 'Flood Stage (ft)']
    v = x.loc[2, 'Flood Stage (ft)']
    return a, h, v

# for a list of flood values with respect to time, return indices of events that exceed max stage
    #takes list of dates, list of stages, and flood stage value 
def find_flood_events(dates, stages, flood_stage):
    swing = (np.max(stages) - np.min(stages)) * 0
    thresh = flood_stage - swing
    
    new_dates = []
    new_stages = []
    for i in range(len(stages)):
        if stages[i] > thresh :
            new_dates.append(dates[i])
            new_stages.append(stages[i])
            
    return new_dates, new_stages 

#input : dates and stages as list/array for one location
#        num_stdev = number of stdevs above the mean to qualify as high rate of change
def high_first_derivative(dates, stages, num_stdev):
    x = np.diff(stages)
    x[x < 0] = 0 
    mean = np.mean(x)
    std = np.std(x)
    limit = mean + num_stdev * std 
    
    #return a list of dates and corresponding stages where data points exceed "limit"
    dates_new = []
    stages_new = []
    
    for i in range(len(dates)-1):
        if x[i] > limit:
            dates_new.append(dates[i])
            stages_new.append(stages[i])
    return dates_new, stages_new 

#get USGS data
def get_streamflow_data(directory, file_names, var_names):
#    directory = r'C:\Users\bydd1\Documents\Research\Data\river data\USGS'
#
#    file_a = r'hermann_peak_discharges.xlsx'
#    file_h = r'louisville_peak_discharges.xlsx'
#    file_v = r'vicksburg_peak_discharges.xlsx'
#    
#    files = [file_a, file_h, file_v]
#    names = ['hermann', 'louisville', 'vicksburg']
    data = []
    
    for f in file_names:
        x = pd.read_excel(os.path.join(directory, f))
        dates = x[73:]
        dates = dates[x.columns[2]]
    #    dates = np.asarray(dates)
        new_dates = []
        for d in dates:
            if type(d) != str:
                new_dates.append(d)
        data.append(new_dates)
            
    dictionary = {var_names[0]:data[0],
                  var_names[1]:data[0],
                  var_names[2]:data[2]}
    
    return dictionary 

    
    

    
    

    
    
    
    
    