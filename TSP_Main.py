import os
import sys
import time
import random
from GraphCreation import GraphCreation
import mstapprox as msta
from BnB import BnB
import sa_base
import sa_improved
import argparse
#import twoopt
import two_opt_imp as topt


'''
This is the base file which contains the code for parsing the arguments and calling respective functions.
##############################################################################
The file writes the various parameters in proj_object variable the structure of which is defined in GraphCreation.py as follows:

self.graph = netx.Graph() : The graph is stored in the form of a networkx object i.e. a list of (source,target,{weight:10})
self.params = {'max_time':600,'rand_seed':0} : These parameters define execution timeout time and random seed to initialize from
self.dist_type = 'EUC_2D' : This is the distance type to use. This is already taken care of while creating the graph
self.file_name = '' : Input filename

#################################Output Format##############################
Each function should return 3 values:

1. Minimum Distance (min_dist)
2. Best Solution Path/Tour (tour)
3. Trace Data which stores execution time and best solution found till that time in a list(trace_data). e.g.:
[[0.017951250076293945,320374],
[0.018466711044311523,310661],
[0.018466711044311523,309123],
[0.01945638656616211,299464],
[0.02145218849182129,294938]]

The output is currently written in output_test folder which will be changed to output folder finally

#############################################################################
To run this file, use the following syntax:

Usage Syntax: python TSP_Main.py -inst Atlanta.tsp -alg LS3 -time 600 -seed 0

'''

def write_output(file_ptr,datalines):
    for i in datalines:
        file_ptr.write(str(i) + "\n")

#parsing the arguments
parser = argparse.ArgumentParser(description='Traveling Salesman Problem Solver')
parser.add_argument('-inst', nargs="?")
parser.add_argument('-alg', nargs="?")
parser.add_argument('-time', type=int)
parser.add_argument('-seed', type=int)

args = parser.parse_args()
method = args.alg
file_name = args.inst.split(".")[0]

# define object with graph creation class
proj_object = GraphCreation()
#call read graph function to read the graph from the edges in file
proj_object.readgraph('./data/' + args.inst)

#set the various parameters for the graph
#use rand_seed = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 35, 40, 45, 50, 100, 1000] in case of local search
proj_object.params['rand_seed'] = args.seed 

proj_object.file_name = file_name
proj_object.params['max_time'] = args.time

#print(proj_object.params)
#print(len(proj_object.graph))

'''
pass the project object and execute. There are 5 algorithms which have been implemented. This returns the tour and trace data.
'''
if method == 'BnB':
    #Branch and Bound - defining object and calling the function
    ob = BnB(proj_object.graph,proj_object.params['max_time'])
    min_dist,tour,trace_data = ob.bnb()
elif method == 'MST':
    min_dist, tour, trace_data = msta.mst_approximation(proj_object)
# elif method == 'Christofides':
#     min_dist, tour, trace_data = msta.mst_approximation(proj_object)
elif method == 'LS1':
    #Local Search - 2-Opt
    # print(proj_object.graph.edges())
    new_graph_imp = topt.two_opt(graph = proj_object.graph, time = proj_object.params['max_time'], seed = proj_object.params['rand_seed'] )
    min_dist, tour, trace_data = new_graph_imp.bests()
    #min_dist, tour, trace_data = twoopt.two_opt(proj_object)
elif method == 'LS2':
    #Local Search - simulated annealing
    min_dist, tour, trace_data = sa_base.simulated_annealing(proj_object)
elif method == 'LS3':
    #Local Search - improved simulated annealing
    min_dist,tour,trace_data = sa_improved.simulated_annealing_improved(proj_object)

#get results,transform into string and write tour and trace files
trace_data = [",".join(map(str,x)) for x in trace_data]
tour_data = []
tour_data.append(min_dist)
tour_data.append(",".join(map(str,tour)))  

outname = "./output/" +  file_name + "_" + method + "_" + str(proj_object.params['max_time']) + "_" + str(proj_object.params['rand_seed'])

f_out = open(outname + ".tour", "w")
write_output(f_out,tour_data)
f_out.close()
f_out_tr = open(outname + ".trace", "w")
write_output(f_out_tr, trace_data)
f_out_tr.close()
