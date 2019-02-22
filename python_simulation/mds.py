#coding:utf-8
import random

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from compiler.ast import flatten
from plot import topk
NumberOfTotalNode = 6
import plot
def mds_fun(P):
    D2 = np.mat(P)
    E = np.mat(np.eye(NumberOfTotalNode, NumberOfTotalNode, dtype=int))
    l = np.mat(np.ones((NumberOfTotalNode, 1)))
    I = l * (l.T)
    H = E - (1.0 / NumberOfTotalNode) * I
    B = -0.5 * H * D2 * H

    vals, vecs = topk(B, 2)  # 特征分解，提取特征值最大的两个特征值和特征向量
    eigvalsMat = np.mat(np.diag(np.sqrt(vals)))
    Loc = vecs * eigvalsMat

    x = Loc[:, 0]
    y = Loc[:, 1]
    x = np.array(x)
    y = np.array(y)
    x = x.flatten()  # 矩阵降维
    y = y.flatten()
    # plt.scatter(x, y, color='blue')
    #
    # # #画出点之间的连线
    # plt.plot(x, y, color='green')
    # xt = []
    # xt.append(x[0])
    # xt.append(x[3])
    # yt = []
    # yt.append(y[0])
    # yt.append(y[3])
    # plt.plot(xt, yt, color='green')
    # xt = []
    # xt.append(x[0])
    # xt.append(x[2])
    # yt = []
    # yt.append(y[0])
    # yt.append(y[2])
    # plt.plot(xt, yt, color='green')
    # xt = []
    # xt.append(x[1])
    # xt.append(x[3])
    # yt = []
    # yt.append(y[1])
    # yt.append(y[3])
    # plt.plot(xt, yt, color='green')
    #
    # # 给多维标度产生的锚节点标记A, B, C, D, E标记
    # plt.text(x[0], y[0], "A", ha='right', va='top', fontsize=10)
    # plt.text(x[1], y[1], "B", ha='right', va='top', fontsize=10)
    # plt.text(x[2], y[2], "C", ha='right', va='top', fontsize=10)
    # plt.text(x[3], y[3], "D", ha='right', va='top', fontsize=10)
    # plt.text(x[4], y[4], "E", ha='right', va='top', fontsize=10)
    # plt.show()

    return Loc, x, y