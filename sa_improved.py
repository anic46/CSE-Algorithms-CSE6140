import math
import time
import numpy as np
import sys
import random
import os

def initialize_soln(G):
    g_soln = []
    node_list = list(range(len(G)))
    cur_node = random.sample(range(0,len(G)),1)[0]
    g_soln.append(cur_node)
    node_list.remove(cur_node)
    #print(node_list)
    while node_list:
        G_dist_s = [G[cur_node+1][k+1]['weight'] for k in node_list]
        min_dist_G = min(G_dist_s)
        cur_node = node_list[G_dist_s.index(min_dist_G)]
        node_list.remove(cur_node)
        g_soln.append(cur_node)
    return g_soln

def length_soln(G,cur_soln):
    dist = 0
    for i in range(0,len(cur_soln)-1):
        dist = dist + G_dist[cur_soln[i]][cur_soln[i+1]]
    dist = dist + G_dist[cur_soln[len(cur_soln)-1]][cur_soln[0]]
    return dist



def generate_3opt_move(cur_soln):
    n_nodes = len(cur_soln)
    while True:
            i = random.randint(0, n_nodes-1)
            j = random.randint(0, n_nodes-2)
            if abs(i-j) >= 2:
               break
    if i > j:
        i, j = j, i
    #reversed solution
    new_soln_r = cur_soln[:]
    if j - i == n_nodes-1:
        new_soln_r[i], new_soln_r[j] = cur_soln[j], cur_soln[i]
        return new_soln_r
    else:
        new_soln_r[i:j] = reversed(new_soln_r[i:j])
    
    #swapped solution
    new_soln_s = cur_soln[:]
    new_soln_s[i],new_soln_s[j] = cur_soln[j],cur_soln[i]
    
    #insert solution
    new_soln_i = cur_soln[:]
    new_soln_i.insert(i,new_soln_i[j])
    new_soln_i.pop(j+1)

    ind = [i,j,0,0,0,0]
    nn = (i + n_nodes - j - 1) % n_nodes
    ind[2] = i - 1
    ind[3] = j + 1
    nc = (j+1 + int(random.random()*(nn-1))) % n_nodes
    ind[4] = nc
    ind[5] = (nc+1) % n_nodes
    
    #transported solution
    nct = len(cur_soln)
    new_soln_t = []
    for j in range((ind[1]-ind[0]) % nct + 1):
            new_soln_t.append(cur_soln[(j+ind[0]) % nct])
    for j in range((ind[2]-ind[5]) % nct + 1):
            new_soln_t.append(cur_soln[(j+ind[5]) % nct])
    for j in range((ind[4]-ind[3]) % nct + 1):
            new_soln_t.append(cur_soln[(j+ind[3]) % nct])
    
    min_dist_ind = np.argmin(np.array((length_soln(G,new_soln_r),length_soln(G,new_soln_s),length_soln(G,new_soln_i),length_soln(G,new_soln_i))))
    if min_dist_ind == 0:
        return new_soln_r[:]
    elif min_dist_ind == 1:
        return new_soln_s[:]
    elif min_dist_ind == 2:
        return new_soln_i[:]
    return new_soln_t[:]


def generate_new_soln_sa(cur_soln):
    n_nodes = len(cur_soln)
    while True:
            i = random.randint(0, n_nodes-1)
            j = random.randint(0, n_nodes-2)
            if abs(i-j) >= 2:
               break
    if i > j:
        i, j = j, i
    
    #reversed solution
    new_soln_r = cur_soln[:]
    if j - i == n_nodes-1:
        new_soln_r[i], new_soln_r[j] = cur_soln[j], cur_soln[i]
        return new_soln_r
    else:
        new_soln_r[i:j] = reversed(new_soln_r[i:j])
    
    #swapped solution
    new_soln_s = cur_soln[:]
    new_soln_s[i],new_soln_s[j] = cur_soln[j],cur_soln[i]
    
    #insert solution
    new_soln_i = cur_soln[:]
    new_soln_i.insert(i,new_soln_i[j])
    new_soln_i.pop(j+1)

    min_dist_ind = np.argmin(np.array((length_soln(G,new_soln_r),length_soln(G,new_soln_s),length_soln(G,new_soln_i))))
    #print(i,j,min_dist_ind)
    if min_dist_ind == 0:
        return new_soln_r[:]
    elif min_dist_ind == 1:
        return new_soln_s[:]
    elif min_dist_ind == 2:
        return new_soln_i[:]

def generate_temp_list(G, Lmax, p0, init_soln_x):
    i_L = 0
    L = []
    x = init_soln_x[:]
    while (i_L < Lmax):
        x_dist = length_soln(G,x[:])
        y = generate_new_soln_sa(x[:])
        y_dist = length_soln(G,y[:])
        if y_dist<x_dist:
            x = y[:]
        if y_dist!=x_dist:
            t = - abs(float(y_dist)-float(x_dist))/math.log(p0)
            L.append(t)
            #print(t)
            i_L += 1
    #print (L)
    #time.sleep(10)
    return L

def simulated_annealing_improved(proj_object):
    global G
    global min_dist_ind
    global G_dist

    min_dist_ind = 0
    G = proj_object.graph
    G_dist = proj_object.dist
    start_time = time.time()
    exec_time = 0
    
    best_soln = []
    cur_soln = []
    new_soln = []

    min_dist = float('Inf')
    cur_dist = float('Inf')
    new_dist = float('Inf')
    
    trace_data = []

    random.seed(proj_object.params['rand_seed'])
    max_time = proj_object.params['max_time']

    k = 0
    K = 10000
    n_cities = len(G)
    M = 30#*n_cities
    Lmax = 110 #4*n_cities
    p0 = 0.8
    
    cur_soln = initialize_soln(G)
    cur_dist = length_soln(G,cur_soln)
    min_dist = cur_dist
    #print(cur_dist)

    temp_list = generate_temp_list(G, Lmax, p0, cur_soln[:])
    
    const_count = 0
    max_const_count = 100*n_cities
    
    while exec_time < max_time and k < K:
        accept_count = 0
        m = 0
        t_k = []
        accept_min_count = 0
        temp = max(temp_list)
        #print(temp)
        while m <= M and exec_time < max_time:
            if const_count >= 10*n_cities:
                new_soln = generate_3opt_move(cur_soln[:])
            else:
                new_soln = generate_new_soln_sa(cur_soln[:])
            new_dist = length_soln(G, new_soln)
            m += 1
            if new_dist <= cur_dist:
                cur_dist = new_dist
                cur_soln = new_soln[:]
                if new_dist < min_dist:
                    best_soln = cur_soln[:]
                    min_dist = cur_dist
                    #print(min_dist)
                    accept_min_count = 1
                    exec_time = (time.time() - start_time)
                    trace_data.append([exec_time,min_dist])
            else:
                prob_accept = math.exp(-abs(float(new_dist) - float(cur_dist))/temp)
                r = random.random()
                if r < prob_accept:
                    t_k.append(- abs(float(new_dist) - float(cur_dist))/math.log(r))
                    cur_soln = new_soln[:]
                    cur_dist = new_dist
                    accept_count += 1
            exec_time = (time.time() - start_time)

        # all_dist.append(cur_dist)
        if accept_count != 0:
            temp_new = sum(t_k)/len(t_k)
            temp_list.remove(temp)
            temp_list.append(temp_new)

        if accept_min_count == 0:
            const_count += 1
        else:
            const_count = 0
        if const_count >= max_const_count:
            #print(max_const_count)
            break
        k += 1
    best_soln = [i+1 for i in best_soln]
    return min_dist,best_soln,trace_data
