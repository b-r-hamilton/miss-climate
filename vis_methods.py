# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 01:12:21 2019
All functions that generate data visualizations
@author: bydd1
"""
import matplotlib.pyplot as plt
import datetime as dt 
import numpy as np
import cartopy.crs as ccrs 

#from pandas.plotting import register_matplotlib_converters
#register_matplotlib_converters()

#make a movie of env var over time 
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

#plot mean and stdev image together and save 
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


def generate_3_var_img(frame1, frame2, frame3, date, path, lat, lon):
   
    fig = plt.figure(figsize = (12, 18))
    plt.suptitle(date)
    print(str(date))
    
    ax1 = plt.subplot(3,1,1, projection = ccrs.PlateCarree())
    ax1.coastlines()
    plt.title('normed temperature')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    mesh1 = plt.pcolormesh(lon, lat, frame1, cmap = 'coolwarm', vmin = -1, vmax = 1)
    plt.colorbar(mesh1)
    
    ax2 = plt.subplot(3,1,2, projection = ccrs.PlateCarree())
    ax2.coastlines()
    plt.title('normed pressure')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    mesh2 = plt.pcolormesh(lon, lat, frame2, cmap = 'coolwarm',vmin = -1, vmax = 1)
    plt.colorbar(mesh2)
    
    ax3 = plt.subplot(3,1,3, projection = ccrs.PlateCarree())
    ax3.coastlines()
    plt.title('normed precip')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    mesh3 = plt.pcolormesh(lon, lat, frame3, cmap = 'coolwarm',vmin = -1, vmax = 1)
    plt.colorbar(mesh3)
    
#    for x in [frame1, frame2, frame3]:
#        if np.nanmax(x) > 1: print('error, max = ' + str(np.nanmax(x)))
#        if np.nanmin(x) > 1: print('error, min = ' + str(np.nanmin(x)))
        
    
    if type(path) == str: plt.savefig(path)
    
    plt.close(fig)
#def generate_image_set():
    