# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:05:24 2020

@author: bydd1
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
import scipy.stats as stats
from sklearn.linear_model import LinearRegression

#%%
def closed_form_lin_reg(x, y):
    """
    computes the closed form linear regression given
    :param x: a vector/matrix of input features
    :param y: a vector of of expected outputs
    :return:
    """
    x_t_x = np.inner(x, x)
    x_t_y = np.inner(x, y)
    try:
        theta = np.linalg.inv(x_t_x) * x_t_y
    except np.linalg.LinAlgError:
        # if x_t_x is a constant, take simple inverse
        theta = (1 / x_t_x) * x_t_y
    print("Theta = {}".format(theta))

#%%
#https://stackoverflow.com/questions/893657/how-do-i-calculate-r-squared-using-python-and-numpy    
# Polynomial Regression
def polyfit(x, y, degree):
    results = {}

    coeffs = np.polyfit(x, y, degree)

     # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = np.poly1d(coeffs)
    print(p)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = ssreg / sstot

    return results
    
#%%
file_path = r'C:\Users\bydd1\OneDrive\Documents\Research\MS Sinuosity Data\MS_segments_with_cop.xlsx'

df = pd.read_excel(file_path)

df = df.replace(-9999, np.nan)

#%%

df['log_sinuosity'] = np.log(df['Sinuosity'])
df['log_mw'] = np.log(df['Meandwave'])
df['log_mean_dis'] = np.log(df['mean_dis'])
df['log_min_dis'] = np.log(df['min_dis'])
df['log_max_dis'] = np.log(df['max_dis'])
df['log_QWBM'] = np.log(df['QWBM'])

#%%
df = df.dropna()
x = df['log_mw']
y = df['log_mean_dis']

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
plt.plot(x, y, '.', markersize = 2)
theo_y = intercept + slope*x
plt.plot(x, theo_y, '-', color = 'red')
plt.xlabel('ln(meander wavelength)')
plt.ylabel('ln(discharge')
plt.title('All data (no preprocessing)')

spm = stats.spearmanr(x, y)
prs = stats.pearsonr(x, y)
theta = closed_form_lin_reg(x, y)

#%%
horz_steps = 1000
vals = np.arange(min(x), max(x), step = (max(x) - min(x)) / horz_steps)
avg_y = []

x = x.tolist()
y = y.tolist()
for b in range(horz_steps-1):
    temp_y = []
    for ind in range(len(x)): 
        if vals[b] < x[ind] and vals[b+1] > x[ind]:
            temp_y.append(y[ind])
    avg_y.append(np.mean(temp_y))

#%%  
plt.figure()
plt.plot(x, y, '.', markersize = 5, alpha = 0.2)
plt.plot(vals[:-1], avg_y, '.', markersize = 5)
plt.xlabel('ln(meander wavelength)')
plt.ylabel('ln(discharge)')
plt.title('raw data vs. binned averaged data')
plt.legend(['raw', 'binned'])


x_d = vals[:-1]
y_d = avg_y
d = {'x_d':x_d, 'y_d':y_d}
df2 = pd.DataFrame(d)
df2 = df2.dropna()

slope, intercept, r_value, p_value, std_err = stats.linregress(df2['x_d'], df2['y_d'])
slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(x, y)
theo_y = intercept + slope*x_d
theo_y2 = intercept1 + slope1*x
plt.plot(x_d, theo_y, '-', color = 'red')
plt.plot(x, theo_y2, '-', color = 'green')


# #%%
# x = df['log_QWBM']
# y = df['log_mw']
# slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
# theo_y = x * slope + intercept
# plt.figure()
# plt.plot(x,y,'.')
# plt.plot(x, theo_y, '-', color = 'red')

# plt.figure()
# given_x = df['QWBM']
# given_y = df['Meandwave']
# plt.plot(given_x, given_y,'.')
# x_axis = np.arange(min(given_x), max(given_x), step = 10)
# a = np.exp(intercept)
# b = slope 
# theo_y_axis = a * x_axis ** b
# plt.plot(x_axis, theo_y_axis)


#%%
rand_500 = np.random.choice(df.index.tolist(), 500)
x_reduced = x[rand_500]
y_reduced = y[rand_500]

plt.figure()
plt.plot(x_reduced, y_reduced, '.', markersize = 2)
slope, intercept, r_value, p_value, std_err = stats.linregress(x_reduced,y_reduced)


theo_y = intercept + slope*x_reduced
plt.plot(x_reduced, theo_y, '-', color = 'red')
plt.xlabel('ln(meander wavelength)')
plt.ylabel('ln(discharge')
plt.title('500 Random Points using Mean Discharge from GFAS')