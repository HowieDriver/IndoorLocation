# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from plot import getDist
from plot import topk
from plot import addGaussNoise
from plot import splti
from plot import combination_k
from mds import mds_fun
from pylab import *     #支持中文显示和负号
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

start_time =time.clock()
def relativeToabsl(anchor_x, anchor_y, realtive_x, realtive_y):

    a1 = []
    a2 = []
    a1.append(realtive_x[0])
    a1.append(realtive_y[0])
    a2.append(realtive_x[1])
    a2.append(realtive_y[1])

    b1 = []
    b2 = []
    b1.append(anchor_x[0])
    b1.append(anchor_y[0])
    b2.append(anchor_x[1])
    b2.append(anchor_y[1])

    a1 = np.mat(a1)
    a2 = np.mat(a2)
    b1 = np.mat(b1)
    b2 = np.mat(b2)


    u = ((b2 - b1).T + (a2 - a1)).T
    v = u / (np.linalg.norm(u))
    E = np.mat(np.eye(2, 2, dtype=int))
    Q = 0 - E + 2 * v * v.T
    L = b1 * (E + Q) + (a1 - b1) * Q



    b3 = []
    b3.append(anchor_x[2])
    b3.append(anchor_y[2])

    a3 = []
    a3.append(realtive_x[2])
    a3.append(realtive_y[2])
    a3 = np.mat(a3)

    a_b3 = a3 * Q + L
    a_b3list = a_b3.getA1()

    c1 = (a_b3 - a1).getA1()
    c2 = (a2 - a1).getA1()
    #####################################################
    epsilon = (c1[0]*c2[0] + c1[1]*c2[1]) / (c2[0] ** 2 + c2[1] ** 2)
    mira_b3 = 2 * epsilon * (a2 - a1) + 2 * a1 - a_b3
    mira_b3list = mira_b3.getA1()

    de1ta1 = ((b3[0] - a_b3list[0]) ** 2 + (b3[1] - a_b3list[1]) ** 2)
    delta2 = ((b3[0] - mira_b3list[0]) ** 2 + (b3[1] - mira_b3list[1]) ** 2)

    at = []
    at.append(realtive_x[5])
    at.append(realtive_y[5])
    at = np.mat(at)

    bt = at * Q + L
    mirbtlist = bt.getA1()

    if delta2 < de1ta1:
        print "需要翻转"
        c1 = (bt - a1).getA1()
        c2 = (a2 - a1).getA1()
        #####################################################
        epsilon = (c1[0] * c2[0] + c1[1] * c2[1]) / (c2[0] ** 2 + c2[1] ** 2)
        mirb = 2 * epsilon * (a2 - a1) + 2 * a1 - bt
        mirbtlist = mirb.getA1()

    return mirbtlist




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
    print "RMSE=", RMSE
    RMSE = str(RMSE)
    plt.xlabel("x/m")
    plt.ylabel("y/m")
    plt.xlim(-6, 6)
    plt.ylim(-6, 6)
    plt.text(-5.8, 5.5, u"陷入局部最优解次数="+str(round(cunt,2))+"，"+u"定位时间="+str(round(end_time-start_time,2))+"，"+u"rmse=" + str(RMSE))  # 在x轴-4， y轴0.30开始加入说明
    # plt.text(-3.7, 5.5, ",rmse=" + str(RMSE))  # 在x轴-4， y轴0.30开始加入说明

    # plt.title(u"四参数模型群组规模500，迭代次数100")
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
cunt = 0
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
        # d = addGaussNoise(d, 0, 0.5)
        D2.append(d*d)
    for k in range(NumberOfAnchorNode):
        P[k][NumberOfAnchorNode] = D2[k]
    for k in range(NumberOfAnchorNode):
        P[NumberOfAnchorNode][k] = D2[k]
    Loc, x, y = mds_fun(P, NumberOfTotalNode)

    realtive_x = x
    realtive_y = y


    xy_tar = relativeToabsl(anchor_x, anchor_y, realtive_x, realtive_y)
    print "xy_tar=", xy_tar
    target_absl_x = xy_tar[0]
    target_absl_y = xy_tar[1]

    print u"本次误差=", ((target_x[i] - target_absl_x)**2 + (target_x[i] - target_absl_x)**2)**0.5
    # print "target_loc_xy=", target_absl_x, target_absl_y
    # print "target_real_xy=", target_x[i], target_y[i]
    target_absl_array_x.append(target_absl_x)
    target_absl_array_y.append(target_absl_y)
end_time =time.clock()
actualFigure(anchor_x, anchor_y, target_x, target_y, target_absl_array_x, target_absl_array_y)
print u"陷入局部最优解次数：" + str(cunt)
tim = end_time-start_time
tim = round(tim,2)
print u"程序运行时间： "+ str(tim)+"s"