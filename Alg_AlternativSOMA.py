import threading
import random
import numpy as np
import time


class AlternativSoma:
	def __init__(self, pop_size, max_migration, path_length, step_size, prt_threshold, spaces, cost_function, num_subplots, max_changes):
		self.pop_size = pop_size
		self.max_migration = max_migration
		self.spaces = spaces
		self.points = []
		self.point_all_plots = []
		self.cost_function = cost_function
		self.path_length = path_length
		self.step_size = step_size
		self.prt_threshold = prt_threshold
		self.lock = threading.Lock()
		self.num_subplots = num_subplots
		self.leader_subplot = None
		self.point_all_plots = [None] * num_subplots
		self.max_changes = max_changes

		for n in range(self.num_subplots):
			dim = [None] * (len(spaces) + 1)
			points = []
			for i in range(self.pop_size):
				for j in range(len(self.spaces)):
					dim[j] = random.uniform(self.spaces[0], self.spaces[1])
				dim[len(self.spaces)] = self.cost_function(np.asarray(dim)[0:len(self.spaces)])
				points.append(dim.copy())
			self.point_all_plots[n] = points.copy()

		best_id = self.get_leader_subplot()
		self.points = self.point_all_plots[best_id]

	def run(self):
		print("Starting in 3 seconds!")
		time.sleep(3)
		for i in range(self.max_changes):
			for subplot_id in range(1):#range(len(self.point_all_plots)):
				print(self.point_all_plots[subplot_id])
				self.run_soma_subplot(subplot_id)
				print(self.point_all_plots[subplot_id])

			#find best plot again
			best_id = self.get_leader_subplot()
			self.points = self.point_all_plots[best_id]
			worst_point = self.find_worst_point(self.point_all_plots[best_id])
			subplot_id, point_id = self.find_best_point_subplots(best_id)
			if self.points[worst_point][len(self.spaces)] > self.point_all_plots[subplot_id][point_id][len(self.spaces)]:
				self.points[worst_point] = self.point_all_plots[subplot_id][point_id]
			self.lock.acquire()

	def run_soma_subplot(self, subplot_id):
		my_points = self.point_all_plots[subplot_id]
		for z in range(self.max_migration):
			leader_id = self.find_leader(subplot_id)
			leader = my_points[leader_id]
			for position in range(self.pop_size):
				if position == leader_id:
					continue
				points = my_points.copy()
				point = my_points[position].copy()
				best = points[0].copy()
				prt_vector = self.get_prt_vector()
				start = self.step_size
				for i in np.arange(start, self.path_length, self.step_size):
					for j in range(len(self.spaces)):
						point[j] = self.points[position][j] + (leader[j] - self.points[position][j] * i * prt_vector[j])
					point[len(self.spaces)] = self.cost_function(np.asarray(point)[0:len(self.spaces)])
					if point[0] < self.spaces[0] or point[0] > self.spaces[1] or point[1] < self.spaces[0] or point[1] > self.spaces[1]:
						continue
					if best[len(self.spaces)] > point[len(self.spaces)]:
						best = point.copy()
				if best[len(self.spaces)] < self.points[position][len(self.spaces)]:
					my_points[position] = best.copy()

	def get_prt_vector(self):
		vector = []
		random.seed()
		for j in range(len(self.spaces) + 1):
			vector.append(1 if random.uniform(0, 1) < self.prt_threshold else 0)
		return vector

	def find_leader(self, subplot_id):
		my_points = self.point_all_plots[subplot_id]
		min_val = my_points[0][len(self.spaces)]
		inx = 0
		for i in range(1, self.pop_size):
			if my_points[i][len(self.spaces)] < min_val:
				min_val = my_points[i][len(self.spaces)]
				inx = i
		return inx

	#Subplot Actions
	def find_worst_point(self, actual_points):
		max_point = None
		idx = -1
		for i in range(0, self.pop_size):
			if idx == -1 or actual_points[i][len(self.spaces)] < max_point[len(self.spaces)]:
				max_point = actual_points[i]
				idx = i
		return idx

	def find_best_point_subplots(self, exception=-1):
		min_point = None
		min_idx = -1
		min_id_point = -1
		for i in range(0, self.num_subplots):
			if exception == i:
				continue
			for j in range(0, self.pop_size):
				if min_idx == -1 or self.point_all_plots[i][j][len(self.spaces)] < min_point[len(self.spaces)]:
					min_point = self.point_all_plots[i][j]
					min_idx = i
					min_id_point = j

		return min_idx, min_id_point

	def get_leader_subplot(self):
		min_point = None
		min_idx = -1
		for i in range(0, self.num_subplots):
			for j in range(0, self.pop_size):
				if min_idx == -1 or self.point_all_plots[i][j][len(self.spaces)] < min_point[len(self.spaces)]:
					min_point = self.point_all_plots[i][j]
					min_idx = i
		return min_idx

