import matplotlib.pyplot as plt
import numpy as np
import random

a = range(0, 100, 1)
x = random.sample(a, 36)
y = random.sample(a, 36)
print "x= ", x
plt.scatter(x, y, color = 'blue')
plt.plot(x, y, color = 'green')
plt.show()

#snd = np.random.randn(2, 4)#
nd = np.random.rand(2, 4)
print snd
print nd