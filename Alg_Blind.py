import threading
import random
import numpy as np
import time

class Blind:
	def __init__(self, pop_size, spaces, cost_function, plot):
		self.pop_size = pop_size
		self.spaces = spaces
		self.points = []
		self.plt = plot
		self.cost_function = cost_function
		self.lock = threading.Lock()
		self.xBest = None

	def run(self):
		print("Starting in 3 seconds!")
		time.sleep(3)
		dim = [None] * (len(self.spaces) + 1)
		for p in range(self.pop_size):
			for j in range(0, len(self.spaces)):
				dim[j] = random.uniform(self.spaces[0], self.spaces[1])
			dim[len(self.spaces)] = self.cost_function(np.asarray(dim)[0:len(self.spaces)])
			self.points.append(dim.copy())
			if self.xBest is None or self.xBest[len(self.spaces)] > self.points[p][len(self.spaces)]:
				self.xBest = self.points[p]

			self.lock.acquire()

		print("COMPLETED")
		self.plt.scatter(self.xBest[0], self.xBest[1], self.xBest[2], s=40, color='RED', marker='<', zorder='999')  # print BEST OF ALL

