# -*- coding: utf-8 -*-
"""
Created on Wed May 17 16:06:06 2023

@author: Jian Wang
"""
import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time

from collections import namedtuple
from itertools import count
from PIL import Image
from itertools import combinations

p_g = 0.5
Lambda = 0.0006
Device_Num = 30
DN_set = []
for i in range(10, Device_Num-1):
    DN_set.append(i)
RT = len(DN_set)

def Poisson(t, k):
    P_t_k = ((math.exp(-Lambda * t)) * ((Lambda * t) ** k)) / math.factorial(k)
    return P_t_k

p_f = (1 - Poisson(200, 0))
print(p_f)

def Com_Cost(n, f, p):
    cc = 0
    if f == 0:
        cc = (n - 1) * (1 - p_f)
    elif f == 1:
        cc = (n - 1) * (1 - p_f) + p * Device_Num + 2 * (1 - p)
    elif f == 2:
        cc = ((p * n * (n - 2)) * ((1 - p_f) ** 2)) / 4
    return cc
    


Com_Cost_List = []

for i in range(3):
    cc_list = []
    for j in DN_set:
        if i == 1:
            cc_list.append(Com_Cost((j + 1), i, p_f))
        else:
            cc_list.append(Com_Cost((j + 1), i, p_g))
    
    Com_Cost_List.append(cc_list)
        
plt.figure()
b3 = [i+1 for i in range(len(Com_Cost_List[0]))]
plt.plot(b3, Com_Cost_List[0])
plt.plot(b3, Com_Cost_List[1])
plt.plot(b3, Com_Cost_List[2])
plt.title("Overhead")
plt.xlabel("Com Number")
plt.ylabel("Density") 
plt.show()


txtName = "Overhead_Central.txt"
f = open(txtName, "a+")
for p in range(len(Com_Cost_List[0])):
    if p == (len(Com_Cost_List[0]) - 1):
        new_context = str(Com_Cost_List[0][p])
    else:
        new_context = str(Com_Cost_List[0][p]) + '\n'
    f.write(new_context)
f.close()  

txtName = "Overhead_Selection.txt"
f = open(txtName, "a+")
for p in range(len(Com_Cost_List[1])):
    if p == (len(Com_Cost_List[1]) - 1):
        new_context = str(Com_Cost_List[1][p])
    else:
        new_context = str(Com_Cost_List[1][p]) + '\n'
    f.write(new_context)
f.close()  

txtName = "Overhead_Gossip.txt"
f = open(txtName, "a+")
for p in range(len(Com_Cost_List[2])):
    if p == (len(Com_Cost_List[2]) - 1):
        new_context = str(Com_Cost_List[2][p])
    else:
        new_context = str(Com_Cost_List[2][p]) + '\n'
    f.write(new_context)
f.close()  


