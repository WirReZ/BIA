import random
import time
import numpy as np
import threading
import copy
import math

class Alg_EvolutionStrategy:
    def __init__(self, pop_size, cd, param_generation, spaces, cost_function):
        self.pop_size = pop_size
        self.tau = 1 / math.sqrt(len(spaces))
        self.sigma = math.sqrt((math.pi*spaces[1])/(2*pop_size))
        self.sigmas = np.full(self.pop_size, self.sigma)
        self.generation_size = param_generation
        self.points = []
        self.cost_function = cost_function
        self.cd = cd
        self.lock = threading.Lock()
        self.spaces = spaces

        dim = [None] * (len(spaces) + 1)
        for i in range(self.pop_size):
            for j in range(len(self.spaces)):
                dim[j] = random.uniform(self.spaces[0], self.spaces[1])
            dim[len(self.spaces)] = self.cost_function(np.asarray(dim)[0:len(self.spaces)])
            self.points.append(dim.copy())

    def run(self):
        print("Starting in 3 seconds!")
        time.sleep(3)
        for i in range(0, self.generation_size):
            trial_points = copy.deepcopy(self.points)
            num_of_previous_better = 0
            for j in range(0, self.pop_size):
                trial = trial_points[j]
                self.sigmas[j] = self.sigmas[j] * math.exp(self.tau*np.random.normal(0, 1))
                for x in range(0, len(self.spaces)):
                    trial[x] += self.sigmas[j] * np.random.normal(0, 1) #np.random.normal(0, self.sigma)
                    # Meze :/
                    if trial[x] > self.spaces[1]:
                        trial[x] = self.spaces[1]
                    if trial[x] < self.spaces[0]:
                        trial[x] = self.spaces[0]

                trial[len(self.spaces)] = self.cost_function([trial[0], trial[1]])
                if trial[len(self.spaces)] < self.points[j][len(self.spaces)]:
                    self.points[j] = trial
                else:
                    num_of_previous_better += 1

            rate = num_of_previous_better / self.pop_size
            for j in range(0, self.pop_size):
                if rate < 1 / 5:
                    self.sigmas[j] = self.sigmas[j] * self.cd
                elif rate > 1 / 5:
                    self.sigmas[j] = self.sigmas[j] / self.cd

            self.lock.acquire()



