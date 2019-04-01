# This file implements the class for defining the project object and load graph into it
import os
import math
import numpy as np
import time
import sys
import networkx as netx

class GraphCreation(object):

    def __init__(self):
        self.graph = netx.Graph()
        self.params = {'max_time':600,'rand_seed':0}
        self.dist_type = 'EUC_2D'
        self.file_name = ''
        self.dist = []

    def calc_dist_graph(self,node_data,dist_type):
        num_points = len(node_data)
        dist = []
        if dist_type == 'EUC_2D':
            dist = [[round(math.sqrt((node_data[i+1][0]-node_data[j+1][0])**2 + (node_data[i+1][1]-node_data[j+1][1])**2)) for i in range(num_points)] for j in range(num_points)]
            for i in range(num_points):
                dist[i][i] = 100000000000000

        elif dist_type == 'GEO':
            '''
            This needs to be updated

            '''
            for i in range(num_points):
                temp_dist = []
                for j in range(num_points):
                        
                        deg = int(node_data[i+1][0])
                        min = node_data[i+1][0]- deg
                        lat_x = math.pi * (deg + 5.0 * min/ 3.0) / 180.0
                        deg = int(node_data[i+1][1])
                        min = node_data[i+1][1] - deg
                        long_x = math.pi * (deg + 5.0 * min/ 3.0) / 180.0

                        deg = int(node_data[j+1][0])
                        min = node_data[j+1][0]- deg
                        lat_y = math.pi * (deg + 5.0 * min/ 3.0) / 180.0
                        deg = int(node_data[j+1][1])
                        min = node_data[j+1][1] - deg
                        long_y = math.pi * (deg + 5.0 * min/ 3.0) / 180.0
                        
                        RRR = 6378.388

                        q1 = math.cos( long_x - long_y )
                        q2 = math.cos( lat_x - lat_y ) 
                        q3 = math.cos( lat_x + lat_y )
            
                        temp_dist.append((int) ( RRR * math.acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0))
                dist.append(temp_dist)

            
            for i in range(num_points):
                dist[i][i] = 100000000000000
        return dist
    
    def calc_dist_edge(self,x,y):
        dist = -1
        if self.dist_type == 'EUC_2D':
            dist = round(math.sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2))    
        elif self.dist_type == 'GEO':
            '''
            Uses the format specificed on TSPLIB
            '''
            deg = int(x[0])
            min = x[0]- deg
            lat_x = math.pi * (deg + 5.0 * min/ 3.0) / 180.0
            deg = int(x[1])
            min = x[1] - deg
            long_x = math.pi * (deg + 5.0 * min/ 3.0) / 180.0

            
            deg = int(y[0])
            min = y[0]- deg
            lat_y = math.pi * (deg + 5.0 * min/ 3.0) / 180.0
            deg = int(y[1])
            min = y[1] - deg
            long_y = math.pi * (deg + 5.0 * min/ 3.0) / 180.0
            
            RRR = 6378.388

            q1 = math.cos( long_x - long_y ); 
            q2 = math.cos( lat_x - lat_y ); 
            q3 = math.cos( lat_x + lat_y ); 
            dist = (int) ( RRR * math.acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0);
        return dist

  
    def readgraph(self,file_path):
        f = open(file_path, 'r')
        all_lines = f.readlines()

        for i,elem in enumerate(all_lines):
            if 'EDGE_WEIGHT_TYPE' in elem:
                self.dist_type = elem.split(":")[-1].strip()
                break
        
        node_data = dict()
        for i in all_lines[3:]:
            line_split = i.split()
            if len(line_split) >= 3:
                #d[int(node_id)] = {'x':float(x), 'y':float(y)}
                #print(line_split)
                node_data[int(line_split[0])] = [float(line_split[1]), float(line_split[2])]

        for val1 in node_data.keys():
            for val2 in node_data.keys():
                if val1 != val2:
                    edge_dist = self.calc_dist_edge(node_data[val1],node_data[val2])
                    self.graph.add_node(val1)
                    self.graph.add_node(val2)
                    self.graph.add_edge(val1,val2,weight=edge_dist)
        #print(self.graph)
        edge_dist = np.array(self.calc_dist_graph(node_data, self.dist_type))
        #self.graph = netx.from_numpy_matrix(edge_dist)
        self.dist = edge_dist
        #print(self.dist)
        return True