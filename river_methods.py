# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 23:35:00 2019
Methods used to import, format, and display USACE river stage data
@author: bydd1
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import statistics
import datetime
import pprint, pickle 

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
def get_peak_streamflow_dates(directory, file, n1, n2, n3):
    f = open(os.path.join(directory, file), 'rb')
    data = pickle.load(f)
    x1 = data[n1]
    x2 = data[n2]
    x3 = data[n3]
    
    return x1, x2, x3

def get_peak_streamflow_dates_and_vals(directory, file, n1, n2, n3):
    f = open(os.path.join(directory, file), 'rb')
    data = pickle.load(f)
    x1 = data[n1]
    x2 = data[n2]
    x3 = data[n3]
    
    return x1, x2, x3



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

    
#takes a list of stages/dates and cuts it down to only dates within dates_to_get
#def return_stages_for_dates(stages, dates, dates_to_get)
    

#__________________________VISUALIZATIONS______________________________________
    
#plot river data w.r.t time
def plot_river_data(dates, stages, start_index, stop_index, fnum):
    
    print('Figure ' + str(fnum) +': stages w.r.t time, ' +str(len(dates)) +' data points.')
    fig = plt.figure(fnum)
    fig.clear()
    plt.plot(dates[start_index:stop_index], stages[start_index:stop_index], '.')
    
    #Make nice strings to print start and stop dates - thanks strftime
    sd = dt.datetime.strftime(dates[start_index],'%b %d, %Y')
    ed = dt.datetime.strftime(dates[stop_index], '%b %d, %Y')
    plt.title('river stage data from ' +sd +' to ' +ed)
    plt.xticks(rotation = 'vertical')
    plt.ylabel('stage [ft]')
    plt.xlabel('date')
    
def plot_two_river_datasets(dates1, dates2, stages1, stages2, y_intercept, fnum):
    fig = plt.figure(fnum)
    print('Figure ' +str(fnum) +': two stage(date) datasets plotted.')
    fig.clear()
    plt.plot(dates1, stages1, '.')
    plt.plot(dates2, stages2, '.')
    plt.xlabel('dates')
    plt.ylabel('stages')
    plt.axhline(y_intercept, c = 'red')
    plt.title('Helena : stages with high first time derivative, and stages above flood level')

def plot_first_derivative(dates, stages, fnum):
    print('Figure ' +str(fnum) + ': first derivative of stage w.r.t time.')
    x = np.diff(stages)
    x[x < 0] = 0 
    print('min = ' +str(min(x)) + ' and max = ' + str(max(x)))
    mean = np.mean(x)
    std = np.std(x)
    limit = mean + 7 * std 
    fig = plt.figure(fnum)
    fig.clear()
    plt.plot(dates.copy()[:-1], x)
    plt.axhline(limit, c = 'red')
    plt.title('first derivative of stage w.r.t time')
    plt.xlabel('date')
    plt.ylabel('stage delta (ft/day)')
    
    #return a list of dates and corresponding stages where data points exceed "limit"
    dates_new = []
    stages_new = []
    
    for i in range(len(dates)-1):
        if x[i] > limit:
            dates_new.append(dates[i])
            stages_new.append(stages[i])
    
    print('Figure ' + str(fnum + 1) + ': all dates where stage exceeds ' + str(limit))
    fig2 = plt.figure(fnum + 1)
    fig2.clear()
    plt.plot(dates_new, stages_new, '.')
    plt.xlabel('date')
    plt.ylabel('stage')
    plt.title('stage data for d(stage)/d(time) > limit')
    return dates_new, stages_new 


#for all 3 locations, plot when they exceed the specified stage 
def plot_river_exceedences(a_ext_dates, a_ext_stages, h_ext_dates, h_ext_stages, 
                           v_ext_dates, v_ext_stages, fnum):
    print('Figure ' + str(fnum) + ': river exceedences for all 3 locations.')
    fig = plt.figure(fnum)
    fig.clear()
    plt.subplot(3, 1, 1)
    plt.plot(a_ext_dates, a_ext_stages, '.')
    plt.title('Arkansas City Exceedence Dates')
    plt.ylabel('stage (ft)')
    plt.subplot(3, 1, 2)
    plt.plot(h_ext_dates, h_ext_stages, '.')
    plt.title('Helena Exceedence Dates')
    plt.ylabel('stage (ft)')
    plt.subplot(3, 1, 3)
    plt.plot(v_ext_dates, v_ext_stages, '.')
    plt.title('Vicksburg Exceedence Dates')
    plt.ylabel('stage (ft)')
    
    
#for two subsets of an array of dates, show what parts of the original dataset are in each subset
def date_comparison(dates, sub1, sub2, fnum):
    print('Figure ' +str(fnum) + ': date comparison for subsets')
    x1 = []
    for date in sub1:
        x1.append(dates.index(date))
    
    x2 = []
    for date in sub2:
        x2.append(dates.index(date))
    
    fig = plt.figure(fnum)
    fig.clear()
    x0 = np.arange(0, len(dates))
    plt.plot(x0, dates, color = 'mediumaquamarine', alpha = 0.5, linewidth = 10)
    plt.plot(x1, [dates[x - 1000] for x in x1], 'r.', markersize = 20, alpha = 0.3)
    plt.plot(x2, [dates[x - 3000] for x in x2], 'b.', markersize = 20, alpha = 0.3)
    plt.xlabel('index')
    plt.ylabel('time')
    plt.title('comparison of dates present in flood datasets for Helena')
    plt.legend(['all avaliable data', 'dates where stage exceeds', 'dates with high first derivative'])
    
    
#for THREE SUBSETS - do the same thing as date_comparison but now we're going to look at the USACE dates as well 

def date_comparison_3_dates(dates, sub1, sub2, sub3, fnum):
    print('Figure ' +str(fnum) + ': date comparison for 3 subsets')
    x1 = []
    for date in sub1:
        x1.append(dates.index(date))
    
    x2 = []
    for date in sub2:
        x2.append(dates.index(date))
        
    x3 = []
    for date in sub3:
        diff = np.abs(np.subtract(dates, date)).tolist()
        ind = diff.index(min(diff))
        x3.append(ind)
        
    
    fig = plt.figure(fnum)
    fig.clear()
    x0 = np.arange(0, len(dates))
    plt.plot(x0, dates, color = 'mediumaquamarine', alpha = 0.5, linewidth = 10)
    plt.plot(x1, [dates[x - 1000] for x in x1], 'r.', markersize = 20, alpha = 0.3)
    plt.plot(x2, [dates[x - 3000] for x in x2], 'b.', markersize = 20, alpha = 0.3)
    plt.plot(x3, [dates[x - 5000] for x in x3], 'g.', markersize = 20, alpha = 0.3)
    plt.xlabel('index')
    plt.ylabel('time')
    plt.title('comparison of dates present in flood datasets for Helena')
    plt.legend(['all avaliable data', 'dates where stage exceeds', 'dates with high first derivative', 'dates from USGS'])
    
    
    
    
    