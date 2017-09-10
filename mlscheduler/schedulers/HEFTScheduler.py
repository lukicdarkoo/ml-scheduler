from math import floor
from copy import deepcopy
from random import random, randint, uniform
from sys import float_info


class HEFTScheduler(object):
    def __init__(self, task_graph):
        self._task_graph = task_graph

    def calculate(self):
        self._task_graph.set_heft_schedule()
        return self._task_graph.copy()


