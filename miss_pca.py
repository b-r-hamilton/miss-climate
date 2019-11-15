# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 16:38:47 2019
Completes PCA analysis on ncep/ncar dataset 
pca code stolen from https://plot.ly/python/v3/ipython-notebooks/principal-component-analysis/
@author: bydd1
"""

#custom libraries
import env_methods as em
import river_methods as rm 
import vis_methods as vm 

#python libraries 
import datetime as dt
import numpy as np
from sklearn import decomposition
import os 

folder = r'C:\Users\bydd1\Documents\Research\PCA Images'

num_months = 6 #number of months prior to peak streamflow date to get data for 
top_days = 10 #produce images for 10 dates with highest discharge 

#locations of river data 
river_folder = r'C:\Users\bydd1\Documents\Research\Data\river data\USGS'
river_files = ['hermann_peak_discharges.xlsx', 'louisville_peak_discharges.xlsx', 'vicksburg_peak_discharges.xlsx']

#location of NCEP-NCAR Reanalysis 3 data - air temp (@ 2m, corollary for SST), precip, and SLP  
ncep_folder = r'C:\Users\bydd1\Documents\Research\Data\NCEP NCAR Reanalysis 3\Monthly Means'
ncep_files = ['air.2m.mon.mean.nc','prate.mon.mean.nc', 'pres.sfc.mon.mean.nc']
ncep_ltm = ['air.2m.mon.ltm.nc','prate.mon.ltm.nc', 'pres.sfc.mon.ltm.nc']

#netCDF variable names - in order of file names above!
var_names = ['air', 'prate', 'pres']

#get 3rd reanalysis data 
time, lat, lon, air = em.get_3rd_reanalysis(ncep_folder, ncep_files[0], var_names[0]) #time, lat, lon equivalent between datasets
_, _, _, prate = em.get_3rd_reanalysis(ncep_folder, ncep_files[1], var_names[1])
_, _, _, pres = em.get_3rd_reanalysis(ncep_folder, ncep_files[2], var_names[2])

#bounding box for ENSO region 
lat_bounds_enso = [-25, 25]
lon_bounds_enso = [181 + 50 , 181 + 110]

#bounding box for G.o.M region 
lat_bounds_gom = [16, 31]
lon_bounds_gom = [180 + 78, 180 + 100]

#full world boundaries 
lat_bounds_full = [min(lat), max(lat)]
lon_bounds_full = [min(lon), max(lon)]

#ROIS 
regions = ['enso', 'gom', 'full']
lat_bounds = [lat_bounds_enso, lat_bounds_gom, lat_bounds_full]
lon_bounds = [lon_bounds_enso, lon_bounds_gom, lon_bounds_full]
#regions = ['gom', 'enso']
#lat_bounds = [lat_bounds_gom, lat_bounds_enso]
#lon_bounds = [lon_bounds_gom, lon_bounds_enso]
 
#get streamflow data - returns as dictionary, then extract important data (dates + discharges)
locations = ['hermann', 'louisville', 'vicksburg']
dictionary = rm.get_streamflow_data(river_folder, river_files, locations)
dis_dates = []
dis = []

for i in range(len(locations)): #iterate over locations, get peak streamflow dates and discharges
    dis_dates.append(dictionary[locations[i] + '_dates'])
    dis.append(dictionary[locations[i] + '_discharges'])

time_greg = [(x - dt.datetime(1800, 1, 1, 0, 0, 0)).days for x in time] #convert time to gregorian digits for easy math 

#%%

pca_frameworks = []

for geospatial_subset in range(len(regions)):

    lb1 = lat_bounds[geospatial_subset]
    lb2 = lon_bounds[geospatial_subset]
    air_sub, pres_sub, prate_sub, lat_sub, lon_sub = em.subset_data(air, pres, prate, lat, lon, time, lb1, lb2)
    
    tuple_list = em.generate_tuples(lat_sub, lon_sub)
    
    lat_bins = [lat_sub[int(len(lat_sub) / 5 * x)] for x in range(5)]
    lon_bins = [lon_sub[int(len(lon_sub) / 5 * x)] for x in range(5)]
    
    location_map = []
    location_map_tuples = em.generate_tuples(np.arange(0,5).tolist(), np.arange(0,5).tolist())
    for tup in tuple_list:
        x = em.find_closest_val(tup[0], lat_bins)
        y = em.find_closest_val(tup[1], lon_bins)
        location_map.append(location_map_tuples.index((x,y)))
    
    for i in range(len(locations)): #iterate through each locations 
        dates = dis_dates[i] #get dates for that location
        discharges = dis[i] #get discharges for that location 
        z = sorted(zip(discharges, dates)) #zip, sort by highest discharges 
        z = z[:top_days] #get top x discharge dates 
        discharges, dates = zip(*(z)) #unzip to original variables 
        
        pca_framework = np.zeros((len(tuple_list), top_days))
        
        for d in dates: #iterate through top 10 dates 
            
            month = d.month 
            year = d.year
            
            #find time index within NCEP-NCAR dataset - convert to days since 1/1/1800, subtract from time_greg
            time_index = em.find_closest_val((d - dt.datetime(1800, 1, 1, 0, 0, 0)).days, time_greg)
            
            #find the mean of the x months before the date 
            frame1 = np.mean(air_sub[time_index - num_months :time_index, :, :], axis = 0)
            frame2 = np.mean(pres_sub[time_index - num_months :time_index, :, :], axis = 0)
            frame3 = np.mean(prate_sub[time_index - num_months :time_index, :, :], axis = 0)
            

            
            fname = str(i) + '_' + regions[geospatial_subset] + '_' + str(dates.index(d)) + '_'+ 'tempmesh' + '.png'
            subfolder = os.path.join(folder, 'meshedimages')
            path = os.path.join(subfolder, fname)
            
            title = 'temp' + locations[i] + '_' + str(d)
            
            vm.single_mesh(frame1, lat_sub, lon_sub, path, title, lat_bins, lon_bins)
                
    
            for j in range(np.shape(frame1)[0]):
                for k in range(np.shape(frame1)[1]):
                    tup = (lat_sub[j], lon_sub[k])
                    index1 = tuple_list.index(tup)
                    index2 = dates.index(d)
                    
                    pca_framework[index1, index2] = frame1[j, k]
                        
#        pca = decomposition.PCA(n_components = 2)
#        projected = pca.fit_transform(pca_framework)
#        
#        fname = str(i) + '_' + regions[geospatial_subset] + '2comp_PCA' + '.png'
#        path = os.path.join(folder, fname)
#        title = regions[geospatial_subset] + '_' + locations[i]
#        vm.biplot(projected, location_map, title, path, pca.explained_variance_ratio_)
#    
        mean_vec = np.mean(pca_framework, axis = 0)
        cov_mat = np.cov(pca_framework.T)
        eig_vals, eig_vecs =np.linalg.eig(cov_mat)
        
#        for ev in eig_vecs:
#            np.testing.assert_array_almost_equal(1.0, np.linalg.norm(ev))
#            print('gucci')
        
        # Make a list of (eigenvalue, eigenvector) tuples
        eig_pairs = [(np.abs(eig_vals[i]), eig_vecs[:,i]) for i in range(len(eig_vals))]
        
        # Sort the (eigenvalue, eigenvector) tuples from high to low
        eig_pairs.sort()
        eig_pairs.reverse()
        
        # Visually confirm that the list is correctly sorted by decreasing eigenvalues
#        print('Eigenvalues in descending order:')
#        for ep in eig_pairs:
#            print(ep[0])
        
        tot = sum(eig_vals)
        var_exp = [(i_sorted / tot)*100 for i_sorted in sorted(eig_vals, reverse=True)]
        cum_var_exp = np.cumsum(var_exp)
        
        fname = locations[i] + '_' + regions[geospatial_subset] + '_' + 'scree' + '.png'
        subfolder = os.path.join(folder, 'screeplots')
        path = os.path.join(subfolder, fname)
        title = locations[i] + '_' + regions[geospatial_subset]
        vm.scree(cum_var_exp, path, title)
        
        matrix_w = np.hstack((eig_pairs[0][1].reshape(10,1), eig_pairs[1][1].reshape(10,1)))
        Y = pca_framework.dot(matrix_w)
        fname = locations[i] + '_' + regions[geospatial_subset] + '2comp_PCA' + '.png'
        path = os.path.join(folder, fname)
        title = regions[geospatial_subset] + '_' + locations[i]
        vm.biplot(Y, location_map, title, path)
        
        bipx_bin = [(max(Y[:,0]) - min(Y[:,0])) * val / 5 + min(Y[:,0]) for val in np.arange(0, 5)]
        bipy_bin = [(max(Y[:,1]) - min(Y[:,1])) * val / 5 + min(Y[:,1]) for val in np.arange(0, 5)]
        
        subfolder = os.path.join(folder, 'pcasim')
        fname = locations[i] + '_' + regions[geospatial_subset] + '_' + 'pcasim' + '.png'
        path = os.path.join(subfolder, fname)
        title = 'pcasim' + locations[i]
        vm.plot_pcasim_reg(tuple_list, bipx_bin, bipy_bin, Y, lat_sub, lon_sub, path, title)
    
