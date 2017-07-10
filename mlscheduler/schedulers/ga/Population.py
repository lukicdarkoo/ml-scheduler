from math import floor
from sys import float_info
from schedulers.ga.Individual import Individual


class Population(object):
    def __init__(self, individuals, task_graph, w, k1, k2, k3, k4):
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

    def append(self, individual):
        self.individuals.append(individual)

    def calculate(self):
        if len(self.individuals) is 0:
            return

        for individual in self.individuals:
            self.set_schedule(individual.chromosome)
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
        if abs(self.t_max - self.t_min) < float_info.epsilon or \
                abs(self.c_max - self.c_min) < float_info.epsilon:
            return 1

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
        if abs(self.f_max - self.f_avg) < float_info.epsilon:
            return 1

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

        if abs(self.f_max - self.f_avg) < float_info.epsilon:
            return 1

        if f >= self.f_avg:
            return self._k3 * ((self.f_max - f) / (self.f_max - self.f_avg))
        return self._k4

    """
    Set task scheduling across processors. 
    :param schedule: Array of indexes that represent index of processor that should be assigned to task. 
        Length of list should be (number of tasks - 2) because first and last should not be in list 
        (set_schedule() has integrated logic for scheduling first & last task).
    """
    def set_schedule(self, schedule):
        self._task_graph.clear()

        # Schedule first task
        first_processor_index = self._task_graph._etc[0].index(min(self._task_graph._etc[0]))
        first_processor = self._task_graph._processors[first_processor_index]
        self._task_graph.get_tasks()[0].processor = first_processor

        # Schedule other tasks
        task_index = 1
        for processor_number in schedule:
            processor_index = processor_number - 1
            self._task_graph.get_tasks()[task_index].processor = self._task_graph._processors[processor_index]
            task_index += 1

        self._task_graph.calculate_st_ft()