"""
Created on Mon Dec  4 16:29:08 2023
@author: Jian Wang
"""
import math
import random
import matplotlib.pyplot as plt
from CI import CI
import datetime

Device_Num = 10
Lambda = 0.0006
T = 100
KT = 600
RT = []
RT = []
#for i in range(0,96,5):
    #RT.append(i)
RT = [[0,5,10,20,30,40,50,60,95],[0,10,20,30,40,50,60,70,95],[0,20,30,40,50,60,70,80,95]]

class Node():
    def __init__(self, index):
        self.index = index
        self.if_central_node = 0
        self.if_fail = 0
    
    def fail_check(self, t, k):
        P_t_k = ((math.exp(-Lambda * t)) * ((Lambda * t) ** k)) / math.factorial(k)
        if random.random() > P_t_k:
            self.if_fail = 1
            

#create node
Node_List = []
for index in range(Device_Num):
    Node_List.append(Node(index))

#fix central node
CI_S_1 = []

Fail_Rate_Avg_1 = []
Fail_Rate_Var_1 = []
Node_List[0].if_central_node = 1

Fail_Rate_1 = []
for k in range(KT):#100 times
    Fail_Rate_One = [0 for j in range(len(RT[0]))] #save fail rate in one round
    for i in range(10):
        for r in range(len(RT[0])):
            Node_List[0].if_fail = 0
            Node_List[0].fail_check(RT[0][r] * T, 0)
            if Node_List[0].if_fail == 1:
                Fail_Rate_One[r] = Fail_Rate_One[r] + 1
    for j in range(len(RT[0])):
        Fail_Rate_One[j] = Fail_Rate_One[j] / 10
    if k == 1:
        print(Fail_Rate_One)
        print(sum(Fail_Rate_One))
    Fail_Rate_1.append(Fail_Rate_One)

#compute confidence interval
CI_S_1 = CI(Fail_Rate_1, Fail_Rate_Avg_1, Fail_Rate_Var_1, KT, len(RT[0]), 0, 2)


#non-fix central node
CI_S_2 = []

Fail_Rate_Avg_2 = []
Fail_Rate_Var_2 = []
Node_List[0].if_central_node = 1
Node_List[1].if_central_node = 1

Fail_Rate_2 = []
for k in range(KT):#100 times
    Fail_Rate_Two = [0 for j in range(len(RT[1]))] #save fail rate in one round
    for i in range(10):
        for r in range(len(RT[1])):
            Node_List[0].if_fail = 0
            Node_List[1].if_fail = 0
            Node_List[0].fail_check(RT[1][r] * T, 0)
            Node_List[1].fail_check(RT[1][r] * T, 0)
            if (Node_List[0].if_fail == 1) and (Node_List[1].if_fail == 1):
                Fail_Rate_Two[r] = Fail_Rate_Two[r] + 1
    for j in range(len(RT[1])):
        Fail_Rate_Two[j] = Fail_Rate_Two[j] / 10
    if k == 1:
        print(Fail_Rate_Two)
        print(sum(Fail_Rate_Two))
    Fail_Rate_2.append(Fail_Rate_Two)   

CI_S_2 = CI(Fail_Rate_2, Fail_Rate_Avg_2, Fail_Rate_Var_2, KT, len(RT[1]), 0, 2)
        
#no central node
CI_S_3 = []

Fail_Rate_Avg_3 = []
Fail_Rate_Var_3 = []
for n in Node_List:
    n.if_central_node = 1

Fail_Rate_3 = []
for k in range(KT):#100 times
    Fail_Rate_Three = [0 for j in range(len(RT[2]))] #save fail rate in one round
    for i in range(10):
        for r in range(len(RT[2])):
            for n in Node_List:
                n.if_fail = 0
            fail_num = 0
            for n in Node_List:
                n.fail_check(RT[2][r] * T, 0)
                if n.if_fail == 1:
                    fail_num = fail_num + 1            
            if fail_num == Device_Num:
                Fail_Rate_Three[r] = Fail_Rate_Three[r] + 1
    for j in range(len(RT[2])):
        Fail_Rate_Three[j] = Fail_Rate_Three[j] / 10
    if k == 1:
        print(Fail_Rate_Three)
        print(sum(Fail_Rate_Three))
    Fail_Rate_3.append(Fail_Rate_Three)  

CI_S_3 = CI(Fail_Rate_3, Fail_Rate_Avg_3, Fail_Rate_Var_3, KT, len(RT[2]), 0, 2)

print('plot')
plt.figure()
b3 = [i+1 for i in range(len(Fail_Rate_Avg_3))]
plt.plot(b3, Fail_Rate_Avg_1)
plt.plot(b3, Fail_Rate_Avg_2)
plt.plot(b3, Fail_Rate_Avg_3)
plt.title("Fail Rate")
plt.xlabel("Com Round")
plt.ylabel("Fail Rate") 
plt.show()

DT = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

txtName = "Fail_Rate_Avg_1.txt"
f = open(txtName, "a+")
for p in range(len(Fail_Rate_Avg_1)):
    if p == (len(Fail_Rate_Avg_1) - 1):
        new_context = str(Fail_Rate_Avg_1[p])
    else:
        new_context = str(Fail_Rate_Avg_1[p]) + '\n'
    f.write(new_context)
f.close()

txtName = "Fail_Rate_CIS_1.txt"
f = open(txtName, "a+")
for p in range(len(CI_S_1)):
    if p == (len(CI_S_1) - 1):
        new_context = str(CI_S_1[p])
    else:
        new_context = str(CI_S_1[p]) + '\n'
    f.write(new_context)
f.close() 

    
txtName = "Fail_Rate_Avg_2.txt"
f = open(txtName, "a+")
for p in range(len(Fail_Rate_Avg_2)):
    if p == (len(Fail_Rate_Avg_2) - 1):
        new_context = str(Fail_Rate_Avg_2[p])
    else:
        new_context = str(Fail_Rate_Avg_2[p]) + '\n'
    f.write(new_context)
f.close()

txtName = "Fail_Rate_CIS_2.txt"
f = open(txtName, "a+")
for p in range(len(CI_S_2)):
    if p == (len(CI_S_2) - 1):
        new_context = str(CI_S_2[p])
    else:
        new_context = str(CI_S_2[p]) + '\n'
    f.write(new_context)
f.close() 


txtName = "Fail_Rate_Avg_3.txt"
f = open(txtName, "a+")
for p in range(len(Fail_Rate_Avg_3)):
    if p == (len(Fail_Rate_Avg_3) - 1):
        new_context = str(Fail_Rate_Avg_3[p])
    else:
        new_context = str(Fail_Rate_Avg_3[p]) + '\n'
    f.write(new_context)
f.close()

txtName = "Fail_Rate_CIS_3.txt"
f = open(txtName, "a+")
for p in range(len(CI_S_3)):
    if p == (len(CI_S_3) - 1):
        new_context = str(CI_S_3[p])
    else:
        new_context = str(CI_S_3[p]) + '\n'
    f.write(new_context)
f.close() 


            
        

    

    
    

