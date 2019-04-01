# This file contains code used to generate plots from the trace and
# solution plots
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

import csv
from os import listdir
from os.path import isfile, join
import sys

from matplotlib.ticker import StrMethodFormatter

concorde_soln = {'Atlanta':2003763,'Berlin':7542,'Boston':893536,'Champaign':52643,'Cincinnati':277952,'Denver':100431,'NYC':1555060,'Philadelphia':1395981,'Roanoke':655454,'SanFrancisco':810196,'Toronto':1176151,'ulysses16':6859,'UMissouri':132709}
algos = {'LS1':'Iterative Method(2-Opt)','LS2':'Simulated Annealing','LS3':'List based Simulated Annealing'}
algo = 'LS3'

mypath = "./output_"+algo+"/"
output_path = "./"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

boxplot_time = {}
boxplot_quality = {}
average_data = {}

for name in concorde_soln.keys():
    optimum = concorde_soln[name]

    time_data = []
    quality_data = []
    solution_data = []
    for i in range(len(onlyfiles)):
        if (name in onlyfiles[i]) and ('.trace' in onlyfiles[i]) and (algo in onlyfiles[i]):
    
            input_file_reader = csv.reader(open(mypath + "/" + onlyfiles[i]), delimiter=',')
            previous_row = ''
            for row in input_file_reader:
                if row[1] != previous_row:
                    t = row[0]
                    q = row[1]
                previous_row = row[1]
            time_data.append(float(t))
            quality_data.append(1.0-float(optimum)/float(q))
            solution_data.append(int(q))

    #print(time_data)
    boxplot_time[name] = np.array(time_data)
    boxplot_quality[name] = np.array(quality_data)
    average_data[name] = [np.mean(time_data),np.mean(solution_data),np.mean(quality_data)]    
#print(boxplot_time)        
fig = plt.figure()
plt.plot()
ax = fig.add_subplot(111)
bp = ax.boxplot(boxplot_time.values())
ax.set_xticklabels(boxplot_time.keys())

#fig.suptitle('Runtime Distribution ('+algos[algo]+")", fontsize=12)
plt.xlabel('Instance', fontsize=10)
plt.xticks(rotation=90)
ax.tick_params(axis=u'both', which=u'both',length=0)
plt.ylabel('Time (in sec)', fontsize=10)
plt.tight_layout()
#plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
fig.savefig('./plots/box_time_' + algo+'.jpg')
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111)
bp = ax.boxplot(boxplot_quality.values())
ax.set_xticklabels(boxplot_quality.keys())

#fig.suptitle('Runtime Distribution ('+algos[algo]+")", fontsize=12)
plt.xlabel('Instance', fontsize=10)
plt.xticks(rotation=90)
ax.tick_params(axis=u'both', which=u'both',length=0)
plt.ylabel('Relative Error', fontsize=10)
plt.tight_layout()
#plt.gca().xaxis.set_major_formatter(StrMethodFormatter('{x:,.4f}'))
fig.savefig('./plots/box_quality_' + algo+'.jpg')

plt.show()