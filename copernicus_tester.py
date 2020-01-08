# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 15:11:45 2020
Pull Copernicus data from 
https://cds.climate.copernicus.eu/cdsapp#!/dataset/10.24381/cds.a4fdd6b9?tab=overview

Calculate 
    1. average of mean annual flow (per pixel) 
    2. average of peak annual flow (maximum per year, average maximum)
    3. average of minimum annual flow (min per year, average) 

@author: bydd1
"""
from netCDF4 import Dataset
import os 
import numpy as np 
import env_methods as em 
import vis_methods as vm 

directory = r'C:\Users\bydd1\Documents\Research\Data\GFAS Data (Copernicus)\dec1_tarr'
filename = r'CEMS_ECMWF_dis24_19791201_glofas_v2.1.nc'

path = os.path.join(directory, filename)

dataset = Dataset(path, 'r', format = 'NETCDF4')

lat = dataset['lat'][:].data
lon = dataset['lon'][:].data
time = dataset['time'][:].data
dis = dataset['dis24'][:,:,:].data

lat_bounds = [45, 28]
lon_bounds = [-95, -83]

dis_new, lat_new, lon_new = em.subset_data_one(dis, lat, lon, time, lat_bounds, 
                                               lon_bounds, normalize = False)
dis_new[dis_new < 40] = np.nan
dis_new[dis_new == 1e+20 ] = np.nan

fig = vm.single_mesh_copernicus(dis_new[0, :, :], lat_new, lon_new, 0, 
                                'December 1, 1970 discharges above 10 m^3/s')

