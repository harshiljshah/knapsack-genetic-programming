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
