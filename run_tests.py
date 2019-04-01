import os
import random

filenames = os.listdir("./data")
for f in filenames:
    if f.find(".tsp") < 0:
        filenames.remove(f)

#This file is to run and test the code on various graphs generating 10 instances for Local Search

algs = ['LS2']
flag = 0
for alg in algs:
    for filename in filenames:
        #if filename == 'ulysses16.tsp':
        #     flag= 1
        # if flag == 1:
        #if filename != 'Atlanta.tsp' and filename != 'Boston.tsp' and filename !='Berlin.tsp':
            if alg in ['LS1','LS2', 'LS3']:
                rand_seeds = random.sample(range(1,100),10)
            else:
                rand_seeds = [0]
            for rand_seed in rand_seeds:
                    exec_str = "python TSP_Main.py -inst " + filename + " -alg " + alg + " -time 600 -seed " + str(rand_seed)
                    print(exec_str)
                    os.system(exec_str)
