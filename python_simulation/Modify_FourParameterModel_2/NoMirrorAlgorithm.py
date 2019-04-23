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
from plot import plotxy
from NoMirrorAlgorithm_PSO import fin_pso
from mds import mds_fun
from pylab import *     #支持中文显示和负号
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

start_time =time.clock()
def relativeToabsl(parameter, relative_x, relative_y):
    m1 = parameter[0] / 180 * 2
    angle = parameter[1] / 180.0 * np.pi
    x1 = parameter[2] / 180.0 * 5
    y1 = parameter[3] / 180.0 * 5
    ret_x = m1 * relative_x * np.cos(angle) - m1 * relative_y * np.sin(angle) + x1
    ret_y = m1 * relative_x * np.sin(angle) + m1 * relative_y * np.cos(angle) + y1
    return ret_x, ret_y

#实际分布图
def actualFigure(anchor_x, anchor_y, target_x, target_y, parm_array_x, parm_array_y):
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
    RMSE = round(RMSE, 4)
    RMSE = str(RMSE)
    print "RMSE=", RMSE
    plt.xlabel("x/m")
    plt.ylabel("y/m")
    plt.xlim(-6, 6)
    plt.ylim(-6, 6)
    plt.text(-5.8, 5.5, r'$\mu=0,\ \sigma=0.5$')  # 在x轴-4， y轴0.30开始加入说明
    plt.text(-3.7, 5.5, ",rmse=" + str(RMSE))  # 在x轴-4， y轴0.30开始加入说明
    # plt.title(u"四参数模型定位结果")
    plt.show()
    return RMSE

np.set_printoptions(suppress=True)
NumberOfTargetNode = 50
NumberOfAnchorNode = 5
NumberOfTotalNode = NumberOfAnchorNode+1
anchor_x = [-5,  0, 5,   0, 0]
anchor_y = [  0, 5,  0, -5, 0]
target_x = np.random.uniform(-5, 5, size=(NumberOfTargetNode))#随机生成50个数，范围在-5到5
target_y = np.random.uniform(-5, 5, size=(NumberOfTargetNode))
target_absl_array_x = []
target_absl_array_y = []
#根据实际坐标生成模拟的距离阵
P = [[  0,  50, 100,  50,  25, 1],
     [ 50,   0,  50, 100,  25, 1],
     [100,  50,   0,  50,  25, 1],
     [ 50, 100,  50,   0,  25, 1],
     [ 25,  25,  25,  25,  0,  1],
     [  1,   1,   1,   1,  1,  0]]

for i in range (NumberOfTargetNode):
    print i
    D2 = []
    for j in range(NumberOfAnchorNode):
        d = getDist([target_x[i], target_y[i]], [anchor_x[j], anchor_y[j]])
        d = addGaussNoise(d, 0, 0.5)
        D2.append(d*d)
    for k in range(NumberOfAnchorNode):
        P[k][NumberOfAnchorNode] = D2[k]
    for k in range(NumberOfAnchorNode):
        P[NumberOfAnchorNode][k] = D2[k]

    Loc, x, y = mds_fun(P, NumberOfTotalNode)
    target_realtive_x = x[5]
    target_realtive_y = y[5]
    parm, diff = fin_pso(anchor_x, anchor_y, x[0:5], y[0:5])

    print "最小Difference值："
    print diff
    target_absl_x, target_absl_y = relativeToabsl(parm, target_realtive_x, target_realtive_y)

    # print "target_loc_xy=", target_absl_x, target_absl_y
    # print "target_real_xy=", target_x[i], target_y[i]
    target_absl_array_x.append(target_absl_x)
    target_absl_array_y.append(target_absl_y)

    # if i==0:
    #     plotxy(anchor_x, anchor_y, target_x[0], target_y[0])
    #
    #     relanc_x = x[0:5]
    #     relanc_y = y[0:5]
    #     relanc_x = relanc_x.tolist()
    #     relanc_y = relanc_y.tolist()
    #     plotxy(relanc_x, relanc_y, target_realtive_x, target_realtive_y)

actualFigure(anchor_x, anchor_y, target_x, target_y, target_absl_array_x, target_absl_array_y)
end_time =time.clock()
print u"程序运行时间： "+ str(end_time-start_time)+"s"