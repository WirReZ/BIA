import copy
import random
import math
import numpy

class Ant:
    def __init__(self, cities, position, algorithm):
        self.allowed_cities = copy.copy(cities)
        self.visited_cities = []
        self.visited_cities.append(self.allowed_cities[position])
        self.actual_city = self.allowed_cities[position]
        self.allowed_cities.remove(self.allowed_cities[position])
        self.alg = algorithm
        self.total_probability = 0
        self.probability = []
        self.actual_position = position
        self.total_distance = 0

    def next_move(self):
        # calculate all distance from actual city
        distances = []
        attractive = []
        sum_total_attractive = 0


        for i in range(0, len(self.allowed_cities)):
            distances.append((i, 1/self.actual_city.distance_to(self.allowed_cities[i])))

        distances = sorted(distances, key=lambda k: k[1])

        for i in range(0, len(distances)):
            pheromon = self.alg.pheromones[self.actual_position][i]
            atr = pow(pheromon, self.alg.param_alfa)*pow(distances[i][1], self.alg.param_beta)
            attractive.append((distances[i][0], atr))
            sum_total_attractive += atr

        rand_roulette = random.uniform(0, 1)
        actual = 0
        next_selection = -1

        for i in range(0, len(attractive)):
            prob = attractive[i][1] / sum_total_attractive
            if rand_roulette < actual+prob:
                next_selection = i
                break
            actual += prob

        #Move to next Point !!!
        self.actual_position = attractive[next_selection][0]
        self.visited_cities.append(self.allowed_cities[self.actual_position])
        self.actual_city = self.allowed_cities[self.actual_position]
        self.allowed_cities.remove(self.allowed_cities[self.actual_position])

        #Check if there is no more cities !
        if len(self.allowed_cities) == 0:
            self.visited_cities.append(self.visited_cities[0])
            self.actual_position = len(self.visited_cities)-1
            self.actual_city = self.visited_cities[self.actual_position]

    def get_distance(self):
        self.total_distance = 0
        for i in range(0, len(self.visited_cities)-1):
            self.total_distance += self.visited_cities[i].distance_to(self.visited_cities[(i+1)])
        return self.total_distance


class Alg_Ant:
    def __init__(self, cities, alfa, beta, Q, ro, pop_size):
        self.all_cities = cities
        self.param_alfa = alfa
        self.param_beta = beta
        self.param_q = Q
        self.param_ro = ro
        self.ants = []
        self.pheromones = numpy.full((len(self.all_cities), len(self.all_cities)), 0.02)
        self.best_distance = 0
        self.best_pop = None
        self.pop_size = pop_size


    def run(self):
        self.ants = []

        if self.pop_size == 0:# if empty pop_size then pop_size = len(all_cities)
            for i in range(0, len(self.all_cities)):
                self.ants.append(Ant(self.all_cities, i, self))
        else:
            cities_id = []
            for i in range(0, self.pop_size):
                rand = random.randint(0, len(self.all_cities)-1)
                while rand in cities_id:
                    rand = random.randint(0, len(self.all_cities)-1)
                cities_id.append(rand)
                self.ants.append(Ant(self.all_cities, rand, self))

        for i in range(0, len(self.ants)):
            ant = self.ants[i]

            while len(ant.allowed_cities) > 0:
                ant.next_move()

        self.pheromones *= self.param_ro
        for i in range(0, len(self.ants)):
            ant = self.ants[i]
            distance = ant.get_distance()

            if self.best_pop is None or distance < self.best_distance:
                self.best_pop = copy.copy(self.ants[i])
                self.best_distance = distance

            for j in range(0, len(ant.visited_cities)-1):
                self.pheromones[ant.visited_cities[j].id][ant.visited_cities[j+1].id] += self.param_q / distance
                self.pheromones[ant.visited_cities[j+1].id][ant.visited_cities[j].id] += self.param_q / distance



