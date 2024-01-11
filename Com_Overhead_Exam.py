"""
Created on Wed Dec  6 11:12:20 2023
@author: Jian Wang
"""
import math
import random
import matplotlib.pyplot as plt
from CI import CI

Device_Num = 30
Lambda = 0.0006
T = 100
KT = 1000

P_Join = 0.5

DN_set = []
for i in range(10, Device_Num, 2):
    DN_set.append(i)
RT = len(DN_set)

def Poisson(t, k):
    P_t_k = ((math.exp(-Lambda * t)) * ((Lambda * t) ** k)) / math.factorial(k)
    return P_t_k

P_Fail = (1 - Poisson(200, 0))
print(P_Fail)
P_Gossip = 0.5

class Node():
    def __init__(self,index):
        self.index = index
        self.if_central_node = 0
        self.if_join_fl = 0
        self.if_fail = 0
    def join_check(self):
        if random.random() < P_Join:
            self.if_join_fl = 1
        else:
            self.if_join_fl = 0
    def fail_check(self):
        if random.random() < P_Fail:
            self.if_fail = 1
        else:
            self.if_fail = 0
                    
#create node
Node_List = []
for index in range(Device_Num):
    Node_List.append(Node(index))

#fixed central node
CI_S_1 = []
Com_Overhead_Avg_1 = []
Com_Overhead_Var_1 = []
Node_List[0].if_central_node = 1
Node_List[0].if_join_fl = 1

Com_Overhead_1 = []
for k in range(KT):#100 times
    Com_Overhead_One = []
    for r in DN_set:
        Node_Join_Num = 0
        for i in range(1, r + 1):
            Node_List[i].if_join_fl = 0
            Node_List[i].join_check()
            if Node_List[i].if_join_fl == 1:
                Node_List[i].fail_check()
                if Node_List[i].if_fail == 0:
                    Node_Join_Num = Node_Join_Num + 1                
        Com_Overhead_One.append(2 * Node_Join_Num)

    if k == 1:
        print(Com_Overhead_One)
    Com_Overhead_1.append(Com_Overhead_One)

#compute confidence interval
CI_S_1 = CI(Com_Overhead_1, Com_Overhead_Avg_1, Com_Overhead_Var_1, KT, RT,0,2)


#non-fixed central node
CI_S_2 = []

Com_Overhead_Avg_2 = []
Com_Overhead_Var_2 = []
Node_List[0].if_central_node = 1
Node_List[1].if_central_node = 1
Node_List[0].if_join_fl = 1

Com_Overhead_2 = []
for k in range(KT):#100 times
    Com_Overhead_Two = []
    for r in DN_set:
        Node_Join_Num = 0
        for i in range(1, r + 1):
            Node_List[i].join_check()
            if Node_List[i].if_join_fl == 1:
                Node_List[i].fail_check()
                if Node_List[i].if_fail == 0:
                    Node_Join_Num = Node_Join_Num + 1 
        Node_List[0].if_fail = 0
        Node_List[0].fail_check()
        if Node_List[0].if_fail == 1:
            Com_Overhead_Two.append(2 * Node_Join_Num + Device_Num)
        elif Node_List[0].if_fail == 0:
            Com_Overhead_Two.append(2 * Node_Join_Num + 2)
        
    if k == 1:
        print(Com_Overhead_Two)
    Com_Overhead_2.append(Com_Overhead_Two)

#compute confidence interval
CI_S_2 = CI(Com_Overhead_2, Com_Overhead_Avg_2, Com_Overhead_Var_2, KT, RT,0,2)


#gossip based decentralized
CI_S_3 = []

Com_Overhead_Avg_3 = []
Com_Overhead_Var_3 = []
Com_Overhead_3 = []

for k in range(KT*3):#100 times
    Com_Overhead_Three = []
    for r in DN_set:
        Node_Join_Num = 0
        for i in range(r + 1):
            Node_List[i].join_check()
            if Node_List[i].if_join_fl == 1:
                Node_List[i].fail_check()
                if Node_List[i].if_fail == 0:
                    Node_Join_Num = Node_Join_Num + 1                
        Com_Overhead_Three.append(P_Gossip * Node_Join_Num * (Node_Join_Num - 1))
    if k == 1:
        print(Com_Overhead_Three)
    Com_Overhead_3.append(Com_Overhead_Three)

#compute confidence interval
CI_S_3 = CI(Com_Overhead_3, Com_Overhead_Avg_3, Com_Overhead_Var_3, KT*3, RT,0,2)

plt.figure()
b3 = [i+1 for i in range(len(Com_Overhead_Avg_2))]
plt.plot(b3, Com_Overhead_Avg_1)
plt.plot(b3, Com_Overhead_Avg_2)
plt.plot(b3, Com_Overhead_Avg_3)
plt.title("Overhead")
plt.xlabel("Com Number")
plt.ylabel("Density") 
plt.show()

txtName = "CO_Avg_1.txt"
f = open(txtName, "a+")
for p in range(len(Com_Overhead_Avg_1)):
    if p == (len(Com_Overhead_Avg_1) - 1):
        new_context = str(Com_Overhead_Avg_1[p])
    else:
        new_context = str(Com_Overhead_Avg_1[p]) + '\n'
    f.write(new_context)
f.close()  

txtName = "CO_CI_S_1.txt"
f = open(txtName, "a+")
for p in range(len(CI_S_1)):
    if p == (len(CI_S_1) - 1): 
        new_context = str(CI_S_1[p])
    else:
        new_context = str(CI_S_1[p]) + '\n'
    f.write(new_context)
f.close()  
 

txtName = "CO_Avg_2.txt"
f = open(txtName, "a+")
for p in range(len(Com_Overhead_Avg_2)):
    if p == (len(Com_Overhead_Avg_2) - 1):
        new_context = str(Com_Overhead_Avg_2[p])
    else:
        new_context = str(Com_Overhead_Avg_2[p]) + '\n'
    f.write(new_context)
f.close()  

txtName = "CO_CI_S_2.txt"
f = open(txtName, "a+")
for p in range(len(CI_S_2)):
    if p == (len(CI_S_2) - 1): 
        new_context = str(CI_S_2[p])
    else:
        new_context = str(CI_S_2[p]) + '\n'
    f.write(new_context)
f.close()  
 

txtName = "CO_Avg_3.txt"
f = open(txtName, "a+")
for p in range(len(Com_Overhead_Avg_3)):
    if p == (len(Com_Overhead_Avg_3) - 1):
        new_context = str(Com_Overhead_Avg_3[p])
    else:
        new_context = str(Com_Overhead_Avg_3[p]) + '\n'
    f.write(new_context)
f.close()  

txtName = "CO_CI_S_3.txt"
f = open(txtName, "a+")
for p in range(len(CI_S_3)):
    if p == (len(CI_S_3) - 1): 
        new_context = str(CI_S_3[p])
    else:
        new_context = str(CI_S_3[p]) + '\n'
    f.write(new_context)
f.close()  





