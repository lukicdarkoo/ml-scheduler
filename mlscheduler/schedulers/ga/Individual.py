class Individual(object):
    """
    Model of individual in population of multi-population genetic algorithm
    """
    def __init__(self, chromosome):
        """
        Constructs an instance of Individual

        :param chromosome: Array of genomes
        """
        self.chromosome = chromosome
        self.total_time = None
        self.total_cost = None
        self.fitness = None
