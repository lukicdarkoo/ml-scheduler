import networkx as nx
import matplotlib.pyplot as plt
from math import exp


class TaskGraph(object):
    def __init__(self, tasks, graph, etc, vm_base=0.1):
        self._tasks = tasks
        self._graph = graph
        self._etc = etc
        self._tasks_per_processor = []
        self._n_processors = len(etc[0])
        self._vm_base = vm_base

    """
    Returns number of tasks scheduled to the specific processor
    """
    def get_n_tasks(self, processor):
        if self._tasks_per_processor is not None:
            return 0
        return len(self._tasks_per_processor[processor])

    """
    Returns last task scheduled to the specific processor
    """
    def get_last_task(self, processor):
        n_tasks = self.get_n_tasks(processor)
        if n_tasks > 0:
            return self._tasks_per_processor[self.get_n_tasks(processor) - 1]
        return None

    """
    Returns exit task. It is used simplified DAG which has only one exit task.
    """
    def get_exit_task(self):
        return self._tasks[len(self._tasks) - 1]

    """
    Returns communication cost between two tasks (edge weight)
    """
    def get_c(self, task1, task2):
        return self._graph.get_edge_data(task1, task2)['weight']

    """
    Execution completion time of last task allocated to the processor
    """
    def get_ava(self, processor):
        if self.get_last_task(processor) is not None:
            return self.get_last_task(processor).ft
        return 0

    """
    Calculates execution start time of task v_i on processor p_k (st(v_i, p_k))
    (2) st(v_i, p_k) = max{ ava(p_k), max(ft(v_j, p_x) + C(e_ji)) }
    """
    def get_st(self, task):
        ava = self.get_ava(task.processor)
        predecessors = self._graph.predecessors(task)
        ft_plus_c_max = 0

        if len(predecessors) == 0:
            return ava

        # Else
        for predecessor in predecessors:
            if self.get_ft(predecessor) + self.get_c(predecessor, task) > ft_plus_c_max:
                ft_plus_c_max = self.get_ft(predecessor) + self.get_c(predecessor, task)
        return max([ava, ft_plus_c_max])

    """
    Calculates execution finish time
    (3) ft(v_i, p_k) = st(v_i, p_k) + ETC(k, i)
    """
    def get_ft(self, task):
        start_time = self.get_st(task)
        finish_time = start_time + self._etc[task.index][task.processor]

        if task.processed is False:
            self._tasks_per_processor[task.processor].append(task)
            task.processed = True
            task.st = start_time
            task.ft = finish_time

        return finish_time

    """
    Calculates total time
    (4) totalTime = min{ ft(v_exit, p_j) }
    """
    def get_total_time(self):
        exit_task = self.get_exit_task()
        exit_task.processor = 0

        total_time = self.get_ft(exit_task)
        for processor_index in range(1, self._n_processors):
            exit_task.processor = processor_index
            temp_total_time = self.get_ft(exit_task)

            if temp_total_time < total_time:
                total_time = temp_total_time

        return total_time

    """
    Calculates the monetary cost of p_i pre unit time
    (5) VM_cost(i) = VM_base * exp^R_base
    """
    def get_vm_cost(self, processor):
        # TODO: "R_base denotes the speed ratio between them", between what?
        return self._vm_base * exp(1)

    """
    Calculates the monetary cost for executing task v_j on processor p_i
    (6) cost(i, j) = VM_cost(i) * ETC(i, j)
    """
    def get_cost(self, task):
        return self.get_vm_cost(task.processor) * self._etc[task.index][task.processor]

    """
    Calculates total cost
    (7) totalCost = sum(cost(i, j))
    """
    def get_total_cost(self):
        total_cost = 0
        for task in self._tasks:
            total_cost += self.get_cost(task)

        return total_cost

    """
    Set task scheduling across processors. 
    :param schedule: Array of indexes that represent index of processor that should be assigned to task. 
        Length of list should be (number of tasks - 2) because first and last tasks are excluded from list.
    """
    def set_schedule(self, schedule):
        # Clear previous configuration
        for task in self._tasks:
            task.ft = None
            task.st = None
            task.processed = False

        self._tasks_per_processor.clear()
        for i in range(self._n_processors):
            self._tasks_per_processor.append([])

        # Schedule first task
        first_processor = self._etc[0].index(min(self._etc[0]))
        self._tasks[0].processor = first_processor

        # Schedule other tasks
        task_index = 1
        for processor_number in schedule:
            processor_index = processor_number - 1
            self._tasks[task_index].processor = processor_index
            task_index += 1

    """
    Visualise the graph.
    """
    def draw(self):
        nx.draw_networkx(self._graph, with_labels=True)
        plt.show()

