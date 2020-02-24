# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 08:41:10 2020

@author: bydd1
"""
import pandas as pd
import matplotlib.pyplot as plt
import pickle 
import numpy as np 
import env_methods as em 
#%%
    
sin_path = r'D:\MS Sinuosity Data\MS_segments_recovered.xlsx'
dis_path = r'D:\CDS River Discharge\Pickles\compressed_ra.pickle'

df = pd.read_excel(sin_path)
dic = pickle.load(open(dis_path, "rb" ) )

lat = dic['lat'].tolist()
lon = dic['lon'].tolist()

means = []
maxs = []
mins = []

for ind in df.index:
    if ind % 1000 == 0:
        print('entry ' + str(ind))
    x = df['lat'][ind]
    y = df['lon'][ind]
    
    ind_x = em.find_closest_val(x, lat)
    ind_y = em.find_closest_val(y, lon)
    
    means.append(dic['mean_annual'][ind_x, ind_y])
    maxs.append(dic['peak_annual'][ind_x, ind_y])
    mins.append(dic['min_annual'][ind_x, ind_y])

#%%

#%%
df['mean_dis'] = means
df['min_dis'] = mins
df['max_dis'] = maxs 

# df = df.replace(-9999, np.nan)
output_excel = r'D:\MS Sinuosity Data\MS_segments_with_cop.xlsx'
df.to_excel(output_excel)


#%%

plt.figure(figsize = (5, 13))
plt.subplot(3, 1, 1)
scat1 = plt.scatter(df['lon'], df['lat'], marker='.', s=1,  
            c=df['mean_dis'], cmap=plt.cm.coolwarm)
plt.colorbar(scat1)
plt.title('Mean Discharge')

plt.subplot(3, 1, 2)
scat2 = plt.scatter(df['lon'], df['lat'], marker='.', s=1,  
            c=df['max_dis'], cmap=plt.cm.coolwarm)
plt.colorbar(scat2)
plt.title('Peak Discharge')

plt.subplot(3, 1, 3)
scat3 = plt.scatter(df['lon'], df['lat'], marker='.', s=1,  
            c=df['min_dis'], cmap=plt.cm.coolwarm)
plt.colorbar(scat3)
plt.title('Minimum Discharge')

#%%
plt.figure(figsize = (5, 10))
plt.subplot(2,1,1)
scat4 = plt.scatter(df['lon'], df['lat'], marker='.', s=1,  
            c=df['Meandwave'], cmap=plt.cm.coolwarm)
plt.colorbar(scat4)
plt.title('Meander Wavelength')

plt.subplot(2,1,2)
scat5 = plt.scatter(df['lon'], df['lat'], marker='.', s=1,  
            c=df['Sinuosity'], cmap=plt.cm.coolwarm)
plt.colorbar(scat5)
plt.title('Sinuosity')

#%%

plt.figure(figsize = (6, 11))
plt.subplot(2,1,1)
plt.plot( df['Meandwave'], df['mean_dis'],'.', alpha = 0.3)
plt.title('Mean discharge as a function of Meander Wavelength')
plt.yscale('log')
plt.xscale('log')
plt.ylabel('mean discharge')
plt.xlabel('meander wavelength')

plt.subplot(2,1,2)
plt.plot( df['Sinuosity'],df['mean_dis'], '.', alpha = 0.3)
plt.title('Mean discharge as a function of Sinuosity')
plt.yscale('log')
plt.xscale('log')
plt.ylabel('mean discharge')
plt.xlabel('sinuosity')


#%%

plt.figure(figsize = (6, 11))
plt.subplot(2,1,1)
plt.plot( df['Meandwave'], df['QWBM'],'.', alpha = 0.3)
plt.title('QWBM as a function of Meander Wavelength')
plt.yscale('log')
plt.xscale('log')
plt.ylabel('mean discharge')
plt.xlabel('meander wavelength')

plt.subplot(2,1,2)
plt.plot( df['Sinuosity'],df['QWBM'], '.', alpha = 0.3)
plt.title('QWBM as a function of Sinuosity')
plt.yscale('log')
plt.xscale('log')
plt.ylabel('mean discharge')
plt.xlabel('sinuosity')

# #%%

# plt.figure(figsize = (6, 11))
# plt.subplot(2,1,1)
# plt.plot( df['Meandwave'], df['max_dis'],'.', alpha = 0.3)
# plt.title('Max discharge as a function of Meander Wavelength')
# plt.yscale('log')
# plt.ylabel('max discharge')
# plt.xlabel('meander wavelength')

# plt.subplot(2,1,2)
# plt.plot( df['Sinuosity'],df['max_dis'], '.', alpha = 0.3)
# plt.title('Max discharge as a function of Sinuosity')
# plt.yscale('log')
# plt.ylabel('max discharge')
# plt.xlabel('sinuosity')

# #%%

# plt.figure(figsize = (6, 11))
# plt.subplot(2,1,1)
# plt.plot( df['Meandwave'], df['min_dis'],'.', alpha = 0.3)
# plt.title('Min discharge as a function of Meander Wavelength')
# plt.yscale('log')
# plt.ylabel('min discharge')
# plt.xlabel('meander wavelength')

# plt.subplot(2,1,2)
# plt.plot( df['Sinuosity'],df['min_dis'], '.', alpha = 0.3)
# plt.title('Min discharge as a function of Sinuosity')
# plt.yscale('log')
# plt.ylabel('min discharge')
# plt.xlabel('sinuosity')
