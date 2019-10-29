# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 15:31:41 2019

@author: bydd1
"""
import env_methods as em 

directory = r'C:\Users\bydd1\Documents\Research\Data\gridded environmental'
file1 = r'rhum.mon.mean.nc'
file2 = r'sst.mon.mean.nc'
time, lat, lon, var = em.get_sst_mon_mean(directory, file2, 'sst')
#just look at surface humdity
#var = var[:, 0, :, : ]
anim = em.generate_animation(time, lat, lon, var)


#%%
#directory = r'C:\Users\bydd1\Documents\Research\Data'
#file2 = r'ENSO34Index.xlsx'
#y = pd.read_excel(os.path.join(directory, file2))
#x = np.asarray(y)[:, 1:].flatten()
#plt.figure()
#
#x_axis = np.arange(0, len(x))
#plt.plot(x_axis, x)
#plt.axhline(0, color = 'red')

#def stupid():
#    import matplotlib.pyplot as plt
#    mesh = plt.pcolormesh(lon, lat, var[0, :, :], cmap = 'coolwarm')
#    cb = plt.colorbar(mesh)
#    cb.set_label('deg C')
#    plt.xlabel('longitude')
#    plt.ylabel('latitude')
#    plt.title('SST on 1850-01-01')
#    
#stupid()
#    