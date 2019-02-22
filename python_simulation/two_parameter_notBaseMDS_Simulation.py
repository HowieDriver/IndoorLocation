#coding:utf-8
import random

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from compiler.ast import flatten
from plot import getDist
from plot import topk
from plot import addGaussNoise
from two_parameter_notBased_PSO_MDS import fin_pso

def actualFigure(anchor_x, anchor_y, target_x, target_y, parm_array_x, parm_array_y):
    RMSE = 0
    plt.scatter(anchor_x, anchor_y, color = 'blue', marker= 's')#离散点
    plt.scatter(target_x, target_y, color='green', marker='^')  # 离散点
    plt.scatter(parm_array_x, parm_array_y, color='red', marker='o')  # 离散点

    for i in range(NumberOfTargetNode):
        tx = []
        tx.append(parm_array_x[i])
        tx.append(target_x[i])
        ty = []
        ty.append(parm_array_y[i])
        ty.append(target_y[i])
        plt.plot(tx, ty, color='black')

        diffD = (parm_array_x[i] - target_x[i])**2 + (parm_array_y[i] - target_y[i])**2
        RMSE += diffD
    RMSE = (RMSE/NumberOfTargetNode)**0.5
    #print "RMSE=", RMSE
    plt.show()
    return RMSE

NumberOfTargetNode = 10
NumberOfAnchorNode = 5
NumberOfTotalNode = NumberOfAnchorNode+1
np.set_printoptions(suppress=True)#禁止科学计数法显示结果
anchor_x = [-5,  0, 5,   0, 0]
anchor_y = [  0, 5,  0, -5, 0]
target_x = np.random.uniform(-5, 5, size=(NumberOfTargetNode))#随机生成NumberOfTargetNode个数，范围在-5到5
target_y = np.random.uniform(-5, 5, size=(NumberOfTargetNode))
parm_array_x = [] #利用粒子群优化得出目标点的坐标
parm_array_y = []
#根据实际坐标生成模拟的距离阵
P = [[  0,  50, 100,  50,  25, 1],
     [ 50,   0,  50, 100,  25, 1],
     [100,  50,   0,  50,  25, 1],
     [ 50, 100,  50,   0,  25, 1],
     [ 25,  25,  25,  25,  0,  1],
     [  1,   1,   1,   1,  1,  0]]

for i in range (NumberOfTargetNode):
    print i
    d2 = [] #目标节点到锚节点的距离平方
    for j in range(NumberOfAnchorNode):
        d = getDist([target_x[i], target_y[i]], [anchor_x[j], anchor_y[j]])
        d = addGaussNoise(d, 0, 1) #添加均值为0， 标准差为1的高斯噪声
        d2.append(d*d)
    for k in range(NumberOfAnchorNode):
        P[k][NumberOfAnchorNode] = d2[k]
    for k in range(NumberOfAnchorNode):
        P[NumberOfAnchorNode][k] = d2[k]


    parm, diff = fin_pso(anchor_x, anchor_y, d2)
    # 结果分析
    # print "群体最优解："
    # print parm
    print "最小Difference值："
    print diff

    print "target_parm_xy=", parm[0], parm[1]
    print "target_real_xy=", target_x[i], target_y[i]

    parm_array_x.append(parm[0])
    parm_array_y.append(parm[1])


RMSE = actualFigure(anchor_x, anchor_y, target_x, target_y, parm_array_x, parm_array_y)
print "RMSE=", RMSE