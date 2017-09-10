from random import randint, uniform
import networkx as nx
from misc.Task import Task
from misc.TaskGraph import TaskGraph
from misc.Processor import Processor


class RandomImporter(object):
    @staticmethod
    def get_task_graph(n_tasks=10, n_processors=3, min_length=1, max_length=100):
        graph = nx.DiGraph()
        tasks = []

        # Generate tasks with random parameters
        for i in range(0, n_tasks):
            tasks.append(Task(randint(min_length, max_length), index=i))
        graph.add_nodes_from(tasks)

        # Generate random edges (connections between tasks)
        last_added = [0]
        while True:
            min_n = max(last_added) + 1
            max_n = min(n_tasks - 1, randint(min_n + 2, min_n + 4))
            for i in last_added:
                for j in range(min_n, max_n):
                    graph.add_edge(tasks[i], tasks[j], weight=randint(10, 30))
            last_added = range(min_n, max_n)

            if max_n == n_tasks - 1:
                for i in last_added:
                    graph.add_edge(tasks[i], tasks[n_tasks - 1], weight=randint(1, 30))
                break

        # Generate ETC table
        etc = []
        for i in range(0, n_tasks):
            etc.append([])
            for j in range(0, n_processors):
                etc[i].append(randint(10, 30))

        # Generate processors
        processors = []
        for i in range(0, n_processors):
            processors.append(Processor(capacity=uniform(0, 1), index=i))

        return TaskGraph(graph=graph, etc=etc, processors=processors)
