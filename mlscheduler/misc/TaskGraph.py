import networkx as nx
import matplotlib.pyplot as plt
from math import exp
import matplotlib.patches as patches


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
        return len(self._tasks_per_processor[processor])

    """
    Returns last task scheduled to the specific processor
    """
    def get_last_task(self, processor):
        n_tasks = self.get_n_tasks(processor)
        if n_tasks > 0:
            return self._tasks_per_processor[processor][n_tasks - 1]
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
        if task1.processor != task2.processor:
            return self._graph.get_edge_data(task1, task2)['weight']
        return 0

    """
    Execution completion time of last task allocated to the processor
    """
    def get_ava(self, processor):
        last_task = self.get_last_task(processor)
        if last_task is not None:
            # print(last_task, last_task.st, last_task.ft)
            return last_task.ft
        return 0

    """
    Calculates execution start time of task v_i on processor p_k (st(v_i, p_k))
    (2) st(v_i, p_k) = max{ ava(p_k), max(ft(v_j, p_x) + C(e_ji)) }
    """
    def get_st(self, task):
        if task.processed is True:
            return task.st

        ava = self.get_ava(task.processor)
        predecessors = self._graph.predecessors(task)
        ft_plus_c_max = 0

        if len(predecessors) == 0:
            return ava

        for predecessor in predecessors:
            ft_plus_c = self.get_ft(predecessor) + self.get_c(predecessor, task)
            if ft_plus_c > ft_plus_c_max:
                ft_plus_c_max = ft_plus_c
            print(predecessor, predecessor.st, predecessor.ft, ft_plus_c)
        return max([ava, ft_plus_c_max])

    """
    Calculates execution finish time
    (3) ft(v_i, p_k) = st(v_i, p_k) + ETC(k, i)
    """
    def get_ft(self, task):
        if task.processed is True:
            return task.ft

        start_time = self.get_st(task)
        finish_time = start_time + self._etc[task.index][task.processor]

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
        Length of list should be (number of tasks - 2) because first and last should not be in list 
        (set_schedule() has integrated logic for scheduling first & last task).
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

        # Calculate start & finish times
        self._tasks[0].st = 0
        self._tasks[0].ft = self.get_ft(self._tasks[0])
        self._tasks[0].processed = True
        self._tasks_per_processor[self._tasks[0].processor].append(self._tasks[0])
        successors = self._graph.successors(self._tasks[0])
        while len(successors) > 1:
            # Process successors
            for successor in successors:
                successor.st = self.get_st(successor)
                successor.ft = self.get_ft(successor)
                successor.processed = True
                self._tasks_per_processor[successor.processor].append(successor)

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
        fig1 = plt.figure()
        ax = fig1.add_subplot(111)

        for processor_index in range(len(self._tasks_per_processor)):
            for task in self._tasks_per_processor[processor_index]:
                left_offset = processor_index * 1.0
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
    def print_scheduled_tasks(self):
        for processor in self._tasks_per_processor:
            tasks_str = ''
            for task in processor:
                tasks_str += 'v' + str(task.index + 1) + ' (' + str(task.st) + ' - ' + str(task.ft) + '), '

            print('Processor #' + str(self._tasks_per_processor.index(processor) + 1) + ': ' + tasks_str)
