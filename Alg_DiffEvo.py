import random
import time
import numpy as np
import threading


class DiffEvo:

    def __init__(self, pop_size, param_f, param_cr, param_generation, spaces, cost_function):
        self.pop_size = pop_size  #(len(spaces)+1) * 10
        self.param_f = param_f
        self.param_cr = param_cr
        self.generation_size = param_generation
        self.cost_function = cost_function
        dim = [None] * (len(spaces) + 1)
        self.points = []
        self.spaces = spaces
        self.lock = threading.Lock()

        for i in range(self.pop_size):
            for j in range(len(self.spaces)):
                dim[j] = random.uniform(self.spaces[0], self.spaces[1])
            dim[len(self.spaces)] = self.cost_function(np.asarray(dim)[0:len(self.spaces)])
            self.points.append(dim.copy())

    def get_random_from_pop(self, neighbour, exc, num):
        rng = neighbour.copy()
        del rng[exc]
        res = []
        for i in range(0, num):
            rand = random.randrange(len(rng))
            res.append(neighbour[rand])
        return res

    def run(self):
        print("Starting in 3 seconds!")
        time.sleep(3)
        for i in range(0, self.generation_size):
            for j in range(0, self.pop_size):
                random_neighbour = self.get_random_from_pop(self.points, j, 3)
                print(random_neighbour)
                trial = self.points[j].copy()
                for x in range(0, len(self.spaces)):
                    rand_num = random.uniform(0, 1)
                    j_rand = random.randrange(0, len(self.points))
                    if rand_num < self.param_cr or j_rand == x:
                        trial[x] = random_neighbour[2][x] + self.param_f*(random_neighbour[0][x]-random_neighbour[1][x])
                    # Meze :/
                    if trial[x] > self.spaces[1]:
                        trial[x] = self.spaces[1]
                    if trial[x] < self.spaces[0]:
                        trial[x] = self.spaces[0]

                trial[len(self.spaces)] = self.cost_function([trial[0], trial[1]])
                if trial[len(self.spaces)] < self.points[j][len(self.spaces)]:
                    self.points[j] = trial

            self.lock.acquire()
