from math import floor
from sys import float_info
from schedulers.ga.Individual import Individual


class Population(object):
    """
    Model of population in multi-population genetic algorithm
    """
    def __init__(self, individuals, task_graph, w, k1, k2, k3, k4):
        """
        Constructs an instance of Population

        :param individuals: Array of Individual that belongs to the population
        :param task_graph: Graph of tasks
        :param w: Optimisation variable (0 - 1), 0 aiming for a lower cost, 1 aiming for a lower time consumption
        :param k1: First constant in crossover operation
        :param k2: Second constant in crossover operation
        :param k3: First constant in mutation operation
        :param k4: Second constant in mutation operation
        """
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

        self.finished = False

        self.no_change_n = 0
        self.total_cost = 0

        self.calculate()

    def append(self, individual):
        """
        Add an individual to the Population

        :param individual: Individual to be added in population
        """
        self.individuals.append(individual)

    def calculate(self):
        """
        Calculates `c_max`, `c_min`, `t_max`, `t_min`, `f_avg`, `f_max` & `f_sum` variables required to determine
        fitness value of each individual
        """
        if len(self.individuals) is 0:
            return

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

    def get_fitness(self, individual):
        """
        Calculates a fitness of individual
        (10) F = w * ((T_max - T) / (T_max - T_min)) + (1 - w) * ((C_max - C) / (C_max - C_min))

        :param individual: Individual that we want to calculate fitness for
        :return Fitness value
        """
        if self._w == 1:
            return 1 / individual.total_time

        if self._w == 0:
            return 1 / individual.total_cost

        if abs(self.t_max - self.t_min) == 0 or \
                abs(self.c_max - self.c_min) == 0:
            return 1 + 1 / individual.total_cost

        return self._w * ((self.t_max - individual.total_time) / (self.t_max - self.t_min)) + \
            (1 - self._w) * ((self.c_max - individual.total_cost) / (self.c_max - self.c_min))

    def get_n_i(self, individual):
        """
        Calculates number of i_th individuals in next generation (N_i)
        (11) N_i = NIND * (F_i / sum(F_i))
        """
        return len(self.individuals) * (individual.fitness / self.f_sum)

    def get_n_next_gen(self):
        """
        NIND - sum(N_i)
        """
        nind = len(self.individuals)
        n_sum = sum(map(lambda entity: floor(self.get_n_i(entity)), self.individuals))
        return nind - n_sum

    def get_p_c(self, f_prim):
        """
        Calculates probability of crossover (P_c)
        (12)    P_c = k1 * ((f_max - f_prim) / (f_max - f_avg)) , f_prim >= f_avg
                P_c = k2                                        , f_prim < f_avg
        """
        if abs(self.f_max - self.f_avg) < float_info.epsilon:
            return 1

        if f_prim >= self.f_avg:
            return self._k1 * ((self.f_max - f_prim) / (self.f_max - self.f_avg))
        return self._k2

    def get_p_m(self, entity):
        """
        Calculates probability of mutation (P_m)
        (13)    P_m = k3 * ((f_max - f) / (f_max - f_avg))  , f >= f_avg
                P_c = k4                                    , f < f_avg
        """
        f = entity.fitness

        if abs(self.f_max - self.f_avg) < float_info.epsilon:
            return 1

        if f >= self.f_avg:
            return self._k3 * ((self.f_max - f) / (self.f_max - self.f_avg))
        return self._k4


