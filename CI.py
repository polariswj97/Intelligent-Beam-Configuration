"""
Created on Wed Dec 20 16:22:56 2023
Calculate confidence interval of 90%,95%,99%
Fail_Rate：数据集
Fail_Rate_Avg：均值
Fail_Rate_Var：标准差
KT：数据数量
RT：数据维度
D_OR_S：单边误差0；双边误差1
C_L：置信水平 [90%, 95%, 99] <---> [0,1,2]
@author: Jian Wang
"""
import math

def CI(Fail_Rate, Fail_Rate_Avg, Fail_Rate_Var, KT, RT, D_OR_S, C_L):    
    CI_UP = []
    CI_DOWN = []
    CI_S = []
    S_N = math.sqrt(KT)
    Z_L = [1.64, 1.96, 2.58]
    
    
    for r in range(RT):       
        FR_r = 0
        FR_r_avg = 0
        FR_r_var = 0       
        for k in range(KT):
            FR_r = FR_r + Fail_Rate[k][r]
            
        FR_r_avg = FR_r / KT
        
        for k in range(KT):
            FR_r_var = FR_r_var + (Fail_Rate[k][r] - FR_r_avg) ** 2
            
        FR_r_var = math.sqrt(FR_r_var / KT)
        
        Fail_Rate_Avg.append(FR_r_avg)
        Fail_Rate_Var.append(FR_r_var)
        
        ERR_S = Z_L[C_L] * (FR_r_var / S_N)
        
        CI_S.append(ERR_S)
        
        CI_UP.append(FR_r_avg + ERR_S)
        CI_DOWN.append(FR_r_avg - ERR_S)
    
    if D_OR_S == 0:
        return CI_S
    elif D_OR_S == 1:
        return CI_UP, CI_DOWN
    else:
        print("error")
        return 0
        
