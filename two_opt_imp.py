import networkx as nx
import numpy as np
import heapq as hq
import math
import copy
import random as rand
import time

class two_opt(object):

    def __init__(self, graph = [], time = [], seed = 1):
        self.graph = graph
        self.init = 1
        self.time = time
        self.seed = seed
        self.new_weight = float('inf')
        self.route = []
        self.struc = []
        self.tracker = 0
        self.rar = 0.98
        self.radr = 0.95
        self.best_route = []
        self.best_struc = []
        self.best_w = float('inf')
        self.flag = True
        self.trace = 0
        self.count = 0

    "CALCULATE MST"
    def computeMST(self, G):

        set_visited = [1]
        weight_MST = 0
        vertices = G.nodes()
        new_node = 1
        self.struc = []
        # print(list(vertices-set_visited))

        while len(set_visited) != len(vertices):
            best_w = float('inf')
            best_edge = []

            for val in list(set(vertices)-set(set_visited)):
                edge_w = G[new_node][val]['weight']
                if edge_w<best_w:
                    best_w = edge_w
                    best_edge = [new_node,val, best_w]
                    best_node = val
            # print(best_edge)
            self.struc.append(best_edge)
                # print (self.struc)
            new_node = best_node
            set_visited.append(best_node)

    def original_route(self):
        "CONSTRUCTION OF MOST LIKELY OPTIMAL SOLUTION"
        # print(self.graph[1][10]['weight'])

        self.computeMST(self.graph)
        # print(self.graph[1][10]['weight'])

        newG = nx.Graph()
        newG.add_weighted_edges_from(self.struc)
        self.struc = np.array(self.struc)
        model = list(newG.adj.items())
        nodes = newG.nodes()
        mst_cycle = []
        h_cyc = 0
        u=1
        nods_vis = []
        route = [self.init]
        max = 0
        # print(self.graph[1][10]['weight'])


        while len(list(set(nods_vis))) != len(nodes):

            adj_nodes = list(model[u-1][1].keys())
            # print (adj_nodes)

            if u == self.init and u not in nods_vis:
                nods_vis.append(u)
                v = adj_nodes[0]
                nods_vis.append(v)
                route.append(v)
                # h_cyc += self.graph[u][v]['weight']
            else:
                if len(adj_nodes) == 1:
                    v = adj_nodes[0]
                    route.append(v)
                    # h_cyc += self.graph[u][v]['weight']
                    nods_vis.append(v)
                else:
                    queue = []
                    for val in adj_nodes:
                        if val not in nods_vis:
                            hq.heappush( queue, (self.graph[u][val]['weight'], u ,val ) )
                    if len(queue) == 0:
                        edge_v = np.where(self.struc[:,1]==u)[0]
                        new_edge = self.struc[edge_v,:]
                        v, u, w = new_edge[0][0], new_edge[0][1], new_edge[0][2]
                        hq.heappush( queue, (w, u ,v) )

                    w, u, v = hq.heappop(queue)
                    nods_vis.append(v)

                    route.append(v)
                    # h_cyc += self.graph[u][v]['weight']
            u = v
            max+=1
            if max>10000:
                nods = self.graph.nodes()[1:]
                sec = rand.sample(nods, len(nods))
                route = list(range(1, len(nods)))
                route[1:] = sec
                break

        route.append(self.init)
        # print(route)

        # print("IT WASNT ME")

        new_cycle, route, new_weight = self.new_struc(route)
        # print("IT WASNT ME")
        # print(route)
        # print(self.new_weight)
        # print(self.struc)
        # print(self.graph[1][10]['weight'])

        return new_cycle, new_weight, route



    def new_struc(self, route):

        new_cycle = []
        curr_route = [self.init]
        i = 1
        s = 1

        while i<(len(route)):
            if route[i] not in curr_route:
                curr_route.append(route[i])
                if curr_route[s-1]==self.init:
                    new_cycle = np.array([curr_route[s-1], curr_route[s], self.graph[curr_route[s-1]][curr_route[s]]['weight']])
                else:
                    new_cycle = np.vstack((new_cycle, [curr_route[s-1], curr_route[s], self.graph[curr_route[s-1]][curr_route[s]]['weight']]))
                s+=1
            i += 1

        curr_route.append(self.init)
        new_cycle = np.vstack((new_cycle, [curr_route[s-1],self.init, self.graph[curr_route[s-1]][self.init]['weight']]))

        self.new_weight = np.sum(new_cycle[:,2])
        self.route = curr_route
        self.struc = new_cycle
        new_route = curr_route
        # print(new_route)

        return new_cycle, new_route, self.new_weight

    def two_exchange(self, route):
        tic = time.time()
        toc = time.time()
        care = False
        # print("YA EMPECE")
        while toc-tic < self.time-30 and self.count <100000:
            curr_opt_route = copy.deepcopy(self.route)
            o_route = copy.deepcopy(self.route)
            curr_opt_w = self.new_weight
            curr_struc = self.struc
            # print(struc)
            # print(route)
            # print(curr_opt_w)
            if self.tracker > 1:
                o_route = self.randomized(route)
                curr_opt_route = copy.deepcopy(o_route)
                curr_opt_w = float('inf')


            for i in range(1, len(route)-2):
                route = copy.deepcopy(o_route)
                val_ex = route[i]

                for j in range(i+1, len(route)-1):
                    route = copy.deepcopy(curr_opt_route)
                    if j-i ==2:
                        val_ex = route[i+1]
                        route[i+1] = route[j]
                        route[j] = val_ex
                    else:
                        sec = route[i+1:j]
                        sec.reverse()
                        route[i+1:j] = sec
                    # print(route)
                    new_struc, new_route, new_weight = self.new_struc(route)
                    if new_weight<curr_opt_w:
                        curr_opt_w = new_weight
                        self.new_weight = curr_opt_w
                        curr_opt_route = new_route
                        curr_struc = new_struc

                    # print (route)
                    reverse = copy.deepcopy(route)
                    reverse.reverse()
                    new_struc, new_route, new_weight = self.new_struc(reverse)
                    if new_weight<curr_opt_w:
                        curr_opt_w = new_weight
                        self.new_weight = curr_opt_w
                        curr_opt_route = new_route
                        curr_struc = new_struc

                    if curr_opt_w<self.best_w:
                        self.best_w = curr_opt_w
                        self.best_route = curr_opt_route
                        self.best_struc = curr_struc
                        toc2 = time.time()
                        if self.trace == 0:
                            self.trace = [[toc2-tic, int(curr_opt_w)]]
                        else:
                            self.trace.append([toc2-tic, int(curr_opt_w)])

                    if time.time()-tic> self.time - 5:
                        care = True
                        break

                    self.count+=1
                if time.time()-tic> self.time - 5:
                    care = True
                    break

            if care == False:
                for z in range(1, len(route)-1):
                    last_comb = copy.deepcopy(curr_opt_route)
                    val = last_comb.pop(1)
                    index = len(last_comb)-1
                    last_comb.insert(int(index),val)
                    new_struc, new_route, new_weight = self.new_struc(last_comb)
                    if new_weight<curr_opt_w:
                        curr_opt_w = new_weight
                        self.new_weight = curr_opt_w
                        curr_opt_route = new_route
                        curr_struc = new_struc
                        self.count+=1
                        break

            # print (o_route)
            # print (curr_opt_route)

            if o_route == curr_opt_route:
                self.tracker +=1

            if curr_opt_w<self.best_w:
                self.best_w = curr_opt_w
                self.best_route = curr_opt_route
                self.best_struc = curr_struc
                self.count = 0

                toc2 = time.time()
                if self.trace == 0:
                    self.trace = [[toc2-tic, int(curr_opt_w)]]
                else:
                    self.trace.append([toc2-tic, int(curr_opt_w)])

            self.struc, self.route, self.new_weight = curr_struc, curr_opt_route, curr_opt_w
            # print(opt_struc, opt_route, opt_w)
            # print(curr_opt_w)
            toc = time.time()


    def randomized(self,route):

        val =rand.random()

        if val<= self.rar:
            new_route = route[1:-1]
            rand.shuffle(new_route)
            self.rar*=self.radr

        elif self.flag == True:
            new_route = copy.deepcopy(self.best_route[1:-1])
            if val<= 0.33:
                init = 0
                fin = int(len(new_route)/3)
            elif val<=0.66:
                init = int(len(new_route)/3)
                fin = int(2*len(new_route)/3)
            else:
                init = int(2*len(new_route)/3)
                fin = int(len(new_route)-1)

            section = rand.sample(new_route[init:fin], len(new_route[init:fin]))
            new_route[init:fin] = section
            self.flag = False

        else:
            new_route = copy.deepcopy(self.best_route[1:-1])
            if val<= 0.25:
                init = int(len(new_route)/6)
                fin = int(len(new_route)/2)
            elif val<=0.50:
                init = int(len(new_route)/2)
                fin = int(5*len(new_route)/6)
            elif val <=0.75:
                init = 0
                fin = int(len(new_route)/2)
            else:
                init = int(len(new_route)/2)
                fin = int(len(new_route)-1)

            section = rand.sample(new_route[init:fin], len(new_route[init:fin]))
            new_route[init:fin] = section
            self.flag = True

        new_route.append(1)
        new_route.insert(0,1)
        # print (intermediate)
        str, rou, wei = self.new_struc(new_route)
        self.tracker =1

        return new_route

    def bests(self):
        curr_struc, weight, route = self.original_route()
        self.two_exchange(route)
        # print(self.rar)
        # print(self.best_w)
        # print(self.best_route)
        # print(self.trace)
        # print(self.count)
        return self.best_w, self.best_route, self.trace
