import networkx as nx
import matplotlib.pyplot as plt
from math import exp
import matplotlib.patches as patches
from copy import deepcopy
from pprint import pprint



class TaskGraph(object):
    def __init__(self, graph, etc, processors, vm_base=0.1):
        self._graph = graph                 # DAG that represents dependencies between tasks
        self._etc = etc                     # Expect Time to Complete
        self._vm_base = vm_base
        self._processors = processors       # Scheduled tasks per processor

    def copy(self):
        return TaskGraph(graph=self._graph.copy(), etc=self._etc, vm_base=self._vm_base, processors=self._processors)

    def get_tasks(self):
        return self._graph.nodes()

    def get_tasks_of_processor(self, processor):
        return list(filter(lambda x: x.processor == processor and x.processed is True, self.get_tasks()))

    def _get_last_task(self, processor):
        tasks_of_processor = self.get_tasks_of_processor(processor)
        if len(tasks_of_processor) > 0:
            return max(tasks_of_processor, key=lambda x: x.ft)
        return None

    def insert_duplicated_task(self, original, duplicated):
        self._graph.add_node(duplicated)

        for predecessor in self._graph.predecessors(original):
            weight = self._graph.get_edge_data(predecessor, original)['weight']
            self._graph.add_edge(predecessor, duplicated, weight=weight)

        for successor in self._graph.successors(original):
            weight = self._graph.get_edge_data(original, successor)['weight']
            self._graph.add_edge(duplicated, successor, weight=weight)

    def get_etc(self, task, processor):
        return self._etc[task.index][processor.index]

    """
    Returns number of processor
    """
    def get_n_processors(self):
        return len(self._etc[0])

    """
    Returns entry task. It is used simplified DAG which has only one entry task.
    """
    def _get_entry_task(self):
        return list(filter(lambda x: len(self._graph.predecessors(x)) == 0 and x.duplicated is False, self.get_tasks()))[0]

    """
    Returns exit task. It is used simplified DAG which has only one exit task.
    """
    def _get_exit_task(self):
        return list(filter(lambda x: len(self._graph.successors(x)) == 0, self.get_tasks()))[0]

    """
    Returns communication cost between two tasks (edge weight)
    """
    def _get_c(self, predecessor, successor):
        if self._get_last_task(successor.processor) is not None and \
                        self._get_last_task(successor.processor).processor.index == predecessor.processor.index:
            return 0

        if predecessor.processor == successor.processor:
            return 0

        return self._graph.get_edge_data(predecessor, successor)['weight']

    """
    Returns ETC value (Expected Time to Complete) for given task
    """
    def _get_etc(self, task):
        return self._etc[task.index][task.processor.index]

    """
    Execution completion time of last task allocated to the processor
    """
    def _get_ava(self, processor):
        last_task = self._get_last_task(processor)
        if last_task is not None:
            return last_task.ft
        return 0

    """
    Calculates execution start time of task v_i on processor p_k (st(v_i, p_k))
    (2) st(v_i, p_k) = max{ ava(p_k), max(ft(v_j, p_x) + C(e_ji)) }
    """
    def _get_st(self, task):
        if task.processed is True:
            return task.st

        ava = self._get_ava(task.processor)
        predecessors = self._graph.predecessors(task)

        if len(predecessors) == 0:
            return ava

        for predecessor in predecessors:
            duplicated_predecessors = list(filter(lambda x: x.index == predecessor.index, predecessors))
            if len(duplicated_predecessors) > 1:
                for duplicated_predecessor in duplicated_predecessors:
                    if self._get_c(duplicated_predecessor, task) != 0:
                        predecessors.remove(duplicated_predecessor)
                        pass

        if task.index == 1:
            x = predecessors[0]
            print(task, self._get_ft(x))

        ft_plus_c_max = max(map(lambda x: self._get_ft(x) + self._get_c(x, task), predecessors))

        return max([ava, ft_plus_c_max])

    """
    Calculates execution finish time
    (3) ft(v_i, p_k) = st(v_i, p_k) + ETC(k, i)
    """
    def _get_ft(self, task):
        if task.processed is True:
            return task.ft

        start_time = self._get_st(task)
        finish_time = start_time + self._get_etc(task)

        return finish_time

    """
    Calculates total time
    (4) totalTime = min{ ft(v_exit, p_j) }
    """
    def get_total_time(self):
        exit_task = self._get_exit_task()
        exit_task.processor = self._processors[0]

        min_ft = None
        min_st = None
        min_processor = None

        for processor in self._processors:
            exit_task.processor = processor
            ft = self._get_ft(exit_task)

            if min_ft is None or ft < min_ft:
                min_ft = ft
                min_st = self._get_st(exit_task)
                min_processor = processor

        exit_task.ft = min_ft
        exit_task.st = min_st
        exit_task.processor = min_processor
        exit_task.processed = True

        return min_ft

    """
    Calculates the monetary cost of p_i pre unit time
    (5) VM_cost(i) = VM_base * exp^R_base
    """
    def _get_vm_cost(self, processor):
        return self._vm_base * exp(processor.capacity)

    """
    Calculates the monetary cost for executing task v_j on processor p_i
    (6) cost(i, j) = VM_cost(i) * ETC(i, j)
    """
    def _get_cost(self, task):
        return self._get_vm_cost(task.processor) * self._get_etc(task)

    """
    Calculates total cost
    (7) totalCost = sum(cost(i, j))
    """
    def get_total_cost(self):
        total_cost = 0
        for task in self.get_tasks():
            total_cost += self._get_cost(task)

        return total_cost

    """
    Clear previous configuration
    """
    def clear(self):
        for task in self.get_tasks():
            task.processed = False

    """
    Calculate start & finish times
    """
    def calculate_st_ft(self):
        entry_task = self._get_entry_task()
        entry_task.st = 0
        entry_task.ft = self._get_ft(entry_task)
        entry_task.processed = True
        successors = self._graph.successors(entry_task)
        while len(successors) > 1:
            # Process successors
            for successor in successors:
                if successor.duplicated is False:
                    successor.st = self._get_st(successor)
                    successor.ft = self._get_ft(successor)
                    successor.processed = True

            # Find all successors level above
            successors_of_successors = []
            for successor in successors:
                for successors_of_successor in self._graph.successors(successor):
                    if successors_of_successor not in successors_of_successors:
                        successors_of_successors.append(successors_of_successor)
            successors = successors_of_successors

    """
    Visualise the graph.
    """
    def draw_graph(self):
        nx.draw_networkx(self._graph, with_labels=True)
        plt.show()

    """
    Visualise scheduled tasks
    """
    def draw_schedule(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)

        for task in self.get_tasks():
            processor_index = task.processor.index
            left_offset = processor_index * 1.0

            if task.ft is None:
                print('task.ft is None:', task)
                continue

            rectangle = patches.Rectangle((left_offset, task.st),  0.9,  task.ft - task.st,
                                          alpha=0.2, edgecolor="#000000")
            ax.add_patch(rectangle)

            # Print task name
            rx, ry = rectangle.get_xy()
            cx = rx + rectangle.get_width() / 2.0
            cy = ry + rectangle.get_height() / 2.0
            ax.annotate('v' + str(task.index + 1), (cx, cy), ha='center', va='center')

        ax.autoscale_view(True, True, True)
        plt.show()

    """
    Print scheduled tasks
    """
    def print_schedule(self):
        for processor in self._processors:
            tasks_str = ''
            for task in filter(lambda x: x.processor == processor, self.get_tasks()):
                tasks_str += 'v' + str(task.index + 1) + ' (' + str(task.st) + ' - ' + str(task.ft) + '), '
            print('Processor #' + str(self._processors.index(processor) + 1) + ': ' + tasks_str)
