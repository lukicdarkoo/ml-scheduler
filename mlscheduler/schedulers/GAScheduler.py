class Entity(object):
    def __init__(self):
        self.t = None
        self.c = None
        self.f = None


class Population(object):
    def __init__(self, chromosomes, task_graph, w=0.25, k1=0.6, k2=0.8, k3=0.1, k4=0.05):
        self._chromosomes = chromosomes
        self._task_graph = task_graph
        self._entities = []

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

    def get_entity(self, index):
        return self._entities[index]

    def calculate(self):
        for chromosome in self._chromosomes:
            entity = Entity()
            self._task_graph.set_schedule(chromosome)
            entity.t = self._task_graph.get_total_time()
            entity.c = self._task_graph.get_total_cost()
            self._entities.append(entity)

            if entity.c > self.c_max or self.c_max is None:
                self.c_max = entity.c
            if entity.c < self.c_min or self.c_min is None:
                self.c_min = entity.c
            if entity.t > self.t_max or self.t_max is None:
                self.t_max = entity.c
            if entity.t < self.t_min or self.t_min is None:
                self.t_min = entity.c

        # Calculate F_max and F_avg
        f_sum = 0
        for entity in self._entities:
            entity.fitness = self.get_fitness(entity)
            f_sum += entity.fitness
            if self.f_max is None or entity.fitness > self.f_max:
                self.f_max = entity.fitness

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

    """
    Calculates a fitness of entity
    (10) F = w * ((T_max - T) / (T_max - T_min)) + (1 - w) * ((C_max - C) / (C_max - C_min))
    """
    def get_fitness(self, entity):
        return self._w * ((self.t_max - entity.t) / (self.t_max - self.t_min)) + \
            (1 - self._w) * ((self.c_max - entity.c) / (self.c_max - self.c_min))


class GAScheduler(object):
    def __init__(self, nind=10):
        self._nind = nind

    def calculate(self):
        pass



