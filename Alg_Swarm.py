import threading
import random
import numpy as np
import time


class Swarm:

    def __init__(self, pop_size, iteration, spaces, cost_function, param_c1, param_c2, max_param_v,w_start,w_stop):
        self.pop_size = pop_size
        self.cost_function = cost_function
        self.spaces = spaces
        self.iteration = iteration
        self.lock = threading.Lock()
        self.points = []
        self.speed = []
        self.gBest = ""
        self.pBest = []
        self.maxV = max_param_v
        self.c1 = param_c1
        self.c2 = param_c2
        self.w_start = w_start
        self.w_stop = w_stop
        dim = [None] * (len(self.spaces) + 1)

        for i in range(self.pop_size):
            for j in range(len(self.spaces)):
                dim[j] = random.uniform(self.spaces[0], self.spaces[1])
            dim[len(self.spaces)] = self.cost_function(np.asarray(dim)[0:len(self.spaces)])
            self.points.append(dim.copy())
            self.pBest.append(dim.copy())
            self.speed.append([0, 0])

    def run(self):
        print("Starting in 3 seconds!")
        time.sleep(3)
        self.gBest = self.find_best(self.points)
        for i in range(self.iteration):
            for j in range(0, self.pop_size):
                self.speed[j] = self.calculate_velocity(i, j, self.iteration)
                next_position = self.next_position(j)

                if next_position[len(self.spaces)] < self.pBest[j][len(self.spaces)]:
                    self.pBest[j] = next_position
                if self.pBest[j][len(self.spaces)] < self.gBest[len(self.spaces)]:
                    self.gBest = self.pBest[j]
                self.points[j] = next_position
            self.lock.acquire()

    def next_position(self, position):
        tmp = [0, 0, 0]
        for i in range(len(self.spaces)):
            tmp[i] = self.points[position][i] + self.speed[position][i]
            if tmp[i] > self.spaces[1]:
                tmp[i] = self.spaces[1]
            if tmp[i] < self.spaces[0]:
                tmp[i] = self.spaces[0]
        tmp[len(self.spaces)] = self.cost_function(np.asarray(tmp)[0:len(self.spaces)])
        return tmp

    def calculate_param_w(self, iteration, maximum):
        return self.w_start - ((self.w_start-self.w_stop)*iteration/maximum)

    def calculate_velocity(self, actual_iteration, i, max_iteration):
        tmp = [0, 0, 0]
        for dimension in range(len(self.spaces)):
            tmp[dimension] = self.calculate_param_w(actual_iteration, max_iteration) * self.speed[i][dimension] + self.c1 * random.uniform(0, 1) * (
                        self.pBest[i][dimension] - self.points[i][dimension]) + self.c2 * random.uniform(0, 1) * (self.gBest[dimension] - self.points[i][dimension])
            if tmp[dimension] > self.maxV:
                tmp[dimension] = self.maxV
            if tmp[dimension] < self.maxV:
                tmp[dimension] = -self.maxV
        return tmp

    def find_best(self, points):
        best = points[0]
        for i in range(1, len(points)):
            if best[len(self.spaces)] > points[i][len(self.spaces)]:
                best = points[i]
        return best
