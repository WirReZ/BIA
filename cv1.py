import itertools
import matplotlib.pyplot as plt
import numpy as np
import math




class City:
    def __init__(self, name,posx,posy):
        self.name = name
        self.posx = posx
        self.posy = posy

completed = []
cities = []
gcost = 0
path = []
pathDistance = []

with open("input.txt","r") as f:
    content = f.read().splitlines()


for line in content:
    variables = line.split(",")

    cities.append(City(variables[0],variables[1],variables[2]))


distance = [[0] * len(cities) for i in range(len(cities))]

for city1 in cities:
    completed.append(0)
    for city2 in cities:
        distance[int(city1.name)-1][int(city2.name)-1]= math.sqrt( pow(int(city1.posx)-int(city2.posx),2) + pow(int(city1.posy)-int(city2.posy),2) )


def next_point(c):
    global gcost
    global path
    global pathDistance
    mincost = 999
    ncity = ""
    kmin = 999
    nc = 999
    for i in range(len(cities)):
        if distance[c][i]!=0 and completed[i]==0:
            if distance[c][i]+distance[i][c] < mincost:
                mincost = distance[i][0]+distance[c][i]
                kmin = distance[c][i]
                ncity = cities[i]
                nc = i

    if mincost!=999:
        pathDistance.append(kmin)
        path.append(ncity)
        gcost+=kmin
    return nc



def startpoint(point):
    global gcost
    completed[point]=1
    npoint=next_point(point)
    if npoint == 999:
        npoint=0
        gcost= gcost + distance[point][npoint]
    else:
        startpoint(npoint)

path.append(cities[0])
startpoint(0) # first index for starting

print(pathDistance)
print(gcost)

for a in path:
    print(a.name)

pointx = []
pointy = []
for c in path:
    pointx.append(int(c.posx))
    pointy.append(int(c.posy))



plt.plot(pointx, pointy, '--o')
for a in path:
    plt.annotate(str(a.name),xy=(int(a.posx),int(a.posy)))




plt.show()