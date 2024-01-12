"""
calculate distance and sector
@author: Jian Wang
"""
import math

def DS(N_1, N_2, Beam_Wid):
    SN = (2 * math.pi) / Beam_Wid
    N_1_x = N_1.location[0]
    N_1_y = N_1.location[1]
    
    N_2_x = N_2.location[0]
    N_2_y = N_2.location[1]
    
    
    #角度计算,以N_1为坐标原点
    Dis_N1_N2 = math.sqrt((N_1_x - N_2_x) ** 2 + (N_1_y - N_2_y) ** 2)    
    Dis_N1_N2_x = N_2_x - N_1_x
    
    if Dis_N1_N2_x != 0:
        Cos_Val = Dis_N1_N2_x / Dis_N1_N2
        
        if N_2_y >= N_1_y:
            Ang = math.acos(Cos_Val)
        else:
            Ang = 2 * math.pi - math.acos(Cos_Val)
        
        #扇区判断
        sec_Num = Ang / Beam_Wid
        sec_Num = math.ceil(sec_Num)
    elif N_2_y >= N_1_y:
        sec_Num = int(SN / 4)
        
    elif N_2_y < N_1_y:
        sec_Num = int((3 * SN) / 4)
        
    
    #print(type(sec_Num))
    #print(Dis_N1_N2, sec_Num)
    
    return Dis_N1_N2, sec_Num

