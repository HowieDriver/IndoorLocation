#coding:utf-8
import random

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from compiler.ast import flatten

from plot import getDist

def InitX():
    X = []
    x = []
    y = []
    mu, sigma = 0, 20
    for i in range(4):
        xt= random.gauss(mu, sigma)
        yt= random.gauss(mu, sigma)
        temp = []
        temp.append(xt)
        temp.append(yt)
        x.append(xt)
        y.append(yt)
        X.append(temp)
    print x
    print y
    print X
    plt.scatter(x, y, color='blue')  # 离散点
    plt.show()



def test(D, X):
    D = np.mat(D)
    X = np.mat(X)

    print "before =", D
    D2 = np.multiply(D, D)
    print "after = ", D2



#非度量型多维标度画图
def scatterFigure():
    x = [0, 5, 10, 15, 20, 25]
    y = [2330, 4597, 389, 625, 34, 1832]
    plt.scatter(x, y, color = 'blue')#离散点
    plt.plot(x, y, color = 'green')#连接离散点
    plt.text(x[0], y[0], "BC", ha='right', va='top', fontsize=10)
    plt.text(x[0], y[0], y[0], ha='center', va='bottom', fontsize=10)

    plt.text(x[1], y[1], "CD", ha='right', va='top', fontsize=10)
    plt.text(x[1], y[1], y[1], ha='center', va='bottom', fontsize=10)

    plt.text(x[2], y[2], "BD", ha='right', va='top', fontsize=10)
    plt.text(x[2], y[2], y[2], ha='center', va='bottom', fontsize=10)

    plt.text(x[3], y[3], "AD", ha='right', va='top', fontsize=10)
    plt.text(x[3], y[3], y[3], ha='center', va='bottom', fontsize=10)

    plt.text(x[4], y[4], "AB", ha='right', va='top', fontsize=10)
    plt.text(x[4], y[4], y[4], ha='center', va='bottom', fontsize=10)

    plt.text(x[5], y[5], "AC", ha='right', va='top', fontsize=10)
    plt.text(x[5], y[5], y[5], ha='center', va='bottom', fontsize=10)
    plt.show()