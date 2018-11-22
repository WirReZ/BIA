import random
import numpy as np
import math
import threading
import time


class Annealing:
	def __init__(self, pop_size, param_t, param_t_final, alpha, number_around, spaces,cost_functions,plt):
		self.pop_size = pop_size
		self.t = param_t
		self.t_final = param_t_final
		self.alpha = alpha
		self.spaces = spaces
		self.cost_function = cost_functions
		self.xBest = None
		self.points = []
		self.number_around = number_around
		self.plt = plt

		self.lock = threading.Lock()
		dim = [None] * (len(spaces) + 1)

		for i in range(self.pop_size):
			for j in range(0, len(self.spaces)):
				dim[j] = random.uniform(self.spaces[0], self.spaces[1])
			dim[len(self.spaces)] = self.cost_function(np.asarray(dim)[0:len(self.spaces)])
			self.points.append(dim.copy())

		self.xBest = self.points[0]

	def run(self):
		print("Starting in 3 seconds!")
		time.sleep(3)
		while self.t > self.t_final:
			for i in range(self.pop_size):
				points_around = self.generate_around(i)
				random_neighbour = points_around[random.randrange(self.number_around)]
				random_neighbour[len(self.spaces)] = self.cost_function(np.asarray(random_neighbour)[0:len(self.spaces)])
				delta = random_neighbour[len(self.spaces)] - self.points[i][len(self.spaces)]
				if delta < 0:
					self.points[i] = random_neighbour
					if self.xBest[len(self.spaces)] > self.points[i][len(self.spaces)]:
						self.xBest = self.points[i]
				else:
					r = random.uniform(0, 1)
					if r < math.exp(-(delta/self.t)):
						self.points[i] = random_neighbour
			self.lock.acquire()
			self.t *= self.alpha
		print("COMPLETED")
		self.plt.scatter(self.xBest[0], self.xBest[1], self.xBest[2], s=40, color='RED', marker='<', zorder='999') # print BEST OF ALL

	def generate_around(self, index):
		new_point = [None] * (len(self.spaces) + 1)
		result = []
		for i in range(self.number_around):
			for j in range(0, len(self.spaces)):
				new_point[j] = random.uniform(self.points[index][j]-5, self.points[index][j]+5)
				while new_point[j] > self.spaces[1] or new_point[j] < self.spaces[0]:
					new_point[j] = random.uniform(self.points[index][j]-0.5, self.points[index][j]+0.5)
			new_point[len(self.spaces)] = self.cost_function(np.asarray(new_point)[0:len(self.spaces)])
			result.append(new_point)
		return result
