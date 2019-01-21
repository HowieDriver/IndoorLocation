# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import numpy as np
import matplotlib.pyplot as plt


# 目标函数定义，x中每个元素对应一个参数
def ras(absolute_x, absolute_y, relative_x, relative_y, parameter):
    y = 0
    for i in range(5):
        t = np.square( (1+parameter[0]) * relative_x[i] * np.cos(parameter[1]) \
                     - (1+parameter[0]) * relative_y[i] * np.sin(parameter[1]) + parameter[2] - absolute_x[i] )\
            + np.square( (1+parameter[0]) * relative_x[i] * np.sin(parameter[1]) \
                     + (1+parameter[0]) * relative_y[i] * np.cos(parameter[1]) + parameter[3] - absolute_y[i] )
        y += t
    return y

def fin_pso(absolute_x, absolute_y, relative_x, relative_y):
    MumberOfparm = 4
    # 参数初始化
    w = 1.0
    c1 = 1.49445
    c2 = 1.49445

    maxgen = 2000  # 进化次数
    sizepop = 500  # 种群规模,群体较小时容易陷入局部最优解
                    #群体较大当数目到一定程度优化变化不明显

    # 粒子速度和位置的范围
    Vmax = 1
    Vmin = -1
    popmax = [ 2,  np.pi,  5,  5]
    popmin = [-2, -np.pi, -5, -5]

    # 产生初始粒子和速度
    pop = np.random.uniform(-1, 1, (MumberOfparm, sizepop))
    pop[0] *= 2
    pop[1] *= np.pi
    pop[2] *= 5
    pop[3] *= 5
    v = np.random.uniform(-1, 1, (MumberOfparm, sizepop))

    fitness = ras(absolute_x, absolute_y, relative_x, relative_y, pop)  # 计算适应度
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
        v = w * v + c1 * np.random.random() * (gbest - pop) + c2 * np.random.random() * (zbest.reshape(4, 1) - pop)
        v[v > Vmax] = Vmax  # 限制速度
        v[v < Vmin] = Vmin

        # 位置更新
        pop = pop + 0.5 * v;
        for jj in range(MumberOfparm):
            for j in range(sizepop):
                if pop[jj][j] > popmax[jj]:
                    pop[jj][j] = popmax[jj]
                if pop[jj][j] < popmin[jj]:
                    pop[jj][j] = popmin[jj]

        # 自适应变异
        p = np.random.random()             # 随机生成一个0~1内的数
        if p > 0.8:                          # 如果这个数落在变异概率区间内，则进行变异处理
            k = np.random.randint(0,MumberOfparm)     # 在[0,2)之间随机选一个整数
            pop[:,k] = np.random.random()  # 在选定的位置进行变异


        # 计算适应度值
        fitness = ras(absolute_x, absolute_y, relative_x, relative_y, pop)

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
    # plt.plot(record, 'b-')
    # plt.xlabel('generation')
    # plt.ylabel('fitness')
    # plt.title('fitness curve')
    # plt.show()
    return zbest,record[t-1]
