#!/usr/bin/python
#coding:utf-8
import random
import time
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
import socket
from compiler.ast import flatten
from two_parameter_model_PSO import fin_pso
from mds import mds_fun
from plot import getDist
import warnings
warnings.filterwarnings("ignore")
def getLocAfterPSO(P, d2):
    Loc, x, y = mds_fun(P)
    target_realtive_x = x[5]
    target_realtive_y = y[5]
    parm, diff = fin_pso(anchor_x, anchor_y, d2, target_realtive_x, target_realtive_y)
    return parm, diff

np.set_printoptions(suppress=True)#禁止科学计数法显示结果
anchor_x = [-5,  0, 5,   0, 0]
anchor_y = [  0, 5,  0, -5, 0]
NumberOfAnchorNode = 5
NumberOfTotalNode = NumberOfAnchorNode+1
try:
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    sock.bind(('192.168.1.125',21567))
    sock.listen(5)
except:
    print("init socket error!")

while True:
    conn,addr=sock.accept()
    conn.settimeout(30)
    szBuf=conn.recv(1024)
    print "From app:", szBuf
    s = szBuf.split(';')
    d2 = []
    for i in range(5):
        t = s[i].split('-')
        d2.append(int(t[1])) 
    #print d2  
    #根据实际坐标生成模拟的距离阵
    P = [[  0,  50, 100,  50,  25, 1],
	     [ 50,   0,  50, 100,  25, 1],
	     [100,  50,   0,  50,  25, 1],
	     [ 50, 100,  50,   0,  25, 1],
	     [ 25,  25,  25,  25,  0,  1],
	     [  1,   1,   1,   1,  1,  0]]

    for k in range(NumberOfAnchorNode):
        P[k][NumberOfAnchorNode] = d2[k]
    for k in range(NumberOfAnchorNode):
        P[NumberOfAnchorNode][k] = d2[k]

    parm, diff = getLocAfterPSO(P, d2)
    #print "最小Difference值："
    #print diff
    #print "实际坐标：", target_x, target_y
    print "发送定位结果", parm[0], parm[1]
    print "\n"
	
    s = "xy:"+str(round(parm[0],4))+","+str(round(parm[1],4))
    conn.send(s)
    time.sleep(0.1)
    conn.close()




'''
target_x = 2.0
target_y = 2.0
d2 = [] #目标节点到锚节点的距离平方
for j in range(NumberOfAnchorNode):
	d = getDist([target_x, target_y], [anchor_x[j], anchor_y[j]])
	d2.append(d*d)
print "d2=",d2
'''

