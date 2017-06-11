from random import randint
import networkx as nx
from misc.Task import Task


class RandomImporter(object):
    @staticmethod
    def get_graph(n_tasks=20, n_processors=3, min_length=1, max_length=100, max_number_of_connections=3):
        graph = nx.DiGraph()
        tasks = []

        # Generate tasks with random parameters
        for i in range(0, n_tasks):
            processor = randint(0, n_processors - 1)
            length = randint(min_length, max_length)

            tasks.append(Task(processor, length))
        graph.add_nodes_from(tasks)

        # Generate random edges (connections between tasks)
        for i in range(0, n_tasks - 1):
            number_of_connections = randint(1, max_number_of_connections)

            for j in range(0, number_of_connections):
                connect_to_task_index = randint(i, n_tasks - 1)
                graph.add_edge(tasks[i], tasks[connect_to_task_index])

        # Set name to first & last node
        tasks[0].set_name('F')
        tasks[n_tasks - 1].set_name('L')

        return graph
