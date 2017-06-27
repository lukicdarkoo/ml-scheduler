class Individual(object):
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.total_time = None
        self.total_cost = None
        self.fitness = None
