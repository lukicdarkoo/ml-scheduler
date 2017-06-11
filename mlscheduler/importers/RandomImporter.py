from random import randint
import networkx as nx
from misc.Task import Task


class RandomImporter(object):
    @staticmethod
    def get_graph(n_tasks=5, n_processors=3, min_length=1, max_length=100, max_number_of_connections=3):
        graph = nx.DiGraph()
        tasks = []

        # Generate tasks with random parameters
        for i in range(0, n_tasks):
            task = Task()
            task.set_index(i)

            for processor_index in range(0, n_processors):
                length = randint(min_length, max_length)
                task.set_length(processor_index, length)

            tasks.append(task)
        graph.add_nodes_from(tasks)

        # Generate random edges (connections between tasks)
        for i in range(0, n_tasks - 1):
            number_of_connections = randint(1, max_number_of_connections)

            for j in range(0, number_of_connections):
                connect_to_task_index = randint(i + 1, n_tasks - 1)
                graph.add_edge(tasks[i], tasks[connect_to_task_index])

        return graph
