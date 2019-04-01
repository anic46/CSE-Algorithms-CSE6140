
The base file contains the code for parsing the arguments and calling respective functions.
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
The versions used of additional libraries were:

networkx==1.11
numpy==1.15.1

To run this file, use the following syntax:

Usage Syntax: 
inst: filename.tsp
alg: approach desired
time: seconds
seed: integer

python TSP_Main.py -inst Atlanta.tsp -alg LS3 -time 600 -seed 0

Following algorithms have been implemented:
LS1 - Branch and Bound (Aditya)
LS2 - MST Approximation (Anirudh)
LS3 - Iterative Local Search (Leonardo)
LS4 - Simulated Annealing (Anirudh)
LS5 - List based Simulated Annealing (Anirudh)