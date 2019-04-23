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
    m1 = parameter[0]
    angle = parameter[1] / 180.0 * np.pi
    x1 = parameter[2] / 180.0 * 5
    y1 = parameter[3] / 180.0 * 5
    for i in range(5):
        t = np.square((relative_x[i] * np.cos(angle) - m1 * relative_y[i] * np.sin(angle)) + x1 - absolute_x[i] )\
          + np.square((relative_x[i] * np.sin(angle) + m1 * relative_y[i] * np.cos(angle)) + y1 - absolute_y[i] )
        y += t
    return y

def fin_pso(absolute_x, absolute_y, relative_x, relative_y):
    MumberOfparm = 4
    # 参数初始化
    w = 0.7298
    c1 = 1.49445
    c2 = 1.49445

    maxgen = 50  # 进化次数
    sizepop = 100  # 种群规模,群体较小时容易陷入局部最优解
                    #群体较大当数目到一定程度优化变化不明显

    # 粒子速度和位置的范围
    Vmax = 10
    Vmin = -10
    popmax = 180
    popmin = -180

    # 产生初始粒子和速度
    pop = np.random.uniform(popmin, popmax, (MumberOfparm, sizepop))
    ttt = [-1, 1]
    for i in range(sizepop):
        tt = random.choice(ttt)
        pop[0][i] = tt
    v = np.random.uniform(Vmin, Vmax, (MumberOfparm, sizepop))
    v[0] = 0
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
        r1 = np.random.rand(4, sizepop)
        r2 = np.random.rand(4, sizepop)
        v = w * v + c1 * r1 * (gbest - pop) + c2 * r2 * (zbest.reshape(4, 1) - pop)
        v[0] = 0
        v[v > Vmax] = Vmax  # 限制速度
        v[v < Vmin] = Vmin
        # 位置更新
        pop = pop + v
        pop[pop > popmax] = popmax  # 限制位置
        pop[pop < popmin] = popmin
        # for ti in range(3):
        #     i = ti+1
        #     for j in range(sizepop):
        #         if pop[i][j] > popmax[i]:
        #             pop[i][j] = popmax[i]
        #         if pop[i][j] < popmin[i]:
        #             pop[i][j] = popmin[i]
        # for ti in range(3):
        #     i = ti+1
        #     for j in range(sizepop):
        #         if v[i][j] > Vmax[i]:
        #             v[i][j] = Vmax[i]
        #         if v[i][j] < Vmax[i]:
        #             v[i][j] = Vmax[i]


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
        # if fitnesszbest < 10:
        #     break
    # 结果分析
    # plt.plot(record, 'b-',label='1234')
    # plt.xlabel(u'迭代次数')
    # plt.ylabel(u'适应度')
    # plt.title(u'适应度曲线,群组大小为500')
    # print plt.ylim()
    plt.show()
    return zbest, record[t-1]