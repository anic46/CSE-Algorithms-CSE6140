import math
import time
import numpy as np
import sys
import random
import os


def initialize_soln(G):
    g_soln = []
    node_list = list(range(len(G)))
    cur_node = random.sample(range(0, len(G)), 1)[0]
    g_soln.append(cur_node)
    node_list.remove(cur_node)
    while node_list:
        G_dist_s = [G_dist[cur_node][k] for k in node_list]
        min_dist_G = min(G_dist_s)
        cur_node = node_list[G_dist_s.index(min_dist_G)]
        node_list.remove(cur_node)
        g_soln.append(cur_node)
    return g_soln

def length_soln(G, cur_soln):
    dist = 0
    for i in range(0, len(cur_soln)-1):
        dist = dist + G[cur_soln[i]+1][cur_soln[i+1]+1]['weight']
    dist = dist + G[cur_soln[len(cur_soln)-1]+1][cur_soln[0]+1]['weight']
    return dist

def generate_new_soln(cur_soln,i,j):
    if i>j:
        i,j = j,i
    new_soln_temp = cur_soln[:]
    new_soln_temp[i+1:j+1] = reversed(new_soln_temp[i+1:j+1])
    return new_soln_temp[:]

def check_new_soln(G, G_dist_s, G_p, cur_soln):
    x = cur_soln[:]
    i = 0
    j = 0
    #print(x)
    y = [x.index(j) for j in range(0,len(G))]
    #print(y)
    n = len(G)
    delta = 0

    min_dist_r = length_soln(G,x)
    for i in range(0,n-1):
        for j in range(i+2,n):
                new_soln_r = x[:]
                new_soln_r[i+1:j+1] = reversed(x[i+1:j+1])
                delta = length_soln(G,new_soln_r) - min_dist_r
                #print(delta)
                if (delta < 0):
                    break
        if delta<0:
            break
    if delta < 0:
        #print("return_1")
        return i, j, False
    
    for i in range(0,n):
        ndash = G_p[x[i]][x[(i+1)%n]]
        #print(ndash)
        for jdash in range(0,ndash):
            c = G_dist_s[i][jdash]
            j = y[c]
            #print("%d,%d, %d, %d, %d" % (i, j, c, jdash, delta))
            if i == j or (i==n-1 and j==0):
                continue
            else:
                delta = G[x[i]+1][x[j]+1]['weight'] + G[x[(i+1)%n]+1][x[(j+1)%n]+1]['weight'] \
                - G[x[i]+1][x[(i+1)%n]+1]['weight'] - G[x[j]+1][x[(j+1)%n]+1]['weight']
                #print("%d,%d, %d, %d, %d" % (i, j, c, jdash, delta))
                if delta < 0:
                    break
        if delta < 0:
            break

    if delta < 0:
        #print("return_1")
        return i, j, False
    # 1-2-3-4-5, 1-2-4-3-5, 1-2-4-3-5
    # 1-2-3-4-5, 1-3-2-4-5, 1-4-3-2-5 

    for i in range(1, n+1):
        ndash = G_p[x[i%n]][x[i-1]]
        for jdash in range(0, ndash):
            c = G_dist_s[i%n][jdash]
            j = y[c]
            if j ==0:
                j = n
            if i == j:
                continue
            else:
                delta = G[x[i%n]+1][x[j%n]+1]['weight'] + G[x[(i-1)%n]+1][x[(j-1)%n]+1]['weight'] - G[x[i%n]+1][x[(i-1)%n]+1]['weight'] - G[x[j%n]+1][x[(j-1)%n]+1]['weight']
                #print("%d,%d, %d, %d, %d" % (i, j, c, jdash, delta))
                #aa = generate_new_soln(x, i-1, j-1)
                #print(aa)
                #print (length_soln(G,aa[:]))
                if delta < 0:
                    break
        if delta < 0:
            i = i - 1
            j = j - 1
            break

    if delta < 0:
        #print("return_1")
        return i, j, False
        
    if delta >= 0:
        return i,j,True
    else:
        return i,j,False


def two_opt(proj_object):
    global G
    G = proj_object.graph
    global G_dist
    G_dist = proj_object.dist
    #G_dist = proj_object.dist
    
    G_dist_s = np.argsort(np.array(G_dist),axis=1)
    #print(G_dist_s)
    G_p = [[G_dist_s[i,:].tolist().index(j) for j in range(0,len(G))] for i in range(0,len(G))]
    #print(G_p)

    start_time = time.time()
    exec_time = 0
    best_soln = []
    cur_soln = []
    new_soln = []

    min_dist = float('Inf')
    cur_dist = float('Inf')
    new_dist = float('Inf')
    all_dist = []
    max_time = proj_object.params['max_time']
    rand_seed = proj_object.params['rand_seed']
    trace_data = []

    random.seed(rand_seed)
    #node_list = range(len(G))
    n_cities = len(G)
    iter_count = 0
    max_iter_count = 100*n_cities
    max_accept_count = 10*n_cities

    cur_soln = initialize_soln(G)
    cur_dist = length_soln(G, cur_soln)

    max_const_count = 1000
    const_count = 0

    while exec_time < max_time:
        i,j,check_complete = check_new_soln(G, G_dist_s, G_p, cur_soln)
        if check_complete:
            break
        
        new_soln = generate_new_soln(cur_soln,i,j)
        new_dist = length_soln(G,new_soln)

        if new_dist < min_dist:
                best_soln = new_soln[:]
                cur_soln = new_soln[:]
                min_dist = new_dist
                exec_time = (time.time() - start_time)
                trace_data.append([exec_time, min_dist])
                #print(min_dist)
                accept_min_count = 1
        exec_time = (time.time() - start_time)
       
        all_dist.append(cur_dist)

        if accept_min_count == 0:
            const_count += 1
        else:
            const_count = 0

        if const_count >= max_const_count:
            #print("accept_count")
            break

    return min_dist, best_soln, trace_data
