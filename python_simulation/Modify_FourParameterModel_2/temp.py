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

anchorNum = [4, 6, 8, 10]
HouseholderRMSE = [0.60, 0.58, 0.54, 0.53]
MdsPsoRMSE = [0.66, 0.65, 0.61, 0.59]

HouseholderTime = []
MdsPsoTime = [18.03]
plt.plot(anchorNum, HouseholderRMSE, 'r--')
plt.plot(anchorNum, HouseholderRMSE, 'rs',label='MDS-HD')

plt.plot(anchorNum, MdsPsoRMSE, 'b')
plt.plot(anchorNum, MdsPsoRMSE, 'bo',label='MDS-PSO')
plt.legend(loc=1) # 指定legend的位置,读者可以自己help它的用法

plt.xlabel(u'锚节点个数')
plt.ylabel(u"定位误差RMSE/m")
plt.xlim(4, 10)
plt.ylim(0.51, 0.68)
plt.show()