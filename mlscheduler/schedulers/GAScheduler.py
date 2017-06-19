from math import floor
from copy import deepcopy
from random import random, randint


class Individual(object):
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.total_time = None
        self.total_cost = None
        self.fitness = None
        self.n_i_fraction = None


class Population(object):
    def __init__(self, individuals, task_graph, w=0.25, k1=0.6, k2=0.8, k3=0.1, k4=0.05):
        self.individuals = individuals
        self._task_graph = task_graph

        self._w = w
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        self._k4 = k4

        self.t_max = None
        self.t_min = None
        self.c_max = None
        self.c_min = None
        self.f_avg = None
        self.f_max = None
        self.f_sum = None

        self.calculate()

    def calculate(self):
        for individual in self.individuals:
            self._task_graph.set_schedule(individual.chromosome)
            individual.total_time = self._task_graph.get_total_time()
            individual.total_cost = self._task_graph.get_total_cost()

            if self.c_max is None or individual.total_cost > self.c_max:
                self.c_max = individual.total_cost
            if self.c_min is None or individual.total_cost < self.c_min:
                self.c_min = individual.total_cost
            if self.t_max is None or individual.total_time > self.t_max:
                self.t_max = individual.total_time
            if self.t_min is None or individual.total_time < self.t_min:
                self.t_min = individual.total_time

        # Calculate sum(F), F_max & F_avg
        self.f_sum = 0
        for individual in self.individuals:
            individual.fitness = self.get_fitness(individual)
            self.f_sum += individual.fitness
            if self.f_max is None or individual.fitness > self.f_max:
                self.f_max = individual.fitness
        self.f_avg = self.f_sum / len(self.individuals)

    """
    Calculates a fitness of individual
    (10) F = w * ((T_max - T) / (T_max - T_min)) + (1 - w) * ((C_max - C) / (C_max - C_min))
    """
    def get_fitness(self, individual):
        return self._w * ((self.t_max - individual.total_time) / (self.t_max - self.t_min)) + \
            (1 - self._w) * ((self.c_max - individual.total_cost) / (self.c_max - self.c_min))

    """
    Calculates number of i_th individuals in next generation (N_i)
    (11) N_i = NIND * (F_i / sum(F_i))
    """
    def get_n_i(self, individual):
        return len(self.individuals) * (individual.fitness / self.f_sum)

    """
    NIND - sum(N_i)
    """
    def get_n_next_gen(self):
        nind = len(self.individuals)
        n_sum = sum(map(lambda entity: floor(self.get_n_i(entity)), self.individuals))
        return nind - n_sum

    """
    Calculates probability of crossover (P_c)
    (12)    P_c = k1 * ((f_max - f_prim) / (f_max - f_avg)) , f_prim >= f_avg
            P_c = k2                                        , f_prim < f_avg
    """
    def get_p_c(self, f_prim):
        if f_prim >= self.f_avg:
            return self._k1 * ((self.f_max - f_prim) / (self.f_max - self.f_avg))
        return self._k2

    """
    Calculates probability of mutation (P_m)
    (13)    P_m = k3 * ((f_max - f) / (f_max - f_avg))  , f >= f_avg
            P_c = k4                                    , f < f_avg
    """
    def get_p_m(self, entity):
        f = entity.fitness
        if f >= self.f_avg:
            return self._k3 * ((self.f_max - f) / (self.f_max - self.f_avg))
        return self._k4


class GAScheduler(object):
    def __init__(self, task_graph, nind=100):
        self._nind = nind
        self._task_graph = task_graph

    def selection_operation(self, population):
        individuals_new = []
        for individual in population.individuals:
            n_i = population.get_n_i(individual)
            individual.n_i_fraction = n_i - floor(n_i)

            for i in range(int(floor(n_i))):
                individuals_new.append(deepcopy(individual))

        individuals_new.sort(key=lambda x: x.n_i_fraction, reverse=True)
        individuals_new = individuals_new[0:population.get_n_next_gen()]
        return Population(task_graph=self._task_graph, individuals=individuals_new)

    @staticmethod
    def crossover_operation(population):
        previous_individual = population.individuals[0]
        for individual_index in range(1, len(population.individuals)):
            individual = population.individuals[individual_index]
            f_prim = max([previous_individual.fitness, individual.fitness])

            # Crossover genome (by taking care about probability of crossover)
            if population.get_p_c(f_prim) > random():
                for i in range(len(individual.chromosome), 2):
                    t = individual.chromosome[i]
                    individual.chromosome[i] = previous_individual[i]
                    previous_individual[i] = t

            # Save previous individual
            previous_individual = individual

    def mutation_operation(self, population):
        for individual in population.individuals:
            if population.get_p_m(individual) > random():
                genome_index = randint(0, len(individual.chromosome))
                individual.chromosome[genome_index] = randint(0, self._task_graph.get_n_processors())

    def generate_initial_population(self, n_tasks):
        individuals = []
        for i in range(self._nind):
            chromosome = []
            for j in range(n_tasks):
                chromosome.append(randint(1, self._task_graph.get_n_processors()))
            individuals.append(Individual(chromosome=chromosome))
            print(chromosome)

        return Population(task_graph=self._task_graph, individuals=individuals)

    @staticmethod
    def print_fitness(population):
        print(list(map(lambda x: population.get_fitness(x), population.individuals)))

    def calculate(self):
        # Make initial population
        population = self.generate_initial_population(8)
        self.print_fitness(population)


        population_new = self.selection_operation(population)

        self.crossover_operation(population_new)
        self.mutation_operation(population_new)

        population_new.calculate()
        # self.print_fitness(population_new)
        self.print_fitness(self.selection_operation(population_new))






