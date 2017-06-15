class Fitness(object):
    def __init__(self, tasks):
        self.__tasks = tasks
        self.__tasks_per_processor = []

    """
    @staticmethod
    def __find_roots(graph):
        return [n for n, d in graph.in_degree().items() if d == 0]

    @staticmethod
    def __calculate_length(graph, node):
        successors = graph.successors(node)
    """

    def calculate(self, chromosome):
        for i in range(len(chromosome)):
            self.__tasks_per_processor[chromosome[i]].append(self.__tasks[i])

