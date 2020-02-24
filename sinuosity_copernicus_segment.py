# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:54:12 2020
Reduce dataset to averaged segments and perform analytics 
@author: bydd1
"""

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs 
import cartopy
import scipy.stats as stats 

def lin_regress(x, y):
    plt.figure()

    plt.title('Segment Averaged Meander Wavelength x Mean Discharge')
    plt.plot(x, y, '.', markersize = 5)
    plt.xlabel('ln(meander wavelength)')
    plt.ylabel('ln(mean discharge)')
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    
    theo_y = intercept + slope*x
    plt.plot(x, theo_y, '-', color = 'red')
    plt.text(x = 8.5, y = 0, s = 'R^2 = ' +str(r_value * r_value)[:6])
    plt.legend(['data', 'lin. reg.'])
    
#%% Get data, preliminary formating (remove rows with nan values )

file_path = r'C:\Users\bydd1\OneDrive\Documents\Research\MS Sinuosity Data\MS_segments_with_cop.xlsx'

df = pd.read_excel(file_path)

df = df.replace(-9999, np.nan)
df = df.dropna()

#%% Take Log of all sinuosity/meander wavelength and discharge variables 

df['log_sinuosity'] = np.log(df['Sinuosity'])
df['log_mw'] = np.log(df['Meandwave'])
df['log_mean_dis'] = np.log(df['mean_dis'])
df['log_min_dis'] = np.log(df['min_dis'])
df['log_max_dis'] = np.log(df['max_dis'])
df['log_QWBM'] = np.log(df['QWBM'])


#%% Average Data by segment 
unique = np.unique(df['SegmentID']) #find all unique SegmentID 
arr = []
df_new = df[0:0] #initialize dataframe 
lengths = []
for u in unique: #iterate through unique SegmentID
    x = df.loc[df['SegmentID'] == u] #find all values within original dataframe with iterated value 
    lengths.append(len(x))
    x = x.mean(axis = 0) #average along first axis 
    df_new = df_new.append(x, ignore_index = True) #append new dataframe 

df_new['vals_in_seg'] = lengths
go_path = r'C:\Users\bydd1\OneDrive\Documents\Research\MS Sinuosity Data\MS_segments_averaged_by_seg.xlsx'
df_new.to_excel(go_path)

#%% Plot meander wavelength x mean_dis 

x = df_new['log_mw']
y = df_new['log_mean_dis']
lin_regress(x, y)

#%% Complete the linear regression for all points with more than 30 values in the segment 
len_thresh = [30, 10000]

df_len_red = df_new[df_new['vals_in_seg'] > len_thresh[0]]
df_len_red = df_len_red[df_len_red['vals_in_seg'] < len_thresh[1]]
x = df_len_red['log_mw']
y = df_len_red['log_mean_dis']
lin_regress(x, y)

#%% Complete the linear regression for all points with low slope 

slope_thresh = [0, 150]
df_slope_thresh = df_new[df_new['Slope'] > len_thresh[0]]
df_slope_thresh = df_new[df_new['Slope'] < len_thresh[1]]
x = df_slope_thresh['log_mw']
y = df_slope_thresh['log_mean_dis']
lin_regress(x,y)