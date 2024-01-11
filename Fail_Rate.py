"""
Created on Tue May 16 14:56:42 2023

@author: Jian Wang
"""

import math
import matplotlib.pyplot as plt
import datetime


Device_num = 10
Lambda = 0.0006
T = 100
Round = []

for i in range(0,96):
    Round.append(i)
#Round = [[0,5,10,20,30,40,50,60,95],[0,10,20,30,40,50,60,70,95],[0,20,30,40,50,60,70,80,95]]

def Poisson(t, k):
    P_t_k = ((math.exp(-Lambda * t)) * ((Lambda * t) ** k)) / math.factorial(k)
    return P_t_k

Fail1 = []
Fail2 = []
Fail3 = []

for i in Round:
    Fail1.append(1 - Poisson(i * T, 0))
for i in Round:
    Fail2.append((1 - Poisson(i * T, 0)) ** 2)
for i in Round:
    Fail3.append((1 - Poisson(i * T, 0)) ** Device_num)   
print(Fail3)

plt.figure()
b3 = [i+1 for i in range(len(Fail1))]
plt.plot(b3, Fail1)
plt.plot(b3, Fail2)
plt.plot(b3, Fail3)
plt.title("Fail Rate")
plt.xlabel("Com Round")
plt.ylabel("Fail Rate") 
plt.show()

DT = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

txtName = "Fail_Rate_Central.txt"
f = open(txtName, "a+")
for p in range(len(Fail1)):
    if p == (len(Fail1) - 1):
        new_context = str(Fail1[p])
    else:
        new_context = str(Fail1[p]) + '\n'
    f.write(new_context)
f.close()    

txtName = "Fail_Rate_Selection.txt"
f = open(txtName, "a+")
for p in range(len(Fail2)):
    if p == (len(Fail2) - 1):
        new_context = str(Fail2[p])
    else:
        new_context = str(Fail2[p]) + '\n'
    f.write(new_context)
f.close()    

txtName = "Fail_Rate_Discentral.txt"
f = open(txtName, "a+")
for p in range(len(Fail3)):
    if p == (len(Fail3) - 1):
        new_context = str(Fail3[p])
    else:
        new_context = str(Fail3[p]) + '\n'
    f.write(new_context)
f.close()    

