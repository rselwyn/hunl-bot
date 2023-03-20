data = [[0 for i in range(13)] for j in range(13)]

f = open("chart.txt", "r").readlines()
d = [i.replace("\n", "") for i in f]
for line in d:
    one, two, suited = line[0], line[2], line[1] == line[3]
    prop = float(line.split("'")[3])
    m = {"A": 0, "K": 1, "Q":2, "J":3, "T":4,"9":5, "8": 6, "7": 7, "6":8, "5":9, "4":10,"3":11, "2": 12}
    if m[two] < m[one]:
        one, two = two, one

    if suited:
        data[12- m[one]][m[two]] = prop
    else:
        data[12- m[two]][m[one]] = prop


import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


plt.pcolormesh(data, edgecolors='k', linewidth=2, cmap=ListedColormap([ "#d92830","#f9b707", "#51a033"]))

ax = plt.gca()
ax.set_aspect('equal')


plt.show()