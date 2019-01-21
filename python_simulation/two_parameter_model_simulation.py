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



#实际分布图
def actualFigure():
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
    print "RMSE=", RMSE
    plt.show()

NumberOfTargetNode =50
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
        d = addGaussNoise(d, 0, 0.4) #添加均值为0， 标准差为1的高斯噪声
        d2.append(d*d)
    for k in range(NumberOfAnchorNode):
        P[k][NumberOfAnchorNode] = d2[k]
    for k in range(NumberOfAnchorNode):
        P[NumberOfAnchorNode][k] = d2[k]

    D2 = np.mat(P)
    E = np.mat(np.eye(NumberOfTotalNode, NumberOfTotalNode, dtype=int))
    l = np.mat(np.ones((NumberOfTotalNode, 1)))
    I = l * (l.T)
    H = E - (1.0/NumberOfTotalNode) * I
    B = -0.5 * H * D2 * H

    vals, vecs = topk(B, 2)#特征分解，提取特征值最大的两个特征值和特征向量
    eigvalsMat = np.mat(np.diag(np.sqrt(vals)))
    Loc = vecs * eigvalsMat

    x = Loc[:, 0]
    y = Loc[:, 1]
    x = np.array(x)
    y = np.array(y)
    x = x.flatten() #矩阵降维
    y = y.flatten()
    plt.scatter(x, y, color='blue')

    # #画出点之间的连线
    plt.plot(x, y, color='green')
    xt = []
    xt.append(x[0])
    xt.append(x[3])
    yt = []
    yt.append(y[0])
    yt.append(y[3])
    plt.plot(xt, yt, color='green')
    xt = []
    xt.append(x[0])
    xt.append(x[2])
    yt = []
    yt.append(y[0])
    yt.append(y[2])
    plt.plot(xt, yt, color='green')
    xt = []
    xt.append(x[1])
    xt.append(x[3])
    yt = []
    yt.append(y[1])
    yt.append(y[3])
    plt.plot(xt, yt, color='green')

    #给多维标度产生的锚节点标记A, B, C, D, E标记
    plt.text(x[0], y[0], "A", ha='right', va='top', fontsize=10)
    plt.text(x[1], y[1], "B", ha='right', va='top', fontsize=10)
    plt.text(x[2], y[2], "C", ha='right', va='top', fontsize=10)
    plt.text(x[3], y[3], "D", ha='right', va='top', fontsize=10)
    plt.text(x[4], y[4], "E", ha='right', va='top', fontsize=10)
    plt.show()

    target_realtive_x = x[5]
    target_realtive_y = y[5]
    parm, diff = fin_pso(anchor_x, anchor_y, d2, target_realtive_x, target_realtive_y)
    # 结果分析
    # print "群体最优解："
    # print parm
    print "最小Difference值："
    print diff

    print "target_parm_xy=", parm[0], parm[1]
    print "target_real_xy=", target_x[i], target_y[i]

    parm_array_x.append(parm[0])
    parm_array_y.append(parm[1])


actualFigure()