import random
import threading
import numpy as np
import time


class Soma:
	def __init__(self, pop_size, max_migration, path_length, step_size, prt_threshold, spaces, cost_function):
		self.pop_size = pop_size
		self.max_migration = max_migration
		self.spaces = spaces
		dim = [None] * (len(spaces) + 1)
		self.points = []
		self.cost_function = cost_function
		self.path_length = path_length
		self.step_size = step_size
		self.prt_threshold = prt_threshold
		self.lock = threading.Lock()

		for i in range(self.pop_size):
			for j in range(len(self.spaces)):
				dim[j] = random.uniform(self.spaces[0], self.spaces[1])
			dim[len(self.spaces)] = self.cost_function(np.asarray(dim)[0:len(self.spaces)])
			self.points.append(dim.copy())

	def get_prt_vector(self):
		vector = []
		random.seed()
		for j in range(len(self.spaces)+1):
			vector.append(1 if random.uniform(0, 1) < self.prt_threshold else 0)
		return vector

	def find_leader(self):
		min_val = self.points[0][len(self.spaces)]
		inx = 0
		for i in range(1, self.pop_size):
			if self.points[i][len(self.spaces)] < min_val:
				min_val = self.points[i][len(self.spaces)]
				inx = i
		return inx

	def run(self):
		print("Starting in 3 seconds!")
		time.sleep(3)
		for z in range(self.max_migration):
			leader_id = self.find_leader()
			leader = self.points[leader_id]
			for position in range(self.pop_size):
				if position == leader_id:
					continue
				point = self.points[position].copy()
				best = point.copy()
				prt_vector = self.get_prt_vector()
				start = self.step_size
				for i in np.arange(start,self.path_length,self.step_size):
					for j in range(len(self.spaces)):
						point[j] = self.points[position][j] + (leader[j] - self.points[position][j]*i*prt_vector[j])
					point[len(self.spaces)] = self.cost_function(np.asarray(point)[0:len(self.spaces)])
					if point[0] < self.spaces[0] or point[0] > self.spaces[1] or point[1] < self.spaces[0] or point[1] > self.spaces[1]:
						continue
					if best[len(self.spaces)] > point[len(self.spaces)]:
						best = point.copy()
				if best[len(self.spaces)] < self.points[position][len(self.spaces)]:
					self.points[position] = best.copy()

			self.lock.acquire()
