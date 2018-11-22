import copy
import random
import math
import numpy

class Ant:
    def __init__(self, cities, pos, algorithm):
        self.cities = copy.copy(cities)
        self.visited = []
        self.visited.append(self.cities[pos])
        self.actual_city = self.cities[pos]
        self.cities.remove(self.cities[pos])
        self.alg = algorithm
        self.total_probability = 0
        self.probability = []
        self.actual_pos = pos
        self.distance = 0

    def get_distance(self):
        if self.distance == 0:
            for i in range(0, len(self.visited)):
                self.distance += self.visited[i].distance_to(self.visited[(i + 1) % len(self.visited)])
        return self.distance

    def next_move(self):
        distances = []
        total_probability = 0
        for i in range(0, len(self.cities)):
            distances.append((i, self.actual_city.distance_to(self.cities[i])))

        distances = sorted(distances, reverse=True, key=lambda k: k[1])

        probs = []
        for i in range(0, len(distances)):
            dist = 1 / distances[i][1]
            total_probability += math.pow(self.alg.pheromones[self.actual_pos][distances[i][0]], self.alg.alfa) * math.pow(dist, self.alg.beta)
        #print("____TOTAL____")
        #print(total_probability)
        for i in range(0, len(distances)):
            dist = 1 / distances[i][1]
            prob = (math.pow(self.alg.pheromones[self.actual_pos][distances[i][0]], self.alg.alfa) * math.pow(dist, self.alg.beta)) / total_probability
            probs.append(prob)

        p = random.uniform(0, 1)
        actual = 0
        next_selection = len(probs)-1
        for i in range(0, len(probs)):
            actual += probs[i]
            if p < actual:
                next_selection = i
                break
        #print(str(next_selection) + " of " + str(len(probs)))
        self.actual_pos = distances[next_selection][0]
        self.visited.append(self.cities[distances[next_selection][0]])
        self.actual_city = self.cities[distances[next_selection][0]]
        self.cities.remove(self.cities[distances[next_selection][0]])
        self.distance = 0


        if len(self.cities) == 0:
            self.visited.append(self.visited[0])
            self.actual_city = self.visited[0]

        self.get_distance()

class Alg_Ant:
    def __init__(self, cities, alfa, beta, Q, ro, pop_size):
        self.cities = cities
        self.alfa = alfa
        self.beta = beta
        self.Q = Q
        self.ro = ro
        self.ants = []
        self.pheromones = numpy.full((len(self.cities), len(self.cities)), 0.02)
        self.best_distance = 0
        self.best_pop = None
        self.pop_size = pop_size

    def run(self):
        self.ants = []
        if self.pop_size == 0:
            for i in range(0, len(self.cities)):
                self.ants.append(Ant(self.cities, i, self))
        else:
            pos_cities = copy.deepcopy(self.cities)
            for i in range(0, self.pop_size):
                test = random.choice(pos_cities)
                self.ants.append(Ant(self.cities, test.id, self))
                pos_cities.remove(test)

        for i in range(0, len(self.ants)):
            ant = self.ants[i]

            while len(ant.cities) > 0:
                ant.next_move()

        self.pheromones *= (1-self.ro)

        for i in range(0, len(self.ants)):
            ant = self.ants[i]
            distance = self.ants[i].get_distance()

            if self.best_pop is None or distance < self.best_distance:
                self.best_distance = distance
                self.best_pop = copy.copy(self.ants[i])

            for j in range(0, len(ant.visited)):
                self.pheromones[ant.visited[j].id][ant.visited[(j+1)%len(ant.visited)].id] += (self.Q / distance)# * (1-self.ro)
                self.pheromones[ant.visited[(j+1)%len(ant.visited)].id][ant.visited[j].id] += (self.Q / distance) #+= (self.Q / distance)# * (1-self.ro)

                #city_from = ant.visited[j].distance_to(ant.visited[(j+1)%len(ant.visited)])













