import queue as q
import time
import random
import os
import math
import numpy as np
import time
import sys


def depth_first_search(edge_list, path, parent):
    if parent not in path:
        path.append(parent)
        child = [x[1] for x in edge_list if x[0] == parent]
        if len(child) > 0:
            for node in child:
                depth_first_search(edge_list, path, node)
        else:
            return

def find_set(node, sets):
    for s in sets:
        if node in s:
            return s

def Kruskal_MST(G):
    #Kruskal used to compute the MST
    node_set = []
    for i in G.nodes():
        node_set.append(set([i-1]))
    
    G_sorted = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    pq = q.PriorityQueue(len(G_sorted))
    for i in range(len(G_sorted)):
        pq.put((G_sorted[i][2]['weight'], G_sorted[i][0]-1, G_sorted[i][1]-1))
    MST_edge_list = []

    while len(MST_edge_list) < len(G) - 1:
        tmp_edge = pq.get()

        tmp_edge_tuple = (tmp_edge[1], tmp_edge[2], tmp_edge[0])
        set1 = find_set(tmp_edge_tuple[0], node_set)
        set2 = find_set(tmp_edge_tuple[1], node_set)
        if set1 != set2:
            MST_edge_list.append(tmp_edge_tuple)
            node_set.remove(set1)
            node_set.remove(set2)
            node_set.insert(0, set1.union(set2))
    #print (MST_edge_list)
    return MST_edge_list

def length_soln_mst(G, cur_soln):
    dist = 0
    #print(G)
    for i in range(0, len(cur_soln)-1):
        dist = dist + G[cur_soln[i]+1][cur_soln[i+1]+1]['weight']
    dist = dist + G[cur_soln[len(cur_soln)-1]+1][cur_soln[0]+1]['weight']
    return dist

def mst_approximation(proj_object):
    G = proj_object.graph
    #print(G.edges(data=True))
    #max_time = proj_object.params['max_time']
    #rand_seed = random.randint(0, len(G)-1)
    random.seed(proj_object.params['rand_seed'])
    start_time = time.time()
    exec_time = 0
    trace_data = []
    MST_edges = Kruskal_MST(G)
    #print(MST_edges)
    
    #generating reverse edges
    reverse_edges = [(x[1], x[0], x[2]) for x in MST_edges]
    edge_list = MST_edges + reverse_edges
    
    parent = 0
    tour = []
    
    #finding Eulerian Tour
    depth_first_search(edge_list, tour, parent)

    trace_data = []

    min_dist = length_soln_mst(G, tour)
    exec_time = round(time.time() - start_time,4)
    trace_data.append((exec_time,min_dist))
    best_soln = [i+1 for i in tour]
    return min_dist,best_soln,trace_data
