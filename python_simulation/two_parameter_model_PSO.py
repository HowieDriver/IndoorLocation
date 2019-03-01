# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import numpy as np
import matplotlib.pyplot as plt
from pylab import *     #支持中文显示和负号
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
np.set_printoptions(suppress=True)#禁止科学计数法显示结果
# 目标函数定义，x中每个元素对应一个参数
def ras(absolute_x, absolute_y, d2, parameter, NumberOfAnchorNode):
    y = 0
    for i in range(NumberOfAnchorNode):
        t = np.square((np.square( parameter[0] - absolute_x[i] ) + np.square( parameter[1] - absolute_y[i] ) )**0.5
                - (d2[i])**0.5 )
        y += t
    y /= 5
    y = y**0.5
    return y

def fin_pso(absolute_x, absolute_y, distrection2, target_x, target_y, NumberOfAnchorNode):
    MumberOfparm = 2 #参数个数
    diff_x = sum(absolute_x) / len(absolute_x)
    diff_y = sum(absolute_y) / len(absolute_y)
    base_x = target_x + diff_x
    base_y = target_y + diff_y

    # 参数初始化
    w = 1.0
    c1 = 1.49445
    c2 = 1.49445

    maxgen = 200  # 进化次数
    sizepop = 200  # 种群规模,群体较小时容易陷入局部最优解
                    #群体较大当数目到一定程度优化变化不明显

    # 粒子速度和位置的范围
    Vmax =  1
    Vmin = -1
    popmax = [ 5,  5]
    popmin = [-5, -5]

    # 产生初始粒子和速度
    pop = 5 * np.random.uniform(-1, 1, (MumberOfparm, sizepop))
    pop[0][0] = base_x
    pop[1][0] = base_y

    pop[0][1] = base_x + 2.5
    pop[1][1] = base_y + 2.5
    pop[0][2] = base_x + 2.5
    pop[1][2] = base_y
    pop[0][3] = base_x
    pop[1][3] = base_y + 2.5

    pop[0][4] = base_x - 2.5
    pop[1][4] = base_y - 2.5
    pop[0][5] = base_x - 2.5
    pop[1][5] = base_y
    pop[0][6] = base_x
    pop[1][6] = base_y - 2.5

    v = np.random.uniform(-1, 1, (MumberOfparm, sizepop))

    fitness = ras(absolute_x, absolute_y, distrection2, pop, NumberOfAnchorNode)  # 计算适应度
    i = np.argmin(fitness)  # 找最好的个体
    gbest = pop  # 记录个体最优位置，第一次就是最好
    zbest = pop[:, i]  # 记录群体最优位置
    fitnessgbest = fitness  # 个体最佳适应度值
    fitnesszbest = fitness[i]  # 全局最佳适应度值

    # 迭代寻优
    t = 0
    record = np.zeros(maxgen)
    while t < maxgen:

        # 速度更新
        v = w * v + c1 * np.random.random() * (gbest - pop) + c2 * np.random.random() * (zbest.reshape(2, 1) - pop)
        v[v > Vmax] = Vmax  # 限制速度
        v[v < Vmin] = Vmin

        # 位置更新
        pop = pop + v

        for jj in range(MumberOfparm):
            for j in range(sizepop):
                if pop[jj][j] > popmax[jj]:
                    pop[jj][j] = popmax[jj]
                if pop[jj][j] < popmin[jj]:
                    pop[jj][j] = popmin[jj]

        # 自适应变异
        p = np.random.random()             # 随机生成一个0~1内的数
        if p > 0.8:                          # 如果这个数落在变异概率区间内，则进行变异处理
            k = np.random.randint(0, MumberOfparm)     # 在[0,MumberOfparm)之间随机选一个整数
            pop[:, k] = np.random.random()  # 在选定的位置进行变异

        # 计算适应度值
        fitness = ras(absolute_x, absolute_y, distrection2, pop, NumberOfAnchorNode)
        # 个体最优位置更新
        index = fitness < fitnessgbest
        fitnessgbest[index] = fitness[index]
        gbest[:, index] = pop[:, index]

        # 群体最优更新
        j = np.argmin(fitness)
        if fitness[j] < fitnesszbest:
            zbest = pop[:, j]
            fitnesszbest = fitness[j]

        record[t] = fitnesszbest  # 记录群体最优位置的变化
        t = t + 1

    # 结果分析
    plt.plot(record, 'b-')
    plt.xlabel(u'迭代次数')
    plt.ylabel(u'适应度')
    plt.title(u'适应度曲线')
    plt.show()
    return zbest, record[t-1]
