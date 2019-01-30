'''
Author: Harshil Shah
Implement the 0/1 Knapsack genetic algorithm using Genetic Algorithm and with the following parameters:

Binary encoding.
Fitness function: Summing the weights and values if the gene is turned on for the current item.
If the weight totals more than the knapsack capacity then the value is set at zero,
otherwise it is the value of the sum of the values of the items in the knapsack.

Selection: Roulette wheel + Elitism.
Crossover: two-point or single-point crossover.
Mutation: Randomly flip every bit.

Population size : input.
Mutation rate: 0.05
Crossover rate: 0.95
Terminal condition: an input number of generations
'''

import random


class Knapsack:
    def __init__(self, item_size, max_val, max_weight, capacity, population_size,
                 mutate_prob, crossover_prob, max_genrations):
        self.values = [random.randint(0, max_val) for i in range(0, item_size)]
        self.weights = [random.randint(0, max_weight) for j in range(0, item_size)]
        self.item_size = item_size
        self.capacity = capacity
        self.p_size = population_size
        self.mutate_prob = mutate_prob
        self.crossover_prob = crossover_prob
        self.generation = max_genrations

    def genetic_knapsack(self):
        generation = 0
        population = self.initialize_population()
        fitness = self.get_fitness(population)
        while generation < self.generation:
            generation += 1
            population = self.new_population(population, fitness)
            fitness = self.get_fitness(population)
        return self.elitism(population, fitness)

    def initialize_population(self):
        # Initializing population
        # return [[random.randint(0, 0) for i in range(self.item_size)] for j in range(self.p_size)]
        population = []
        for j in range(self.p_size):
            cap = 0
            temp = []
            for x in range(self.item_size):
                choice = random.randint(0, 1)
                cap += choice * self.weights[x]
                if choice == 1 and cap <= self.capacity:
                    temp.append(1)
                else:
                    temp.append(0)
            population.append(temp)
        return population

    def get_fitness(self, population):
        fitness = []
        for i in range(self.p_size):
            value = 0
            weight = 0
            selected_items = []
            for j in range(self.item_size):
                if population[i][j] == 1:
                    weight += self.weights[j]
                    value += self.values[j]
                    selected_items += [j]
            if weight > self.capacity:
                value = 0
            fitness += [value]
        return fitness

    def new_population(self, population, fitness):
        new_pop = []
        new_pop += [self.elitism(population, fitness)]
        while len(new_pop) < self.p_size:
            mate1, mate2 = self.select_individuals(population, fitness)
            random_num = random.random()
            if random_num <= self.crossover_prob:
                new_pop += [self.mutate(self.crossover(mate1, mate2))]
        return new_pop

    @staticmethod
    def elitism(population, fitness):
        # Elitism
        elite = 0
        for i in range(len(fitness)):
            if fitness[i] > fitness[elite]:
                elite = i
        return population[elite]

    def select_individuals(self, population, fitness):
        # select individuals for reproduction
        # Roulette wheel
        total_fit = sum(fitness)
        random_num = random.randint(0, total_fit)
        temp_sum = 0
        mate1 = []
        fitness1 = 0
        for i in range(self.p_size):
            temp_sum += fitness[i]
            if temp_sum >= random_num:
                mate1 = population.pop(i)
                fitness1 = fitness.pop(i)
                break
        temp_sum = 0
        random_num = random.randint(0, sum(fitness))
        for i in range(len(population)):
            temp_sum += fitness[i]
            if temp_sum >= random_num:
                mate2 = population[i]
                population += [mate1]
                fitness += [fitness1]
                return mate1, mate2

    @staticmethod
    def crossover(mate1, mate2):
        # crossover
        random_num = random.randint(0, len(mate1) - 1)
        return mate1[:random_num] + mate2[random_num:]

    def mutate(self, chromosome):
        # mutation
        for gene in range(len(chromosome)):
            random_num = random.random()
            if random_num < self.mutate_prob:
                if chromosome[gene] == 0:
                    chromosome[gene] = 1
                else:
                    chromosome[gene] = 0
        return chromosome

    def dynamic_knapsack(self, capacity, n):
        k = [[0 for w in range(capacity + 1)]
             for i in range(n + 1)]
        for i in range(n + 1):
            for w in range(capacity + 1):
                if i == 0 or w == 0:
                    k[i][w] = 0
                elif self.weights[i - 1] <= w:
                    k[i][w] = max(self.values[i - 1]
                                  + k[i - 1][w - self.weights[i - 1]],
                                  k[i - 1][w])
                else:
                    k[i][w] = k[i - 1][w]
        res = k[n][capacity]
        print("Best from Dynamic Programming is %d." % res)

        w = capacity
        print("Knapsack items by Dynamic Programming:    ", end="")
        for i in range(n, 0, -1):
            if res <= 0:
                break
            if res == k[i - 1][w]:
                continue
            else:
                print(i - 1, end=" ")
                res = res - self.values[i - 1]
                w = w - self.weights[i - 1]

    def print_ans(self):
            sum_w = 0
            sum_v = 0
            print("Items:", [i for i in range(self.item_size)])
            print("Values:", [self.values[i] for i in range(self.item_size)])
            print("Weights:", [self.weights[i] for i in range(self.item_size)])
            self.dynamic_knapsack(self.capacity, self.item_size)
            sol = self.genetic_knapsack()
            print("\nKnapsack items by Genetic Algorithm:    ", end="")
            for i in range(0, self.item_size):
                if sol[i] == 1:
                    sum_w += self.weights[i]
                    sum_v += self.values[i]
                    # print(i, end=" ")
                    print(i, end=" ")
            print("\nThe best solution is %d/%d." % (sum_v, sum_w))

item_size = int(input("Number of items: "))
capacity = int(input("Knapsack capacity: "))
max_weight = int(input("Largest Object Weight: "))
max_val = int(input("Largest Object Value: "))
pop_size = int(input("Population size: "))
mutate_prob = float(input("Mutation rate: "))
crossover_prob = float(input("Crossover rate: "))
generations = int(input("Stop after generations: "))

# crossover_prob = 0.95
# item_size = 50
# max_val = 100
# max_weight = 500
# pop_size = 1000
# mutate_prob = 0.05
# generations = 1000
# capacity = 1000
obj = Knapsack(item_size, max_val, max_weight, capacity, pop_size, mutate_prob, crossover_prob, generations)
obj.print_ans()
