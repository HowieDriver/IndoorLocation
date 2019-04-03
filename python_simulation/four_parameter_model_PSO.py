# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import numpy as np
import matplotlib.pyplot as plt
import random

# 目标函数定义，x中每个元素对应一个参数
def ras(absolute_x, absolute_y, relative_x, relative_y, parameter):
    y = 0
    m1 = 1 + parameter[0]
    angle = parameter[1] / 180.0 * np.pi
    for i in range(5):
        t = np.square(m1 * (relative_x[i] * np.cos(angle) - relative_y[i] * np.sin(angle)) + parameter[2] - absolute_x[i] )\
          + np.square(m1 * (relative_x[i] * np.sin(angle) + relative_y[i] * np.cos(angle)) + parameter[3] - absolute_y[i] )
        y += t
    return y

def fin_pso(absolute_x, absolute_y, relative_x, relative_y):
    MumberOfparm = 4
    # 参数初始化
    w = 1
    c1 = 2
    c2 = 2
    # c1 = 1.49445
    # c2 = 1.49445

    maxgen = 200  # 进化次数
    sizepop = 5000  # 种群规模,群体较小时容易陷入局部最优解
                    #群体较大当数目到一定程度优化变化不明显

    # 粒子速度和位置的范围
    Vmax = [0, 15, 1, 1]
    Vmin = [0, -15, -1, -1]
    popmax = [ 2,  180,  5,  5]
    popmin = [-2, -180, -5, -5]

    # 产生初始粒子和速度
    pop = np.random.uniform(-1, 1, (MumberOfparm, sizepop))
    for i in range(sizepop):
        tt = random.randrange(-2, 1, 2)
        pop[0][i] = tt
    pop[1] *= 180
    pop[2] *= 5
    pop[3] *= 5
    # print "initial pop =\n", pop
    v = np.random.uniform(-1, 1, (MumberOfparm, sizepop))
    v[0] = 0
    v[1] *= 10
    # print "initial v=\n", v
    fitness = ras(absolute_x, absolute_y, relative_x, relative_y, pop)  # 计算适应度
    # print "initial fitness=\n", fitness
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
        r1 = np.random.rand(4, sizepop)
        r2 = np.random.rand(4, sizepop)
        v = w * v + c1 * r1 * (gbest - pop) + c2 * r2 * (zbest.reshape(4, 1) - pop)
        v[0] = 0

        # 位置更新
        pop = pop + v
        for ti in range(3):
            i = ti+1
            for j in range(sizepop):
                if pop[i][j] > popmax[i]:
                    pop[i][j] = popmax[i]
                if pop[i][j] < popmin[i]:
                    pop[i][j] = popmin[i]
        for ti in range(3):
            i = ti+1
            for j in range(sizepop):
                if v[i][j] > Vmax[i]:
                    v[i][j] = Vmax[i]
                if v[i][j] < Vmax[i]:
                    v[i][j] = Vmax[i]
        # print "##################################################"
        # print "pop=\n", pop
        # print "##################################################"
        # # 自适应变异
        # p = np.random.random()             # 随机生成一个0~1内的数
        # if p > 0.8:                          # 如果这个数落在变异概率区间内，则进行变异处理
        #     temp = np.random.random()
        #     temp *= 5
        #     k = np.random.randint(0,MumberOfparm)     # 在[0,2)之间随机选一个整数
        #     pop[:,k] = temp  # 在选定的位置进行变异


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
        if fitnesszbest < 10:
            break
    # 结果分析
    plt.plot(record, 'b-',label='1234')
    plt.xlabel(u'迭代次数')
    plt.ylabel(u'适应度')
    # plt.title(u'适应度曲线,群组大小为500')
    # print plt.ylim()
    plt.show()
    return zbest, record[t-1]