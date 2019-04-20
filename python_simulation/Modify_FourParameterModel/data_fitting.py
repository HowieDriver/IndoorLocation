# -*- coding: utf-8 -*
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from pylab import *     #支持中文显示和负号
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
np.set_printoptions(suppress=True)
d = [ 0.5,     1,      2,     3,     4,      5,       6,      7,       8]
p = [-48.89, -51.14, -52.32, -56.2, -58.36, -60.11, -62.16, -60.33, -63.07]
d = np.array(d)
p = np.array(p)
# #########################log fitting ########################
def fun(d, n, c):
    return -51.14 - 10*n*(np.log10(d)) + c
popt, pcov = curve_fit(fun, d, p)
n=popt[0] # popt里面是拟合系数，读者可以自己help其用法
c=popt[1]
c = round(c, 2)
n = round(n, 2)
print "n=",n,"\tc=",c
yvals=fun(d,n,c)
print "d=",d

sum = 0
for i in range(9):
    sum += (p[i]-yvals[i])**2
print "sum=", sum
sum /= 9
ave = sum ** 0.5
print "ave=", sum
# d2 = [3, 5, 7]
# yvals2=fun(d2,n,c)
# print yvals2
plot1=plt.plot(d, p, '*',label=u'原始数据')
plot2=plt.plot(d, yvals, 'r',label=u'拟合曲线')
plt.xlabel('d/m')
plt.ylabel('P/dB')
plt.legend(loc=1) # 指定legend的位置,读者可以自己help它的用法
# plt.title(u'衰减模型拟合: P = -51.14-10*%5.3f* lg(d)%5.3f' % tuple(popt))
# plt.title(u'衰减模型拟合')
plt.show()
#
# # plt.savefig('p2.png') #保存图片

##############ploynomial fitting#############
# z1 = np.polyfit(p, d, 3) # 用3次多项式拟合
# p1 = np.poly1d(z1)
# print(p1) # 在屏幕上打印拟合多项式
# yvals=p1(p) # 也可以使用yvals=np.polyval(z1,x)
# plot1=plt.plot(p, d, '*',label=u'原始数据')
# plot2=plt.plot(p, yvals, 'r',label=u'拟合曲线')
# plt.xlabel(u'RSSI/dB')
# plt.ylabel(u'距离/m')
# plt.legend(loc=1) # 指定legend的位置,读者可以自己help它的用法
# # plt.title(u'多项式拟合:P =  %5.3fx**3%5.3fx**2%5.3fx%5.3f' % tuple(z1))
# plt.title(u'多项式拟合')
#
# plt.show()


##############################################
d = [1, 2, 3, 4, 5, 6, 8]
RssiMin = [-50,-52,-55,-57,-58,-60,-61]
RssiMax = [-55, -54, -59, -60, -62, -66, -66]
NoRssiMin = [-62, -63, -67, -69, -69, -68, -73]
NoRssiMax = [-69, -72, -78, -78, -81]
SplitLine  = [-60,-60,-60,-60,-60, -60, -60]
# plot1=plt.plot(d, RssiMin, 'r',label=u'RssiMin')
plot2=plt.plot(d, RssiMax, 'r--',label=u'无障碍物时RSSI最小值')
# plot1=plt.plot(d, RssiMin, 'r*')
plot2=plt.plot(d, RssiMax, 'r*')

plot3=plt.plot(d, NoRssiMin, 'b',label=u'有障碍物时RSSI最大值')
# plot3=plt.plot(d, NoRssiMax, 'b',label=u'NoRssiMax')
plot3=plt.plot(d, NoRssiMin, 'b*')
# plot3=plt.plot(d, NoRssiMax, 'b*')

# plot3=plt.plot(d, SplitLine, 'k')

SplitLine  = [-62, -62, -62, -62, -62,  -62,  -62]
# plot3=plt.plot(d, SplitLine, 'k')
plt.xlabel('d/m')
plt.ylabel('RSSI/dB')
plt.legend(loc=1) # 指定legend的位置,读者可以自己help它的用法
# plt.title(u'衰减模型拟合: P = -51.14-10*%5.3f* lg(d)%5.3f' % tuple(popt))
# plt.title(u'衰减模型拟合')
plt.show()
