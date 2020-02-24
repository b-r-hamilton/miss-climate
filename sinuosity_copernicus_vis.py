# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 08:47:20 2020
Highlight sections of the Mississippi with discharge/meander wavelength
within specified range

@author: bydd1
"""
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs 
import cartopy

#%%

file_path = r'C:\Users\bydd1\OneDrive\Documents\Research\MS Sinuosity Data\MS_segments_with_cop.xlsx'

df = pd.read_excel(file_path)

df = df.replace(-9999, np.nan)
df = df.dropna()

#%%

df['log_sinuosity'] = np.log(df['Sinuosity'])
df['log_mw'] = np.log(df['Meandwave'])
df['log_mean_dis'] = np.log(df['mean_dis'])
df['log_min_dis'] = np.log(df['min_dis'])
df['log_max_dis'] = np.log(df['max_dis'])
df['log_QWBM'] = np.log(df['QWBM'])


#%%
#Overall Maps 

for var in ['log_mean_dis', 'QWBM', 'log_mw']:

    plt.figure()
    ax = plt.subplot(projection = ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.LAND, edgecolor='black')
    ax.add_feature(cartopy.feature.LAKES, edgecolor='black')
    scat = plt.scatter(df['lon'], df['lat'], c = df[var], s = 1, cmap = 'coolwarm')
    plt.title(var +' log scale')
    plt.colorbar(scat)

#%% Meander Wavelength Maps 

ranges = [5, 6, 7, 8 , 9 , 10]

for i in range(len(ranges)  - 1):
    
    mw_arr = df['log_mw']
    mw_arr = np.asarray(mw_arr)
    #reduce array to values within current range 
    mw_arr_ran = mw_arr[mw_arr > ranges[i]]
    mw_arr_ran = mw_arr_ran[mw_arr_ran < ranges[i + 1]]
    mw_arr_ran = mw_arr_ran.tolist()
    mw_arr = mw_arr.tolist()
    
    indices = []
    for val in mw_arr_ran:
        indices.append(mw_arr.index(val))
    
    plt.figure()
    ax = plt.subplot(projection = ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cartopy.feature.OCEAN)
    ax.add_feature(cartopy.feature.LAND, edgecolor='black')
    ax.add_feature(cartopy.feature.LAKES, edgecolor='black')
    plt.scatter(df['lon'], df['lat'], color = 'red', s = 5)
    plt.scatter(df['lon'][indices], df['lat'][indices], color = 'blue', s = 4)
    plt.title('Meander Wavelength in Log Range' + str([ranges[i], ranges[i+1]]))

#%% Non Logged Meander Wavelength Maps 
    
# mw_arr = df['Meandwave']
# mw_arr = np.asarray(mw_arr)

# ranges = [min(mw_arr) + i * (max(mw_arr) - min(mw_arr)) / 10 for i in range(10)]

# for i in range(len(ranges)  - 1):
    
#     #reduce array to values within current range 
#     mw_arr_ran = mw_arr[mw_arr > ranges[i]]
#     mw_arr_ran = mw_arr_ran[mw_arr_ran < ranges[i + 1]]
#     mw_arr_ran = mw_arr_ran.tolist()
#     mw_arr = mw_arr.tolist()
    
    
#     indices = []
#     for val in mw_arr_ran:
#         indices.append(mw_arr.index(val))
    
#     plt.figure()
#     ax = plt.subplot(projection = ccrs.PlateCarree())
#     ax.coastlines()
#     ax.add_feature(cartopy.feature.OCEAN)
#     ax.add_feature(cartopy.feature.LAND, edgecolor='black')
#     ax.add_feature(cartopy.feature.LAKES, edgecolor='black')
#     plt.scatter(df['lon'], df['lat'], color = 'red', s = 5)
#     plt.scatter(df['lon'][indices], df['lat'][indices], color = 'blue', s = 4)
    plt.title('Meander Wavelength in Log Range' + str([ranges[i], ranges[i+1]]))


#%%
    
plt.figure()
x_org_arr = np.asarray(df['SegmentID'])
x_org_list = x_org_arr.tolist()
x = x_org_arr[x_org_arr == 14]

indices = []
for i in x:
    indices.append(x_org_list.index(i))
    
scat = plt.scatter(df['lon'], df['lat'], color ='blue', alpha = 0.5, s = 1)
plt.scatter(df['lon'][indices], df['lat'][indices], color ='red')

plt.colorbar(scat)


#%%
unique = np.unique(df['SegmentID'])
arr = []
df_new = df[0:0]
for u in unique:
    x = df.loc[df['SegmentID'] == u]
    x = x.mean(axis = 0)
    df_new = df_new.append(x, ignore_index = True)

#%%
plt.figure()
plt.scatter(df_new['lon'], df_new['lat'], s = 20, c = df_new['log_mw'], cmap = 'coolwarm')

#%%
plt.figure()
plt.scatter(df_new['log_mw'], df_new['log_mean_dis'], '.')
