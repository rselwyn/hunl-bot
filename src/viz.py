import numpy as np
import random

data = [[0 for i in range(13)] for j in range(13)]

f = open("chart.txt", "r").readlines()
d = [i.replace("\n", "") for i in f]
for line in d:
    # if "rrb" not in line:
    #     continue
    one, two, suited = line[0], line[2], line[1] == line[3]
    prop = float(line.split("'")[3])
    m = {"A": 0, "K": 1, "Q":2, "J":3, "T":4,"9":5, "8": 6, "7": 7, "6":8, "5":9, "4":10,"3":11, "2": 12}
    if m[two] < m[one]:
        one, two = two, one

    if suited:
        data[12- m[one]][m[two]] = prop
    else:
        data[12- m[two]][m[one]] = prop

# data = [[random.random() for i in range(13)] for j in range(13)]

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


p = plt.pcolormesh(data, edgecolors='k', linewidth=2, 
    cmap=LinearSegmentedColormap.from_list('custom_r', [(0, "#d92830"),(0.5, "#f9b707"), (1, "#51a033")], N=256))

m = {"A": 0, "K": 1, "Q":2, "J":3, "T":4,"9":5, "8": 6, "7": 7, "6":8, "5":9, "4":10,"3":11, "2": 12}
rev = {m[k]:k for k in m.keys()}

ax = plt.gca()
ax.set_aspect('equal')

fig, toss = plt.subplots(1)

fig.colorbar(p,ax=ax)

for (i, j), z in np.ndenumerate(data):
    # print(rev[i])
    # print(rev[j])
    if 12 - i < j:
        s = rev[12 - i]+rev[j] + "s"
    else:
        s= rev[j] + rev[12 - i] 
        if 12 - i != j:
            s += "o"

    ax.text(j + 0.5, i + 0.45, s, ha='center', va='center')


plt.show()