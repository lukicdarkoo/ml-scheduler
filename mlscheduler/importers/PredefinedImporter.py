import networkx as nx
from misc.Task import Task
from misc.TaskGraph import TaskGraph
from misc.Processor import Processor

"""
Module provides data given in "Cost-Effective Scheduling Precedence Constrained Tasks in Cloud Computing"
"""


class PredefinedImporter(object):
    @staticmethod
    def get_task_graph():
        graph = nx.DiGraph()

        # Generate tasks
        tasks = [
            Task(13, index=0),
            Task(17, index=1),
            Task(14, index=2),
            Task(9, index=3),
            Task(12, index=4),
            Task(13, index=5),
            Task(11, index=6),
            Task(10, index=7),
            Task(17, index=8),
            Task(15, index=9)
        ]
        graph.add_nodes_from(tasks)

        # Generate edges (connections between tasks)
        graph.add_edge(tasks[0], tasks[1], weight=18)
        graph.add_edge(tasks[0], tasks[2], weight=12)
        graph.add_edge(tasks[0], tasks[3], weight=9)
        graph.add_edge(tasks[0], tasks[4], weight=11)
        graph.add_edge(tasks[0], tasks[5], weight=14)

        graph.add_edge(tasks[1], tasks[7], weight=19)
        graph.add_edge(tasks[1], tasks[8], weight=16)
        graph.add_edge(tasks[2], tasks[6], weight=23)
        graph.add_edge(tasks[3], tasks[7], weight=27)
        graph.add_edge(tasks[3], tasks[8], weight=23)
        graph.add_edge(tasks[4], tasks[8], weight=13)
        graph.add_edge(tasks[5], tasks[7], weight=15)

        graph.add_edge(tasks[6], tasks[9], weight=17)
        graph.add_edge(tasks[7], tasks[9], weight=11)
        graph.add_edge(tasks[8], tasks[9], weight=13)

        # Generate ETC table
        etc = [
            [14, 16, 9],
            [13, 19, 18],
            [11, 13, 19],
            [13, 8, 7],
            [12, 13, 10],
            [13, 16, 9],
            [7, 15, 11],
            [5, 11, 14],
            [18, 12, 20],
            [21, 7, 16]
        ]

        # Generate processors
        processors = [
            Processor(capacity=0.3, index=0),
            Processor(capacity=0.6, index=1),
            Processor(capacity=1, index=2)
        ]

        return TaskGraph(graph=graph, etc=etc, processors=processors)

