from math import floor
from copy import deepcopy
from random import random, randint, uniform
from sys import float_info
from schedulers.ga.Individual import Individual
from schedulers.ga.Population import Population


class GAScheduler(object):
    def __init__(self, task_graph, nind=100, max_terminate=150, no_change_terminate=10, w=0.25, k1=0.6, k2=0.8, k3=0.1, k4=0.05):
        self._nind = nind
        self._task_graph = task_graph
        self._no_change_terminate = no_change_terminate
        self._max_terminate = max_terminate
        self._w = w
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        self._k4 = k4

    def get_random_individual(self, population):
        temp_fitness_sum = 0
        random_fitness_boundary = uniform(0, population.f_sum)
        sorted_individuals = sorted(population.individuals, key=lambda x: x.fitness, reverse=True)

        for individual in sorted_individuals:
            temp_fitness_sum += individual.fitness
            if temp_fitness_sum >= random_fitness_boundary:
                return individual

    def selection_operation(self, population):
        individuals_new = []
        for individual in population.individuals:
            n_i = population.get_n_i(individual)
            individual.n_i_fraction = n_i - floor(n_i)

            for i in range(int(floor(n_i))):
                individuals_new.append(deepcopy(individual))

        individuals_new.sort(key=lambda x: x.n_i_fraction, reverse=True)
        individuals_new = individuals_new[0:population.get_n_next_gen()]
        return Population(task_graph=self._task_graph, individuals=individuals_new, w=self._w, k1=self._k1, k2=self._k2, k3=self._k3, k4=self._k4)

    @staticmethod
    def crossover_operation(population, individual1, individual2):
        f_prim = max([individual1.fitness, individual2.fitness])

        # Crossover genome (by taking care about probability of crossover)
        if population.get_p_c(f_prim) > random():
            individual = deepcopy(individual1)

            for i in range(0, randint(1, len(individual1.chromosome))):
                individual.chromosome[i] = individual2.chromosome[i]
            return individual

        return None

    def mutation_operation(self, population, individual):
        if population.get_p_m(individual) > random():
            genome_index = randint(0, len(individual.chromosome) - 1)
            individual.chromosome[genome_index] = randint(0, self._task_graph.get_n_processors())

    def generate_initial_population(self, n_tasks):
        individuals = []
        for i in range(self._nind):
            chromosome = []
            for j in range(n_tasks):
                chromosome.append(randint(1, self._task_graph.get_n_processors()))
            individuals.append(Individual(chromosome=chromosome))

        return Population(task_graph=self._task_graph, individuals=individuals, w=self._w, k1=self._k1, k2=self._k2, k3=self._k3, k4=self._k4)

    @staticmethod
    def print_fitness(population):
        print(list(map(lambda x: population.get_fitness(x), population.individuals)))

    def calculate(self):
        # Make initial population
        population = self.generate_initial_population(n_tasks=8)
        no_change_n = 0
        previous_total_cost = 0

        for i in range(self._max_terminate):
            # Generate new population
            # Initial population for next generation is list of elite individuals (individuals with  greatest fitness)
            population_new = self.selection_operation(population)
            elite_population_num = len(population_new.individuals)

            # Add additional individuals to make new generation of NIND individuals
            for j in range(elite_population_num, self._nind):
                individual = None
                individual1 = self.get_random_individual(population)
                individual2 = self.get_random_individual(population)

                # Try to  apply crossover
                crossover_individual = self.crossover_operation(population, individual1, individual2)

                if crossover_individual is None:
                    individual = individual1
                else:
                    individual = crossover_individual

                # Try to apply mutation
                self.mutation_operation(population, individual)
                population_new.append(individual)

            population_new.calculate()

            # Investigate break conditions
            current_total_cost = population.individuals[0].total_cost
            if abs(previous_total_cost - current_total_cost) < float_info.epsilon:
                no_change_n += 1

            if no_change_n >= self._no_change_terminate:
                return population.individuals[0]

            previous_total_cost = current_total_cost
            population = population_new

        return population.individuals[0]







