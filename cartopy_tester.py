# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 21:55:42 2019

@author: bydd1
"""
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

import env_methods as em 

ncep_folder = r'C:\Users\bydd1\Documents\Research\Data\NCEP NCAR Reanalysis 3\Monthly Means'
ncep_files = ['air.2m.mon.mean.nc','prate.mon.mean.nc', 'pres.sfc.mon.mean.nc']
ncep_ltm = ['air.2m.mon.ltm.nc','prate.mon.ltm.nc', 'pres.sfc.mon.ltm.nc']

var_names = ['air', 'prate', 'pres']

time, lat, lon, air = em.get_3rd_reanalysis(ncep_folder, ncep_files[0], var_names[0]) #time, lat, lon equivalent between datasets

#%%

lon_left = 30
lon_right = 70
lat_bottom = 40
lat_top = 100

lon_new = lon[lon_left:lon_right]
lat_new = lat[lat_bottom:lat_top]
air_new = air[:, lat_bottom:lat_top, lon_left:lon_right]
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()

mesh = plt.pcolormesh(lon_new, lat_new, air_new[0, :, :], cmap = 'coolwarm')
plt.colorbar(mesh)
plt.show()

