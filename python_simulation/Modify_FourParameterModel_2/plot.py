#coding:utf-8
import random

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
np.set_printoptions(suppress=True)#阻止以科学计数法方式输出
def topk(mat,k):
    e_vals,e_vecs = np.linalg.eig(mat)
    sorted_indices = np.argsort(e_vals)
    return e_vals[sorted_indices[:-k-1:-1]],e_vecs[:,sorted_indices[:-k-1:-1]]

def addGaussNoise(x, mu, sigma):
    x += random.gauss(mu, sigma)
    return x

def getDist(x1, x2):
    x1 = np.array(x1)
    x2 = np.array(x2)
    t = x2-x1
    d = np.math.hypot(t[0], t[1])
    return d

def histFigure():
    mu, sigma = 0, 1
    sampleNo = 100
    np.random.seed(0)
    s = np.random.normal(mu, sigma, sampleNo)
    # print s
    plt.hist(s, bins=100, normed=True, color="green")
    plt.xlabel("x")
    plt.ylabel("y")
    a = 10
    plt.text(-2, 1, r'$\mu=0,\ \sigma=1$')#在x轴-4， y轴0.30开始加入说明
    string = "1234"
    plt.title(u"中文"+string)
    plt.show()

def subFigure():
    x = np.arange(-5.0, 5.0, 0.02)
    y1 = np.sin(x)
    plt.figure(1)
    plt.subplot(211)
    plt.axis([-5, 5, -2, 2])#设置x,y坐标范围
    plt.xlim((-3, 3))#另一种设置坐标区间的方法
    plt.plot(x, y1)

    plt.subplot(212)
    #设置x轴范围
    plt.xlim(-2.5, 2.5)
    #设置y轴范围
    plt.ylim(-1, 1)
    plt.plot(x, y1)
    plt.show()

def mulFigure():
    x = np.arange(0, 5, 0.2)
    y1 = x
    y2 = x**2 #平方
    y3 = x**3

    plt.plot(x, y1, 'r.', label="x")
    plt.plot(x, y2, 'bs', label="x^2")
    plt.plot(x, y3, 'g^', label="x^3")

    plt.legend(loc="upper left")
    plt.show()

def scatterFigure():
    x = np.random.uniform(1, 10, size=(1, 10))
    y = np.random.uniform(1, 10, size=(1, 10))
    print x
    print y
    plt.scatter(x, y, c = 'blue', marker  = 'v')#离散点
    #plt.plot(x, y, color = 'green')#连接离散点
    plt.show()

def gaussNoise():
    x = np.linspace(0, 2*np.pi, 100)
    y = np.sin(x)
    mu, sigma = 0, 0.05
    for i in range(x.size):
        x[i] += random.gauss(mu, sigma)
        y[i] += random.gauss(mu, sigma)
    print x
    print y
    plt.plot(x, y, "g.")
    plt.show()

def plotxy(anchor_x, anchor_y, target_x, target_y):

    actual_x = anchor_x
    actual_y = anchor_y
    actual_x.append(target_x)
    actual_y.append(target_y)
    plt.scatter(actual_x, actual_y, c='blue', marker='v')  # 离散点


    actual_x = []
    actual_y = []
    for i in range(4):
        actual_x.append(anchor_x[i])
        actual_y.append(anchor_y[i])
    actual_x.append(anchor_x[0])
    actual_y.append(anchor_y[0])
    plt.plot(actual_x, actual_y, color='green')  # 连接离散点

    actual_x = []
    actual_y = []
    actual_x.append(anchor_x[4])
    actual_y.append(anchor_y[4])
    actual_x.append(target_x)
    actual_y.append(target_y)
    plt.plot(actual_x, actual_y, color='green')  # 连接离散点

    actual_x = []
    actual_y = []
    actual_x.append(anchor_x[0])
    actual_y.append(anchor_y[0])
    actual_x.append(anchor_x[2])
    actual_y.append(anchor_y[2])
    plt.plot(actual_x, actual_y, color='green')  # 连接离散点

    actual_x = []
    actual_y = []
    actual_x.append(anchor_x[1])
    actual_y.append(anchor_y[1])
    actual_x.append(anchor_x[3])
    actual_y.append(anchor_y[3])
    plt.plot(actual_x, actual_y, color='green')  # 连接离散点
    plt.show()


def combination_k(s, k):
    if k == 0:
        return ['']
    subletters = []
    for i in range(len(s)):
        for letter in combination_k(s[i + 1:], k - 1):
            subletters += [s[i] + letter]
    return subletters

def splti(subletters):
    index3 = []
    for i in range(len(subletters)):
        temp = []
        isubletters = int(subletters[i])
        temp.append(isubletters / 100)
        temp.append(isubletters % 100 / 10)
        temp.append(isubletters % 10)
        index3.append(temp)
    return index3
# print splti(combination_k('12345', 3))
# histFigure()