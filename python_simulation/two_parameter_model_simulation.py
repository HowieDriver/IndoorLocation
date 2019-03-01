#coding:utf-8
import random
import time
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from compiler.ast import flatten
from plot import getDist
from plot import topk
from plot import addGaussNoise
from two_parameter_model_PSO import fin_pso
from mds import mds_fun
from pylab import *     #支持中文显示和负号
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
start_time =time.clock()
def getLocAfterPSO(P, d2, NumberOfTotalNode):
    Loc, x, y = mds_fun(P, NumberOfTotalNode)
    target_realtive_x = x[NumberOfTotalNode-1]
    target_realtive_y = y[NumberOfTotalNode-1]
    parm, diff = fin_pso(anchor_x, anchor_y, d2, target_realtive_x, target_realtive_y, NumberOfTotalNode-1)
    return parm, diff
#实际分布图
def actualFigure(anchor_x, anchor_y, target_x, target_y, parm_array_x, parm_array_y,string):
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
    #print "RMSE=",
    RMSE = round(RMSE,4)
    RMSE = str(RMSE)
    plt.xlabel("x/m")
    plt.ylabel("y/m")
    plt.xlim(-6, 6)
    plt.ylim(-6, 6)
    plt.text(-5.8, 5.5, r'$\mu=0,\ \sigma=0.5$')  # 在x轴-4， y轴0.30开始加入说明
    plt.text(-3.7, 5.5, ",rmse="+RMSE)  # 在x轴-4， y轴0.30开始加入说明
    plt.title(string)
    plt.show()
    return RMSE


NumberOfTargetNode = 10
NumberOfAnchorNode = 5
barier_d = 10
barier_d2 = barier_d*barier_d #给某两点之间加上障碍物的值
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
        d = addGaussNoise(d, 0, 0.5) #添加均值为0， 标准差为1的高斯噪声
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

    t_p = np.array(P)
    t_p = np.delete(t_p, i_barier, axis=0)  # 删除行
    t_p = np.delete(t_p, i_barier, axis=1)  # 删除列
    t_d = np.delete(d2,i_barier,axis=0)
    parm, diff = getLocAfterPSO(P, d2, NumberOfTotalNode)
    #parm_barier, diff_barier = getLocAfterPSO(P_barier, d2_barier, NumberOfTotalNode)
    print "无障碍物最小Difference值："
    print diff
    # print "有障碍物最小Difference值："
    # print diff_barier
    # print "实际坐标：", target_x[i], target_y[i]
    # print "无障碍物定位坐标", parm[0], parm[1]
    # print "有障碍物定位坐标=", parm_barier[0], parm_barier[1]


    parm_array_x.append(parm[0])
    parm_array_y.append(parm[1])
    # parm_array_barier_x.append(parm_barier[0])
    # parm_array_barier_y.append(parm_barier[1])


# RMSE = actualFigure(anchor_x, anchor_y, target_x, target_y, parm_array_x, parm_array_y, u"障碍物处理后")
#RMSE_barrier = actualFigure(anchor_x, anchor_y, target_x, target_y, parm_array_barier_x, parm_array_barier_y, u"有障碍物存在时")
# print "RMSE=", RMSE
# print "RMSE_barrier=", RMSE_barrier
end_time =time.clock()
print u"程序运行时间： "+ str(end_time-start_time)+"s"