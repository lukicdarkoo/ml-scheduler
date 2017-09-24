from math import floor
from copy import deepcopy
from random import random, randint, uniform
from sys import float_info
from schedulers.ga.Individual import Individual
from schedulers.ga.Population import Population


class GAScheduler(object):
    """
    Task scheduler based on multi-population genetic algorithm
    """

    def __init__(self, task_graph, nind=100, max_terminate=150, no_change_terminate=10, n_populations=5, w=0.25, k1=0.6, k2=0.8, k3=0.1, k4=0.05):
        """
        Constructor of genetic algorithm based scheduler

        :param task_graph: TaskGraph
        :param nind: Number of individuals
        :param max_terminate: Max number of generation before termination
        :param no_change_terminate: Max number of generation in which the best individual doesn't have any performance
        improvements compared to previous one
        :param n_populations: Number of population
        :param w: Optimisation variable (0 - 1), 0 aiming for a lower cost, 1 aiming for a lower time consumption
        :param k1: First constant in crossover operation
        :param k2: Second constant in crossover operation
        :param k3: First constant in mutation operation
        :param k4: Second constant in mutation operation
        """
        self._nind = nind
        self._task_graph = task_graph
        self._no_change_terminate = no_change_terminate
        self._max_terminate = max_terminate
        self._w = w
        self._k1 = k1
        self._k2 = k2
        self._k3 = k3
        self._k4 = k4
        self._n_populations = n_populations

    def get_random_individual(self, population):
        """
        Choosing a random individual based on roulette wheel selection algorithm

        :param population: Population in which we are searching for an Individual
        :return: Chosen Individual
        """
        temp_fitness_sum = 0
        random_fitness_boundary = uniform(0, population.f_sum)
        sorted_individuals = sorted(population.individuals, key=lambda x: x.fitness, reverse=True)

        for individual in sorted_individuals:
            temp_fitness_sum += individual.fitness
            if temp_fitness_sum >= random_fitness_boundary:
                return individual

    def selection_operation(self, population):
        """
        Generates a new population based on previous population. Initial individuals in population are generated
        by cloning elite individuals. Elite individuals are chosen by fraction part of N_i.
        (11) N_i = NIND * (F_i / sum(F_i))

        :param population: Previous population
        :return: Generated population
        """

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
        """
        Performs crossover operation. Look at Population.get_p_c()

        :param population: Population that individual1 & individual2 belong to
        :param individual1: First individual that participate in crossover operation
        :param individual2: Second individual that participate in crossover operation
        :return: Individual if crossover is performed or None if crossover is not performed
        """

        f_prim = max([individual1.fitness, individual2.fitness])

        # Crossover genome (by taking care about probability of crossover)
        if population.get_p_c(f_prim) > random():
            individual = deepcopy(individual1)

            for i in range(0, randint(1, len(individual1.chromosome))):
                individual.chromosome[i] = individual2.chromosome[i]
            return individual

        return None

    def mutation_operation(self, population, individual):
        """
        Performs mutation operation. Look at Population.get_p_m()

        :param population: Population that individual1 belong to
        :param individual: Individual that participate in mutation operation. This individual will be change
        if conditions are satisfied.
        """
        if population.get_p_m(individual) > random():
            genome_index = randint(0, len(individual.chromosome) - 1)
            individual.chromosome[genome_index] = randint(0, self._task_graph.get_n_processors())

    def generate_initial_population(self, n_tasks):
        """
        Generates initial population with random chromosomes

        :param n_tasks: Number of tasks that have to be scheduled
        :return: Populations with random chromosomes
        """
        individuals = []
        for i in range(self._nind):
            chromosome = []
            for j in range(n_tasks):
                chromosome.append(randint(1, self._task_graph.get_n_processors()))
            individuals.append(Individual(chromosome=chromosome))

        return Population(task_graph=self._task_graph, individuals=individuals, w=self._w, k1=self._k1, k2=self._k2, k3=self._k3, k4=self._k4)

    def _get_individual_with_max_fitness(self, population):
        """
        Search for individual that has the highest fitness value
        :param population: Population in which we search for individual
        :return: Individual with the highest fitness value in Population population
        """
        return max(population.individuals, key=lambda x: x.fitness)

    def _get_graph_with_max_fitness(self, population):
        """
        Generates TaskGraph based on chromosome that the highest value in Population population
        :param population: Population in which we search for individual
        :return: TaskGraph with the highest fitness value in Population population
        """
        best_individual = self._get_individual_with_max_fitness(population)
        self._task_graph.set_schedule(best_individual.chromosome)
        return self._task_graph.copy()

    def _get_graph_with_max_fitness_mp(self, populations):
        """
        Generates TaskGraph based on chromosome that the highest value in array of populations
        :param populations: Array of populations in which we search for individual
        :return: TaskGraph with the highest fitness value in array of populations
        """
        best_individual = None
        for population in populations:
            individual = self._get_individual_with_max_fitness(population)
            if best_individual is None or individual.fitness > best_individual.fitness:
                best_individual = individual
        self._task_graph.set_schedule(best_individual.chromosome)
        return self._task_graph.copy()

    def calculate(self):
        """
        Finding a TaskGraph with lowest price or time (highest fitness value)
        :return: TaskGraph with lowest price or time
        """
        finished_populations_indexes = []

        # Make initial population
        populations = self._n_populations * [None]
        for i in range(0, self._n_populations):
            populations[i] = self.generate_initial_population(n_tasks=(len(self._task_graph.get_tasks()) - 2))

        # Start an evolution
        for i in range(self._max_terminate):
            for pi in range(0, self._n_populations):
                # Skip population if population already hit NO_CHANGE_TERMINATE
                if pi in finished_populations_indexes:
                    break

                # Generate new population
                # Initial population for next generation is list of elite individuals
                # (individuals with greatest fitness)
                population_new = self.selection_operation(populations[pi])
                elite_population_num = len(population_new.individuals)

                # Add additional individuals to make new generation of NIND individuals
                for j in range(elite_population_num, self._nind):
                    individual = None
                    individual1 = self.get_random_individual(populations[pi])
                    individual2 = self.get_random_individual(populations[pi])

                    # Try to apply crossover operation
                    crossover_individual = self.crossover_operation(populations[pi], individual1, individual2)
                    if crossover_individual is None:
                        individual = individual1
                    else:
                        individual = crossover_individual

                    # Try to apply mutation operation
                    self.mutation_operation(populations[pi], individual)
                    population_new.append(individual)

                # Calculate sts and fts for a new population
                population_new.calculate()

                # Investigate break conditions
                current_total_cost = self._get_individual_with_max_fitness(populations[pi]).total_cost
                new_total_cost = self._get_individual_with_max_fitness(population_new).total_cost
                if abs(new_total_cost - current_total_cost) < float_info.epsilon:
                    populations[pi].no_change_n += 1
                    if populations[pi].no_change_n >= self._no_change_terminate:
                        finished_populations_indexes.append(pi)

                # Replace with a new population
                populations[pi] = population_new

        return self._get_graph_with_max_fitness_mp(populations)

    @staticmethod
    def print_fitness(population):
        print(list(map(lambda x: population.get_fitness(x), population.individuals)))