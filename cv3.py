import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import numpy as np
from matplotlib.animation import FuncAnimation
import threading
#Function

import Alg_Functions
#Algorithm
import Alg_Blind
import Alg_Annealing
import Alg_Soma
import Alg_Swarm
import Alg_DiffEvo
import Alg_HillClimb
import Alg_AlternativSOMA


#############TSP
import TSP_Population
import TSP_Alg
import TSP_City

import Alg_Ant

###### MAIN PROGRAM
task = 'tsp'


def animation(frame, points, alg):
    if alg.lock.locked():
        for p in points:
            p.remove()
        points.clear()
        points.append(plot.scatter(np.asarray(alg.points)[:, 0], np.asarray(alg.points)[:, 1], np.asarray(alg.points)[:, 2], c='y', zorder=998))
        alg.lock.release()


if task == 'alg':

    fig = plt.figure()
    plot = fig.gca(projection="3d")

    spaces = (-40, 40)
    plot_points = []
    func = Alg_Functions.SchwefelFunction

    #algorithm = Alg_Blind.Blind(15, spaces, func, plot)
    #algorithm = Alg_HillClimb.HillClimb(4, 10, 3, -0.1, 0.5, spaces, func)
    #algorithm = Alg_Annealing.Annealing(5, 2.0, 0.05, 0.98, 10, spaces, func, plot)
    #algorithm = Alg_Soma.Soma(4, 10, 1.1, 0.11, 0.6, spaces, func)
    #algorithm = Alg_Swarm.Swarm(15, 80, spaces, func, 2, 2, 1, 0.8, 0.6)
    #algorithm = Alg_DiffEvo.DiffEvo(10, 0.7, 0.5, 25, spaces, func)
    algorithm = Alg_AlternativSOMA.AlternativSoma(4, 10, 1.1, 0.11, 0.5, spaces, func, 4, 10)

    X = np.arange(spaces[0], spaces[1], 0.1)
    Y = np.arange(spaces[0], spaces[1], 0.1)
    X, Y = np.meshgrid(X, Y)
    Z = func([X, Y])
    surf = plot.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False, alpha=0.5)
    if algorithm.points:
        plot_points.append(plot.scatter(np.asarray(algorithm.points)[:, 0], np.asarray(algorithm.points)[:, 1], np.asarray(algorithm.points)[:, 2], s=20, color='BLACK', marker='v', zorder='999'))

    threading.Thread(target=algorithm.run).start()
    animation = FuncAnimation(fig, animation, interval=200, fargs=(plot_points, algorithm,))

    plt.show()

elif task == 'tsp':

    cities = []
    section = "ANT"

    file = open('tsp.txt')
    i = 0
    for line in file.readlines():
        line_array = [int(s) for s in line.split()]
        cities.append(TSP_City.TSP_City(line_array[0]-1, line_array[1], line_array[2]))
        i += 1
        if i == 11:
            break

    if section == "GA":
        population = TSP_Population.TSP_Population(cities, 100)
        algorithm = TSP_Alg.TSP_Alg(cities, 0.205)
        for i in range(0, 10):
            population = algorithm.evolutePopulation(population)
            print(population.get_best_binary_string().get_distance())

        best = population.get_best_binary_string()
        pointx = []
        pointy = []
        for p in best.string:
            pointx.append(p.x)
            pointy.append(p.y)

        pointx.append(best.string[0].x)
        pointy.append(best.string[0].y)
        print(best.get_distance())
        plt.plot(pointx, pointy, '--o')
        plt.show()
    else:
        algorithm = Alg_Ant.Alg_Ant(cities, 0.2, 0.6, 100, 0.6, 0)

        for i in range(250): # 100 generaci
            algorithm.run()
            print(algorithm.best_distance)

        pointx = []
        pointy = []
        for i in range(0, len(algorithm.best_pop.visited)):
           # print(algorithm.best_pop.visited[i])
            pointx.append(algorithm.best_pop.visited[i].x)
            pointy.append(algorithm.best_pop.visited[i].y)

        #pointx.append(algorithm.best_pop.visited[0].x)
        #pointy.append(algorithm.best_pop.visited[0].y)

        plt.plot(pointx, pointy, '--o')
        plt.show()

        #    print(i)
            #algorithm = algorithm.run()














############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################



