import matplotlib.pyplot as plt
import numpy as np
from pylab import *

r1 = [0.25,0.01]
r2 = [0.05,0.1]


data = np.array( [r1, r2])


data = np.ma.masked_greater(data, 0.05)


fig, ax = plt.subplots()

cmap2 = plt.cm.Blues_r
cmap2.set_bad(color="white")

heatmap = ax.pcolormesh(data, cmap=cmap2)

fig.colorbar(heatmap)
savefig('map.png')

# put the major ticks at the middle of each cell
#ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
#ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

# want a more natural, table-like display
ax.invert_yaxis()
#ax.xaxis.tick_top()

