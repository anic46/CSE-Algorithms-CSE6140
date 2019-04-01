import networkx as nx
import sys
import numpy as np
import time

class BS:

    def __init__(self,graph, path, path_cost, matrix):
        self.graph = graph
        self.path = path
        self.path_cost = path_cost
        self.matrix = matrix


    def stop_node(self, stop):
        if len(self.path):
            self.path_cost = self.path_cost + self.graph[self.path[-1]][stop]['weight']
        self.path.append(stop)
        self.b = self.minlb(self.matrix, self.path, self.path_cost)


    def lb(self, graph, path, path_cost):
        sub_graph = graph.copy()
        if len(path) > 1 and path[0] == path[-1]:
            path = path[:-1]

        for n in path:
            sub_graph.remove_node(n)

        mst = nx.minimum_spanning_tree(sub_graph)
        start_u = path[0]
        start_v = self.least_cost_neighbour(start_u,graph)
        end_u = path[-1]
        end_v = self.least_cost_neighbour(end_u,graph)

        mst.add_edge(start_u, start_v, weight=graph[start_u][start_v]['weight'])
        mst.add_edge(end_u, end_v, weight= graph[end_u][end_v]['weight'])

        return path_cost + mst.size(weight='weight')


    def minlb(self, matrix, path, path_cost):
        mat = matrix.copy()
        if len(path) > 1:
            i=0
            while i < len(path)-2:
                mat[path[i]-1] = sys.maxsize
                mat[path[i+1]-1] = sys.maxsize
                i += 2
        row_min = np.amin(mat, axis=1)
        mat = mat - np.reshape(row_min,(len(matrix),1))
        col_min = np.amin(mat, axis=0)

        return np.sum(row_min) + np.sum(col_min) + path_cost


    def least_cost_neighbour(self, node, graph):
        temp_dict = graph[node]
        tup = []
        for key in temp_dict:
            tup.append((key,temp_dict[key]['weight']))

        return min(tup,key =lambda edge:edge[1])[0]

class BnB:

    def __init__(self, graph, limit=600):
        self.graph = graph
        self.winner = None
        self.results = []
        self.limit = limit


    def DFS(self, graph, matrix):
        stack = []
        initial_city = 1
        initial_state = BS(graph.copy(), [], 0, matrix)
        initial_state.stop_node(initial_city)
        stack.append(initial_state)
        i = 0
        prev_shorter = 0
        while len(stack):
            if time.time() - self.begin_time > self.limit:
                break

            last_state = stack.pop()
            if not self.winner or last_state.b < self.winner.b:
                if len(graph.node.keys()) == len(last_state.path):
                    if last_state.path[0] in graph[last_state.path[-1]].keys():
                        last_state.stop_node(last_state.path[0])
                        if not self.winner or self.winner.b > last_state.b:
                            i += 1
                            self.results.append((last_state.path_cost, last_state.path,[time.time() - self.begin_time, last_state.path_cost]))
                            prev_shorter = last_state.path_cost
                            self.winner = last_state
                else:
                    sorted_list = self.se(graph[last_state.path[-1]])
                    for node,cost in sorted_list:
                        if node not in last_state.path:
                            new_state = BS(graph, last_state.path[:], last_state.path_cost, matrix)
                            new_state.stop_node(node)
                            if not self.winner or self.winner.b > new_state.b:
                                stack.append(new_state)


    def se(self,x):
        tup = []
        for key in x:
            tup.append((key,x[key]['weight']))
        sorted(tup, key=lambda edge:edge[1], reverse=True)
        return tup


    def bnb(self):
        graph = self.graph
        mat = [[0 for i in range(len(graph.node.keys()))] for j in range(len(graph.node.keys()))]
        for i in range(len(graph.node.keys())):
            for j in range(len(graph.node.keys())):
                if i != j:
                    mat[i][j] = graph[i+1][j+1]['weight']
                else:
                    mat[i][j] = sys.maxsize
        self.mat = np.array(mat)
        self.begin_time = time.time()
        self.DFS(graph, self.mat)

        min_dist = self.results[-1][0]
        tour = self.results[-1][1]
        trace_data = []
        for i in range(0,len(self.results)):
            trace_data.append(self.results[i][-1])

        return min_dist, tour, trace_data
