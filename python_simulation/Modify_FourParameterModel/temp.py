# -*- coding: utf-8 -*
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import random
from pylab import *     #支持中文显示和负号
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
np.set_printoptions(suppress=True)

for i in range(10):
    tt = random.randrange(-2, 1, 2)
    print tt