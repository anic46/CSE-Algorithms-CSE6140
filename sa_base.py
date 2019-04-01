import math
import time
import numpy as np
import sys
import random
import os
import mstapprox

'''
Initialize a greedy solution
'''

def initialize_soln(G):
    g_soln = []
    node_list = list(range(len(G)))
    cur_node = random.sample(range(0, len(G)), 1)[0]
    g_soln.append(cur_node)
    node_list.remove(cur_node)
    while node_list:
        G_dist_s = [G[cur_node+1][k+1]['weight'] for k in node_list]
        min_dist_G = min(G_dist_s)
        cur_node = node_list[G_dist_s.index(min_dist_G)]
        node_list.remove(cur_node)
        g_soln.append(cur_node)
    return g_soln


'''
Calculate the path length
'''

# def length_soln_sa_base(cur_soln):
#     dist = 0
#     for i in range(0,len(cur_soln)-1):
#         dist = dist + G[cur_soln[i]+1][cur_soln[i+1]+1]['weight']
#     dist = dist + G[cur_soln[len(cur_soln)-1]+1][cur_soln[0]+1]['weight']
#     return dist

def length_soln_sa_base(cur_soln):
    dist = 0
    for i in range(0,len(cur_soln)-1):
        dist = dist + G_dist[cur_soln[i]][cur_soln[i+1]]
    dist = dist + G_dist[cur_soln[len(cur_soln)-1]][cur_soln[0]]
    return dist

'''
Used to generate a new solution
'''
def generate_new_soln(cur_soln,ind,soln_type):
    new_soln_temp = []
    if soln_type == "reversed":
        new_soln_temp = cur_soln[:]
        i = ind[0]
        j = ind[1]
        new_soln_temp[i:j] = reversed(new_soln_temp[i:j])
    elif soln_type == "threeopt":
        n_cities = len(cur_soln)
        for j in range((ind[1]-ind[0]) % n_cities + 1):
            new_soln_temp.append(cur_soln[(j+ind[0]) % n_cities])
        for j in range((ind[2]-ind[5]) % n_cities + 1):
            new_soln_temp.append(cur_soln[(j+ind[5]) % n_cities])
        for j in range((ind[4]-ind[3]) % n_cities + 1):
            new_soln_temp.append(cur_soln[(j+ind[3]) % n_cities])
    return new_soln_temp[:] 

'''
This function is the main part of implementation of Simulated Annealing
'''

def simulated_annealing(proj_object):
    global G
    global G_dist
    G_dist = proj_object.dist
    G = proj_object.graph
    start_time = time.time()
    exec_time = 0

    best_soln = []
    cur_soln = []
    new_soln = []
    trace_data = []

    min_dist = float('Inf')
    cur_dist = float('Inf')
    new_dist = float('Inf')

    max_time = proj_object.params['max_time']
    rand_seed = proj_object.params['rand_seed']
    
    random.seed(rand_seed)
      
    temp_min = 1
    alpha = 0.99
    n_cities = len(G)
    iter_count = 0
    
    ind = np.zeros(6,dtype=int)
    cur_soln = initialize_soln(G)
    cur_dist = length_soln_sa_base(cur_soln)
    min_dist=cur_dist

    temp_start = 1000.0
    temp = float(temp_start)
    Preverse = 0.8
    
    max_iter_count = 10*n_cities
    max_accept_count = 1*n_cities
    const_count = 0
    max_const_count = 20*n_cities

    while temp >= temp_min and exec_time < max_time:
        accept_count = 0
        iter_count = 0
        accept_min_count = 0
        #print(temp)
        while iter_count <= max_iter_count and exec_time < max_time:
            
            while True:
                ind[0] = random.randint(0, len(G)-1)
                ind[1] = random.randint(0, len(G)-1)
                if (ind[1] >= ind[0]) : 
                    ind[1] = ind[1] + 1
                if (ind[1] < ind[0]): 
                    ind[1],ind[0] = ind[0],ind[1]
                n_diff = (ind[0] + n_cities - ind[1] - 1) % n_cities
                if n_diff>=2: break
            
            #Do reversing with 80% probability and 3-opt with 20% probability

            if Preverse > random.random():
                new_soln = generate_new_soln(cur_soln,ind,"reversed")
            else:
                ind[2] = ind[0] - 1
                ind[3] = ind[1] + 1
                ind[4] = (ind[1]+1 + int(random.random()*(n_diff-1))) % n_cities
                ind[5] = (ind[4]+1) % n_cities
                new_soln = generate_new_soln(cur_soln,ind,"threeopt")
            
            new_dist = length_soln_sa_base(new_soln)

            if new_dist < cur_dist:
                cur_dist = new_dist
                cur_soln = new_soln[:]
                accept_count += 1
                if new_dist < min_dist:
                    best_soln = cur_soln[:]
                    min_dist = cur_dist
                    exec_time = (time.time() - start_time)
                    trace_data.append([exec_time, min_dist])
                    accept_min_count = 1

            else:
                prob_accept = math.exp(-abs(float(new_dist) - float(cur_dist))/temp)

                if random.random() < prob_accept:
                    cur_soln = new_soln[:]
                    cur_dist = new_dist
                    accept_count += 1
            
            if accept_count > max_accept_count:
                break
            
            exec_time = (time.time() - start_time)
            iter_count += 1
            if accept_count > max_accept_count:
                break

        temp = alpha*temp
        
        if accept_count == 0 or const_count >= max_const_count:
            break

        if accept_min_count == 0:
            const_count += 1
        else:
            const_count = 0
    exec_time = (time.time() - start_time)
    trace_data.append([exec_time,min_dist])
    
    return min_dist,best_soln,trace_data