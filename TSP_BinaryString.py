import random


class TSP_BinaryString:
    def __init__(self, cities):
        self.string = []
        self.fitness = 0.0
        self.distance = 0

        for i in cities:
            self.string.append(i)

        random.shuffle(self.string)
        self.get_distance()

    def get_fitness(self):
        #F_MAX = 1
        #F_MIN = 0.01
        f_ind = self.get_distance()

        #result = (F_MAX - F_MIN)/(f_min-f_max)*f_ind+((f_min*F_MIN-f_max*F_MIN)/f_min-f_max)
        #print(result)
        self.fitness = 1 / f_ind
        return 1/f_ind #result

    def get_distance(self): # Calculate distance between all points !
        if self.distance == 0:
            tour_distance = 0
            for i in range(0, len(self.string)-1):
                distance_between = self.string[i].distance_to(self.string[i+1])
                tour_distance += distance_between
            tour_distance += self.string[len(self.string)-1].distance_to(self.string[0]) # last and first
            self.distance = tour_distance

        return self.distance

    def __lt__(self, other):
        return self.get_fitness() < other.get_fitness()


