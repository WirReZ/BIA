import random
import numpy as np
import threading
import time


class HillClimb:
	def __init__(self, pop_size, steps, max_stuck, scalar, delta, spaces, cost_function):
		self.pop_size = pop_size
		self.steps = steps
		self.spaces = spaces
		self.delta = delta
		self.cost_function = cost_function
		self.max_stuck = max_stuck
		self.scalar = scalar
		dim = [None] * (len(self.spaces) + 1)
		self.points = []
		self.lock = threading.Lock()

		for i in range(self.pop_size):
			for j in range(0, len(self.spaces)):
				dim[j] = random.uniform(self.spaces[0], self.spaces[1])
			dim[len(spaces)] = self.cost_function(np.asarray(dim)[0:len(self.spaces)])
			self.points.append(dim.copy())

	def run(self):
		print("Starting in 3 seconds!")
		time.sleep(3)
		for i in range(0, self.steps):
			for j in range(0, len(self.points)):
				self.points[j] = self.next_move(j)
				self.lock.acquire()

	def next_move(self, index):
		current = self.points[index]
		#best = self.points[index]
		stuck = 0

		while True:
			next = self.grad_ascend(current)
			if next[len(self.spaces)] < current[len(self.spaces)]:
				current = next
				#if best[len(self.spaces)] > next[len(self.spaces)]:
				#	best = next
			else:
				if stuck < self.max_stuck:
					stuck += 1
					for j in range(0, len(self.spaces)):
						current[j] = next[j] + (random.uniform(0.1, 0.5)*next[j])
						if current[j] < self.spaces[0]:
							current[j] = self.spaces[0]
						if current[j] > self.spaces[1]:
							current[j] = self.spaces[1]
					current[len(self.spaces)] = self.cost_function(np.asarray(current)[0:len(self.spaces)])
				else:
					break
		return current

	def grad_ascend(self, point):
		result = []
		for x in range(len(self.spaces)):
			delta_pos = (self.cost_function([point[x]+self.delta, 0]) - self.cost_function([point[x]-self.delta, 0])) / (2.0 * self.delta)
			new_position = point[x] + (self.scalar * delta_pos)
			if new_position > self.spaces[1]:
				new_position = self.spaces[1]
			elif new_position < self.spaces[0]:
				new_position = self.spaces[0]
			result.append(new_position)
		result.append(self.cost_function(np.asarray(result)[0:len(self.spaces)]))
		return result


