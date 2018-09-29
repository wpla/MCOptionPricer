from matplotlib import rcParams
# rcParams['font.family'] = 'serif'
# rcParams['font.serif'] = ['CMU Serif', 'Times New Roman']
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

x = np.arange(0, 2 * np.pi, 0.001)
y = [np.sin(i) for i in x]

fig, ax = plt.subplots()
ax.plot(x, y)

ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()

fig.savefig("test.png")
# plt.show()

plt.clf()

mu, sigma = 100, 15
x = np.random.randn(10000)

# the histogram of the data
n, bins, patches = plt.hist(x, 100, density=True, facecolor='gray')

n_x = np.arange(-5, 5, 0.01)
n_y = [norm.pdf(i) for i in n_x]

plt.plot(n_x, n_y, color="black", linewidth=0.5)

plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram')
plt.axis([-3, 3, 0, 0.5])
plt.grid(True)
plt.savefig("test2.png")
plt.show()
