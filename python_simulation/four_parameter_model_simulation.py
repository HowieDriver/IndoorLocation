#coding:utf-8
import random

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from compiler.ast import flatten
from plot import getDist
from plot import topk
from plot import addGaussNoise
from four_parameter_model_PSO import fin_pso

def relativeToabsl(parameter, relative_x, relative_y):
    ret_x = (1 + parameter[0]) * relative_x * np.cos(parameter[1]) \
                  - (1 + parameter[0]) * relative_y * np.sin(parameter[1]) + parameter[2]
    ret_y = (1 + parameter[0]) * relative_x * np.sin(parameter[1]) \
                  + (1 + parameter[0]) * relative_y * np.cos(parameter[1]) + parameter[3]
    return ret_x, ret_y

#实际分布图
def actualFigure():
    plt.scatter(anchor_x, anchor_y, color = 'green', marker= 'o')#离散点
    plt.scatter(target_x, target_y, color='blue', marker='^')  # 离散点
    plt.scatter(target_absl_array_x, target_absl_array_y, color='red', marker='s')  # 离散点
    plt.show()


np.set_printoptions(suppress=True)
NumberOfTargetNode = 10
NumberOfAnchorNode = 5
NumberOfTotalNode = NumberOfAnchorNode+1
anchor_x = [-5,  0, 5,   0, 0]
anchor_y = [  0, 5,  0, -5, 0]
target_x = np.random.uniform(-5, 5, size=(NumberOfTargetNode))#随机生成50个数，范围在-5到5
target_y = np.random.uniform(-5, 5, size=(NumberOfTargetNode))

#根据实际坐标生成模拟的距离阵
P = [[  0,  50, 100,  50,  25, 1],
     [ 50,   0,  50, 100,  25, 1],
     [100,  50,   0,  50,  25, 1],
     [ 50, 100,  50,   0,  25, 1],
     [ 25,  25,  25,  25,  0,  1],
     [  1,   1,   1,   1,  1,  0]]

target_absl_array_x = []
target_absl_array_y = []
for i in range (10):
    print "#########################################"
    print i
    D2 = []
    for j in range(NumberOfAnchorNode):
        d = getDist([target_x[i], target_y[i]], [anchor_x[j], anchor_y[j]])
        #d = addGaussNoise(d)
        D2.append(d*d)
    for k in range(NumberOfAnchorNode):
        P[k][NumberOfAnchorNode] = D2[k]
    for k in range(NumberOfAnchorNode):
        P[NumberOfAnchorNode][k] = D2[k]

    D2 = np.mat(P)
    E = np.mat(np.eye(NumberOfTotalNode, NumberOfTotalNode, dtype=int))
    l = np.mat(np.ones((NumberOfTotalNode, 1)))
    I = l * (l.T)
    H = E - (1.0/NumberOfTotalNode) * I
    B = -0.5 * H * D2 * H
    vals, vecs = topk(B, 2)
    # print "vals="
    # print vals
    # print "vecs="
    # print vecs
    eigvalsMat = np.mat(np.diag(np.sqrt(vals)))
    Loc = vecs * eigvalsMat
    #print Loc

    x = Loc[:, 0]
    y = Loc[:, 1]
    x = np.array(x)
    y = np.array(y)
    x = x.flatten()
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

    plt.text(x[0], y[0], "A", ha='right', va='top', fontsize=10)
    plt.text(x[1], y[1], "B", ha='right', va='top', fontsize=10)
    plt.text(x[2], y[2], "C", ha='right', va='top', fontsize=10)
    plt.text(x[3], y[3], "D", ha='right', va='top', fontsize=10)
    plt.text(x[4], y[4], "E", ha='right', va='top', fontsize=10)
    plt.show()

    target_realtive_x = x[5]
    target_realtive_y = y[5]
    parm, diff = fin_pso(anchor_x, anchor_y, x[0:5], y[0:5])
    # # 结果分析
    # print "群体最优解："
    # print parm
    print "最小Difference值："
    print diff
    target_absl_x, target_absl_y = relativeToabsl(parm, target_realtive_x, target_realtive_y)

    print "target_absl_xy=", target_absl_x, target_absl_y
    print "target_real_xy=", target_x[i], target_y[i]
    target_absl_array_x.append(target_absl_x)
    target_absl_array_y.append(target_absl_y)



#actualFigure()