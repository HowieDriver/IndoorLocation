#coding:utf-8
import random

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from compiler.ast import flatten
from plot import getDist
from plot import topk
from plot import addGaussNoise
from two_parameter_model_PSO import fin_pso
from mds import mds_fun

def getLocAfterPSO(P, d2):
    Loc, x, y = mds_fun(P)
    target_realtive_x = x[5]
    target_realtive_y = y[5]
    parm, diff = fin_pso(anchor_x, anchor_y, d2, target_realtive_x, target_realtive_y)
    return parm, diff
#实际分布图
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
barier_d2 = 100 #给某两点之间加上障碍物的值
NumberOfTotalNode = NumberOfAnchorNode+1
np.set_printoptions(suppress=True)#禁止科学计数法显示结果
anchor_x = [-5,  0, 5,   0, 0]
anchor_y = [  0, 5,  0, -5, 0]
target_x = np.random.uniform(-5, 5, size=(NumberOfTargetNode))#随机生成NumberOfTargetNode个数，范围在-5到5
target_y = np.random.uniform(-5, 5, size=(NumberOfTargetNode))
parm_array_x = [] #利用粒子群优化得出目标点的坐标
parm_array_y = []
parm_array_barier_x = []
parm_array_barier_y = []

#根据实际坐标生成模拟的距离阵
P = [[  0,  50, 100,  50,  25, 1],
     [ 50,   0,  50, 100,  25, 1],
     [100,  50,   0,  50,  25, 1],
     [ 50, 100,  50,   0,  25, 1],
     [ 25,  25,  25,  25,  0,  1],
     [  1,   1,   1,   1,  1,  0]]
P_barier = P
for i in range (NumberOfTargetNode):
    print i
    d2 = [] #目标节点到锚节点的距离平方
    d2_barier = []
    for j in range(NumberOfAnchorNode):
        d = getDist([target_x[i], target_y[i]], [anchor_x[j], anchor_y[j]])
        # d = addGaussNoise(d, 0, 0.4) #添加均值为0， 标准差为1的高斯噪声
        d2.append(d*d)
        d2_barier.append(d * d)
    i_barier = np.random.randint(0, NumberOfAnchorNode)
    d2_barier[i_barier] += barier_d2
    for k in range(NumberOfAnchorNode):
        P[k][NumberOfAnchorNode] = d2[k]
        P_barier[k][NumberOfAnchorNode] = d2_barier[k]
    for k in range(NumberOfAnchorNode):
        P[NumberOfAnchorNode][k] = d2[k]
        P_barier[NumberOfAnchorNode][k] = d2_barier[k]

    parm, diff = getLocAfterPSO(P, d2)
    parm_barier, diff_barier = getLocAfterPSO(P_barier, d2_barier)
    print "无障碍物最小Difference值："
    print diff
    print "有障碍物最小Difference值："
    print diff_barier
    # print "实际坐标：", target_x[i], target_y[i]
    # print "无障碍物定位坐标", parm[0], parm[1]
    # print "有障碍物定位坐标=", parm_barier[0], parm_barier[1]


    parm_array_x.append(parm[0])
    parm_array_y.append(parm[1])
    parm_array_barier_x.append(parm_barier[0])
    parm_array_barier_y.append(parm_barier[1])


RMSE = actualFigure(anchor_x, anchor_y, target_x, target_y, parm_array_x, parm_array_y)
RMSE_barrier = actualFigure(anchor_x, anchor_y, target_x, target_y, parm_array_barier_x, parm_array_barier_y)
print "RMSE=", RMSE
print "RMSE_barrier=", RMSE_barrier