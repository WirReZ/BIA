import TSP_BinaryString

class TSP_Population:
    def __init__(self, cities, number_of_population):
        self.population = []
        self.cities = cities
        self.number_of_population = number_of_population
        self.distance = 0
        self.fitness = 0
        for i in range(0, self.number_of_population):
            self.population.append(TSP_BinaryString.TSP_BinaryString(self.cities))
        self.calculate_distance()
        self.calculate_fitness()

    def get_best_binary_string(self):

        self.calculate_distance()
        best = self.population[0]
        for i in range(0, self.number_of_population):
            if best.get_fitness() < self.population[i].get_fitness():
                best = self.population[i]
        return best

    def calculate_distance(self):
        if self.distance == 0:
            for i in range(0, self.number_of_population):
                distance = int(self.population[i].get_distance())
                self.distance += distance
        return self.distance

    def calculate_fitness(self):
        if self.fitness == 0:
            for i in range(0, self.number_of_population):
                fitness = self.population[i].get_fitness()
                self.fitness += fitness
        return self.fitness

