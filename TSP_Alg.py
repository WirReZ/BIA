import random
import TSP_Population
import TSP_BinaryString

import copy

class TSP_Alg:

    def __init__(self, city_list,   mutation_rate):
        self.Cities = city_list
        self.mutation_rate = mutation_rate

    def evolutePopulation(self, pop):
        new_population = TSP_Population.TSP_Population(self.Cities, len(pop.population))
        #GetBest
        new_population.population[0] = pop.get_best_binary_string()

        for i in range(1, len(pop.population)): # Hledam rodice !
            parent1 = self.select_parent(pop)
            parent2 = self.select_parent(pop)
            while parent1 == parent2:
                parent2 = self.select_parent(pop)

            child = self.cross_over(parent1, parent2) # Udelam krizeni
            new_population.population[i] = child

        #Udelam mutaci
        for i in range(0, len(new_population.population)):
            self.mutation(new_population.population[i])

        return new_population

    def mutation(self, binary_string):
        for i in range(0, len(binary_string.string)):
            if random.uniform(0, 1) < self.mutation_rate:
                rand = int(random.uniform(0, len(binary_string.string)))
                c1 = binary_string.string[i]
                c2 = binary_string.string[rand]

                binary_string.string[i] = c2
                binary_string.string[rand] = c1

    def select_parent(self, pop): # Roulette !!
        total_fitness = pop.calculate_fitness()
        probs = []
        tmp_pop = copy.copy(pop.population)
        tmp_pop.sort()
        for i in range(0, len(pop.population)):
            probs.append(tmp_pop[i].get_fitness()/total_fitness)

        #probs.sort()

        r = random.uniform(0, 1)
        actual = 0
        for i in range(0, len(probs)):
            actual += probs[i]
            if r < actual:
                return tmp_pop[i]

        return tmp_pop[len(pop.population)-1]


        #tmp = TSP_Population.TSP_Population(self.Cities, 5)
        #for i in range(0, len(tmp.population)):
        #    rand = int(random.uniform(0, len(pop.population)-1))
        #    tmp.population[i] = pop.population[rand]
        #best = tmp.get_best_binary_string()

        #return best

    def cross_over(self, parent1, parent2):

        child = TSP_BinaryString.TSP_BinaryString(self.Cities)

        pos1 = int(random.uniform(0, len(parent1.string)))
        pos2 = int(random.uniform(0, len(parent1.string)))
        if pos1 < pos2:
            start_position = pos1
            end_position = pos2
        else:
            start_position = pos2
            end_position = pos1

        for i in range(0, len(child.string)):
            child.string[i] = None

        for i in range(start_position, end_position):
            child.string[i] = parent1.string[i]

        j = 0
        for i in range(0, len(child.string)):
            if child.string[i] is None:
                while parent2.string[j] in child.string:
                    j += 1
                child.string[i] = parent2.string[j]
                j += 1

        return child
