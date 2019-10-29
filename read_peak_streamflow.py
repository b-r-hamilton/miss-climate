# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 13:07:56 2019

@author: bydd1
"""
import os 
import pandas as pd 
import numpy as np
from datetime import datetime as dt 
import pickle 
#read peak discharge files acquired from USGS

directory = r'C:\Users\bydd1\Documents\Research\Data\river data\USGS'

file_a = r'hermann_peak_discharges.xlsx'
file_h = r'louisville_peak_discharges.xlsx'
file_v = r'vicksburg_peak_discharges.xlsx'

files = [file_a, file_h, file_v]
names = ['hermann', 'louisville', 'vicksburg']
data = []

for f in files:
    x = pd.read_excel(os.path.join(directory, f))
    dates = x[73:]
    dates = dates[x.columns[2]]
#    dates = np.asarray(dates)
    new_dates = []
    for d in dates:
        if type(d) != str:
            new_dates.append(d)
    data.append(new_dates)
        
dictionary = {names[0]:data[0],
              names[1]:data[0],
              names[2]:data[2]}

pickle_path = os.path.join(directory, 'peak_discharges_full_river.pickle')

output = open(pickle_path, 'wb')
pickle.dump(dictionary, output)
output.close()
    