# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
import numpy as np
from pylab import *     #支持中文显示和负号
reload(sys)
sys.setdefaultencoding('utf-8')
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import numpy as np
beaconData = [-48,-48,-49,-50,-50,-50,-50,-48,-48,-48,-48,-48,-48,-48,-48,-48,-47,-47,-47,-47,-50,-50,-50,-50,-50,-50,-48,-48,-48,-48,-49,-47,-47,-47,-47,-47,-49,-50,-50,-50,-50,-50,-50,-48,-48,-48,-48,-48,-48,-48,-48,-47,-47,-47,-47,-50,-50,-50,-50,-50,-47,-47,-47,-47,-47,-47,-47,-50,-50,-50,-50,-50,-50,-50,-50,-50,-48,-48,-48,-48,-48,-48,-48,-48,-48,-48,-47,-50,-47,-47,-48,-48,-47,-50,-50,-50,-47,-47,-48,-50,-49,-49,-49,-51,-51,-49,-49,-49,-49,-49,-51,-49,-51,-50,-47,-49,-47,-47,-47,-48,-48,-47,-48,-47,-50,-50,-50,-50,-50,-48,-48,-48,-48,-48,-48,-51,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-49,-50,-51,-50,-50,-49,-49,-49,-49,-48,-48,-48,-49,-49,-49,-51,-51,-50,-50,-50,-51,-51,-49,-48,-48,-48,-47,-48,-47,-50,-50,-50,-50,-50,-50,-50,-50,-51,-51,-50,-50,-50,-51,-49,-49,-49,-49,-49,-49,-49,-50,-49,-49,-49]
print len(beaconData)
del(beaconData[0:100])
del(beaconData[50:600])
x = np.arange(start=0, stop=50)
print x

plt.ylim(-55, -44)
plt.scatter(x, beaconData, c = 'blue')#离散点
plt.plot(x, beaconData,color = 'green')
plt.xlabel(u"次数/n")
plt.ylabel(u"RSSI值/dB")
plt.title(u"0.5米处信号接收强度")
beaconData.sort()
print beaconData
del(beaconData[0:3])
print beaconData
print len(beaconData)
del(beaconData[44:47])
ave = np.average(beaconData)
ave = round(ave, 2)
std = np.std(beaconData,ddof=1)
std = round(std, 2)
plt.text(0, -45, u'均值='+str(ave)+",标准差="+str(std))
plt.show()


