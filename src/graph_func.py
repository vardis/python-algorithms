__author__ = 'giorgos'
import math
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt


x_range = xrange(-100, 100)

y = []
for x in x_range:
    # y.append(x*x*x + 3*x*x + 2*x + 5)
    y.append(math.fabs(x) + math.fabs(x - 16))

plt.plot(x_range, y)
plt.xlabel('y')
plt.ylabel('x')
plt.show()

