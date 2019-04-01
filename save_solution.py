# This file contains code used to generate plots from the trace and
# solution plots

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import csv
from os import listdir
from os.path import isfile, join
import sys


concorde_soln = {'Atlanta':2003763,'Berlin':7542,'Boston':893536,'Champaign':52643,'Cincinnati':277952,'Denver':100431,'NYC':1555060,'Philadelphia':1395981,'Roanoke':655454,'SanFrancisco':810196,'Toronto':1176151,'ulysses16':6859,'UMissouri':132709}
algos = {'BnB':'BnB','MST':'MSTApprox','LS1':'2-Opt','LS2':'Simulated Annealing','LS3':'List based Simulated Annealing'}

#box_time = {}
#box_quality = {}
#box_solution = {}
box_df = pd.DataFrame()

for algo in algos.keys():
    mypath = "./output_"+algo+"/"
    output_path = "./"
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    # boxplot_time = {}
    # boxplot_quality = {}
    # average_data = {}

    for inst_name in concorde_soln.keys():
        optimum = concorde_soln[inst_name]

        time_data = []
        quality_data = []
        solution_data = []
        for i in range(len(onlyfiles)):
            if (inst_name in onlyfiles[i]) and ('.trace' in onlyfiles[i]) and (algo in onlyfiles[i]):
                input_file_reader = csv.reader(open(mypath + "/" + onlyfiles[i]), delimiter=',')
                previous_row = ''
                for row in input_file_reader:
                    if row[1] != previous_row:
                        t = row[0]
                        q = row[1]
                    previous_row = row[1]
                
                box_df = box_df.append({'Algorithm':algo,'Instance':inst_name,'Time':float(t), 'Error':round(1.0-float(optimum)/float(q),2), 'Solution':int(q),'Optimum' : optimum},ignore_index=True)

box_df.to_csv('results_summary.csv')