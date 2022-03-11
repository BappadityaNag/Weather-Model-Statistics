#! /usr/bin/python3

## Ranked Probability Score for Seasonal Forecasts
''' rps = 1/(M-1) sum( sum(p)-sum(o) )^2
'''
import numpy as np
import matplotlib.pyplot as plt

filein = open("ens_prate_IC05.txt","r+")
fileout = open("prob_model_IC05.txt","w+")

#######################################################################
# Read the Data
#######################################################################
header = filein.readline()
# pstr = filein1.read().split()
years = []
mod_r = []
for line in filein:
    # use a list comprehension to build your array on the fly
    array = line.split('   ')
    # print array

    new_array = []
    for i in range(1,len(array)):
       new_array.append(float(array[i]))
    #After all elements are added to an array, add array to result
    mod_r.append(new_array)
    years.append(int(array[0]))

mod_r = [[elem if elem >= 0.0 else np.nan for elem in arr] for arr in mod_r]

print ("\nThe predicted values are :\n",mod_r)
print ("\nYears taken :\n", years)

mean_mod_r = np.nanmean(mod_r, axis=1)
std_mod_r = np.nanstd(mod_r, axis=1)
mean_ensmean_mod_r = np.mean(mean_mod_r, axis=0)
std_ensmean_mod_r = np.std(mean_mod_r, axis=0)

print ("\nEnsemble Mean Model Rainfall :\n",mean_mod_r)
print ("\nLPA of Ens. Mean Model Rainfall :",mean_ensmean_mod_r)
print ("\nStd. Dev. of Ens. Mean Model Rainfall :",std_ensmean_mod_r)

print("\nNumber of Years :",len(years))
print("\nNumber of Ensemble Mean Model Rainfall :",len(mean_mod_r))
print("\nNumber of Ensemble Std. Dev. of Model Rainfall :",len(std_mod_r))

fileout.write("Year    BelowAvg    Normal    AboveAvg\n")
for yr in range(len(years)) :
    belavg, abvavg, norm, total = 0, 0, 0, 0
    for ens in range(10) :
        if (~np.isnan(mod_r[yr][ens])) :
            if (mod_r[yr][ens] < mean_ensmean_mod_r-std_ensmean_mod_r) :
                belavg += 1
            else :
                if (mod_r[yr][ens] > mean_ensmean_mod_r+std_ensmean_mod_r) :
                    abvavg += 1
                else :
                    norm += 1
            total += 1
    fileout.writelines([str(years[yr]), "    ", str(belavg/total),  "    ", str(norm/total), "    ",  str(abvavg/total), "\n"])
             
#######################################################################
# Omitting NaN values in python
#######################################################################

# for index, item in enumerate(mod_r):
# 	if item > 50.0:
# 		mod_r[index] = np.nan

# mod_r = [np.nan if value == 100.0 else value for value in mod_r]
# np.place(mod_r, mod_r == 100.0, 0.0)
# mod_r[mod_r >= 50 ] = np.nan
# np.where(mod_r>50, np.nan, mod_r)
# mod_r = np.replace(mod_r, 100.0, nan)

# arr = np.arange(6).reshape(2, 3)
# arr = [[1, 2], [2, 3]]
# print(arr)
# replace 0 with -10
# np.place(arr, arr == 0, -10)
# print(arr)

#######################################################################

filein.close()
fileout.close()
exit()
