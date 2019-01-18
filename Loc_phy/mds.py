#coding:utf-8
import random

import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import numpy as np
from compiler.ast import flatten
from plot import topk

import plot
D = [[0, 244, 268, 215], [244, 0, 88, 146], [268, 88, 0, 91], [215, 146, 91, 0]]
#D = [[0, 100, 200, 100], [100, 0, 100, 200], [200, 100, 0, 100], [100, 200, 100, 0]]
D = np.mat(D)
D2 = np.multiply(D, D)
# D2 = [[  0,  50, 100,  50,  25],
#      [ 50,   0,  50, 100,  25],
#      [100,  50,   0,  50,  25],
#      [ 50, 100,  50,   0,  25],
#      [ 25,  25,  25,  25,  0]]
# D2 = np.mat(D2)
print "D2 = ", D2
E = np.mat(np.eye(4, 4, dtype=int))
l = np.mat(np.ones((4, 1)))
I = l*(l.T)
H =  E - 0.25*I
print "H=", H
B = -0.5 * H*D2*H
print "B=", B

eigvals,eigvectors = np.linalg.eig(B)
print("eigvals=")
print eigvals
print("eigvectors=")
print eigvectors
vals, vecs = topk(B, 2)
print("vals=")
print vals
print("vecs=")
print vecs

eigvalsMat = np.mat(np.diag(np.sqrt(vals)))
Loc = vecs * eigvalsMat
print Loc

x = Loc[:,0]
y = Loc[:,1]
#x = np.array(x)
#y = np.array(y)
x = x.tolist()
y = y.tolist()
x = flatten(x)
y = flatten(y)

plt.scatter(x, y, color = 'blue')
plt.plot(x, y, color = 'green')

xt = []
xt.append(x[0])
xt.append(x[3])
yt = []
yt.append(y[0])
yt.append(y[3])
plt.plot(xt, yt, color = 'green')

xt = []
xt.append(x[0])
xt.append(x[2])
yt = []
yt.append(y[0])
yt.append(y[2])
plt.plot(xt, yt, color = 'green')
xt = []
xt.append(x[1])
xt.append(x[3])
yt = []
yt.append(y[1])
yt.append(y[3])
plt.plot(xt, yt, color = 'green')
plt.show()

#if __name__ == "__main__":
#    plot.gaussNoise()