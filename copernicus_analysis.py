# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 14:17:24 2020
Visualizes river discharge data
@author: THALWEG
"""
import pickle
import vis_methods as vm 
import numpy as np 
import os

#%%

save_path =r'D:\CDS River Discharge\Pickles\river_analytics.pickle'
dictionary = pickle.load( open( save_path, "rb" ) )

#%%
mean_annual = dictionary['mean_annual']
peak_annual = dictionary['peak_annual']
min_annual = dictionary['min_annual']
lat = dictionary['lat']
lon = dictionary['lon']
year = dictionary['year']
#%%
# pic_save = r'path'

# x_save = os.path.join(pic_save, 'av.png')
# x = np.mean(mean_annual, axis = 0)
# x[x < 40] = np.nan
# vm.single_mesh_copernicus(x, lat, lon, 0, 'Average River Discharge')
# y_save = os.path.join(pic_save, 'max.png')
# y = np.max(peak_annual, axis = 0)
# y[y < 100] = np.nan
# vm.single_mesh_copernicus(y, lat, lon, 0, 'Peak River Discharge')
# z_save = os.path.join(pic_save, 'min.png')
# z = np.min(min_annual, axis = 0)
# z[z < 5] = np.nan
# vm.single_mesh_copernicus(z, lat, lon, 0, 'Min River Discharge')

#%%

new_file = r'D:\CDS River Discharge\Pickles\compressed_ra.pickle'

dictionary = {'mean_annual' : np.mean(mean_annual, axis = 0),
              'peak_annual' : np.mean(peak_annual, axis = 0),
              'min_annual' : np.mean(min_annual, axis = 0),
              'year' : year,
              'lat' : lat,
              'lon' : lon}

pickle.dump(dictionary, open(new_file, "wb" ) )