#! /usr/bin/python3

## Ranked Probability Score for Seasonal Forecasts
''' rps = 1/(M-1) sum( sum(p)-sum(o) )^2
'''
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt

filein1 = open("prob_model.txt","r+")
filein2 = open("prob_obvs.txt","r+")
filein3 = open("obvs.txt","r+")

ncat = 3

#######################################################################
# Read the Data
#######################################################################

# pstr = filein1.read().split()
years = []

pred_mod = []
header = filein1.readline()
for line in filein1:
    array = line.split()
    new_array = []
    for i in range(1,len(array)):
       new_array.append(float(array[i]))
    #After all elements are added to an array, add array to result
    pred_mod.append(new_array)
    years.append(int(array[0]))
print ("\nYears :\n",years)
print ("\nThe predicted model values are :\n",pred_mod)

pred_obvs = []
header = filein2.readline()
for line in filein2:
    array = line.split()
    new_array = []
    for i in range(1,len(array)):
       new_array.append(float(array[i]))
    pred_obvs.append(new_array)
    years.append(int(array[0]))
print ("\nThe predicted climatological values are :\n",pred_obvs)

obvs = []
header = filein3.readline()
for line in filein3:
    array = line.split()
    new_array = []
    for i in range(1,len(array)):
       new_array.append(float(array[i]))
    obvs.append(new_array)
print ("\nThe observed values are :\n",obvs)

#######################################################################
# Calculation of RPSS
#######################################################################

for k in range(len(pred_mod)) :
    list=pred_mod[k]
    new_list=[]
    j=0
    for i in range(len(pred_mod[k])) :
        j+=list[i]
        new_list.append(j)
    pred_mod[k]=new_list
print ("\nThe Cumulative Predicted Model Values are :\n",pred_mod)

for k in range(len(pred_obvs)) :
    list=pred_obvs[k]
    new_list=[]
    j=0
    for i in range(len(pred_obvs[k])) :
        j+=list[i]
        new_list.append(j)
    pred_obvs[k]=new_list
print ("\nThe Cumulative Predicted Climatological Values are :\n",pred_obvs)

for k in range(len(obvs)) :
    list=obvs[k]
    new_list=[]
    j=0
    for i in range(len(obvs[k])) :
        j+=list[i]
        new_list.append(j)
    obvs[k]=new_list
print ("\nThe Cumulative Observed Values are :\n",obvs)

print ("\nThe Cumulative Error Values of Model Predictability are :\n", np.subtract(pred_mod,obvs))

sq_err_fcst = (np.subtract(pred_mod,obvs))**2
print ("\nThe Squared Error Values of Model Predictability are :\n",sq_err_fcst)

sq_err_clim = (np.subtract(pred_obvs,obvs))**2
print ("\nThe Squared Error Values of Climatology are :\n",sq_err_clim)

rps_fcst = 1.0/(ncat-1.0)*np.sum(sq_err_fcst, axis=1)
print ("\nForecast RPS are :\n",rps_fcst)
mean_rps_fcst = mean(rps_fcst)
mean_rps_fcst=float("{:.2f}".format(mean_rps_fcst))

rps_clim = 1.0/(ncat-1.0)*np.sum(sq_err_clim, axis=1)
print ("\nClimatology RPS are :\n",rps_clim)

rpss = 1.0-(np.sum(rps_fcst)/np.sum(rps_clim))
rpss=float("{:.2f}".format(rpss))
print ("\nRPSS is :\n",rpss)

# rpss = 1.0-(rps_fcst/rps_clim)
# mean_rpss = mean(rpss)
# mean_rpss=float("{:.2f}".format(mean_rpss))
# print ("\nRPSS is :\n",rpss)

#######################################################################
# Plotting
#######################################################################
fig1 = plt.figure()
fig1.set_figwidth(10)
fig1.set_figheight(3)
plt.rcParams["font.family"] = "Times New Roman"

plt.plot(rps_fcst, lw=2, color='black')
plt.xlabel('Year', size=15)
plt.xlim([0, 28])
plt.ylim([0.0, 0.5])
x_pos = np.arange(len(pred_mod))
plt.xticks(x_pos, years, size=12, rotation=90)
plt.yticks(size=12)
plt.title('RPS (CFSv2, T382, Feb IC)', size=18)

plt.hlines(y=mean_rps_fcst, xmin=0, xmax=29, colors='blue', linestyles='--', lw=2, label='Mean RPS = %0.2f' %mean_rps_fcst)
plt.legend(bbox_to_anchor=(0.85,0.9), loc="upper right", borderaxespad=0)

plt.annotate('RPSS = %0.2f' %rpss, xy=(18.75, 0.35), bbox=dict(boxstyle='round', fc='w'))

fig1.savefig("RPS_fcst_1D.eps", bbox_inches='tight')
fig1.savefig("RPS_fcst_1D.png", bbox_inches='tight')

# fig2 = plt.figure()
# fig2.set_figwidth(10)
# fig2.set_figheight(3)

# plt.plot(rpss, lw=2, color='black')
# plt.xlabel('Year', size=15)
# plt.xlim([0, 29])
# plt.ylim([-2.0, 1.0])
# x_pos = np.arange(len(pred_mod))
# plt.xticks(x_pos, years, size=12, rotation=90)
# plt.yticks(size=12)
# plt.title('RPSS (CFSv2, T382, Feb IC)', size=18)

# plt.hlines(y=0, xmin=0, xmax=29, colors='blue', linestyles='--', lw=2)
# plt.annotate('Mean RPSS = %0.2f' %mean_rpss, xy=(23, -1.6), bbox=dict(boxstyle='round', fc='w'))

# fig2.savefig("RPSS.eps", bbox_inches='tight')
# fig2.savefig("RPSS.png", bbox_inches='tight')

#######################################################################

filein1.close()
filein2.close()
filein3.close()
exit()
