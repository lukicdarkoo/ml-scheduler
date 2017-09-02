import networkx as nx
import matplotlib.pyplot as plt
from math import exp
import matplotlib.patches as patches


class TaskGraph(object):
    def __init__(self, graph, etc, processors, task_duplicator=None, vm_base=0.1, alpha=1, beta=1):
        self._graph = graph                 # DAG that represents dependencies between tasks
        self._etc = etc                     # Expect Time to Complete
        self._vm_base = vm_base
        self._processors = processors       # Scheduled tasks per processor
        self._task_duplicator = task_duplicator
        self._alpha = alpha
        self._beta = beta

    def copy(self):
        return TaskGraph(graph=self._graph.copy(), etc=self._etc, vm_base=self._vm_base, processors=self._processors)

    def set_task_duplicator(self, task_duplicator):
        self._task_duplicator = task_duplicator

    def get_tasks(self):
        return self._graph.nodes()

    def get_tasks_of_processor(self, processor):
        return list(filter(lambda x: x.processor == processor and (x.processed is True or x.duplicated is True), self.get_tasks()))

    def _get_last_task(self, processor):
        tasks_of_processor = list(filter(lambda x: x.processed is True, self.get_tasks_of_processor(processor)))
        if len(tasks_of_processor) > 0:
            return max(tasks_of_processor, key=lambda x: x.ft)
        return None

    def delete_task(self, task):
        self._graph.remove_node(task)

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

    def set_schedule(self, schedule):
        """
        Set task scheduling across processors.
        :param schedule: Array of indexes that represent index of processor that should be assigned to task.
            Length of list should be (number of tasks - 2) because first and last should not be in list
            (set_schedule() has integrated logic for scheduling first & last task).
        """
        self.clear()

        # Schedule first task
        first_processor_index = self._etc[0].index(min(self._etc[0]))
        first_processor = self._processors[first_processor_index]
        self.get_tasks()[0].processor = first_processor

        # Schedule other tasks
        task_index = 1
        for processor_number in schedule:
            processor_index = processor_number - 1
            self.get_tasks()[task_index].processor = self._processors[processor_index]
            task_index += 1

        self.calculate()

    def get_n_processors(self):
        """
        Returns number of processor
        """
        return len(self._etc[0])

    def _get_entry_task(self):
        """
        Returns entry task. It is used simplified DAG which has only one entry task.
        """
        return list(filter(lambda x: len(self._graph.predecessors(x)) == 0 and x.duplicated is False, self.get_tasks()))[0]

    def _get_exit_task(self):
        """
        Returns exit task. It is used simplified DAG which has only one exit task.
        """
        return list(filter(lambda x: len(self._graph.successors(x)) == 0, self.get_tasks()))[0]

    def _get_c(self, predecessor, successor):
        """
        Returns communication cost between two tasks (edge weight)
        """
        if predecessor.processor == successor.processor:
            return 0

        for task in self.get_tasks_of_processor(successor.processor):
            if task.index == predecessor.index:
                return 0

        return self._graph.get_edge_data(predecessor, successor)['weight']

    def _get_etc(self, task):
        """
        Returns ETC value (Expected Time to Complete) for given task
        """
        return self._etc[task.index][task.processor.index]

    def _get_ava(self, processor):
        """
        Execution completion time of last task allocated to the processor
        """
        last_task = self._get_last_task(processor)
        if last_task is not None:
            return last_task.ft
        return 0

    def _get_st(self, task, use_cached=True):
        """
        Calculates execution start time of task v_i on processor p_k (st(v_i, p_k))
        (2) st(v_i, p_k) = max{ ava(p_k), max(ft(v_j, p_x) + C(e_ji)) }
        """
        if task.processed is True and use_cached is True:
            return task.st

        ava = self._get_ava(task.processor)
        predecessors = self._graph.predecessors(task)

        if len(predecessors) == 0:
            return ava

        # Ignore same tasks with high communication cost (tasks on different processor)
        # If predecessor has a copy and one of the copies is on same processor delete all other copies
        for predecessor in predecessors:
            same_tasks = list(filter(lambda x: x.index == predecessor.index, predecessors))
            if len(same_tasks) > 1:
                same_tasks_diff_process = list(filter(lambda x: x.processor != task.processor, same_tasks))
                if len(same_tasks) - len(same_tasks_diff_process) > 0:
                    predecessors = [x for x in predecessors if x not in same_tasks_diff_process]
                else:
                    min_c_predecessor = min(same_tasks_diff_process, key=lambda x: self._get_c(x, task))
                    predecessors = [x for x in predecessors if x not in same_tasks_diff_process or x == min_c_predecessor]

        ft_plus_c_max = max(map(lambda x: self._get_ft(x) + self._get_c(x, task), predecessors))

        return max([ava, ft_plus_c_max])

    def _get_ft(self, task, use_cached=True):
        """
        Calculates execution finish time
        (3) ft(v_i, p_k) = st(v_i, p_k) + ETC(k, i)
        """
        if task.processed is True and use_cached is True:
            return task.ft

        start_time = self._get_st(task)
        finish_time = start_time + self._get_etc(task)

        return finish_time

    def _schedule_exit_task(self):
        """
        Calculates total time
        (4) totalTime = min{ ft(v_exit, p_j) }
        """
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

    def get_total_time(self):
        return self._get_exit_task().ft

    def _get_vm_cost(self, processor):
        """
        Calculates the monetary cost of p_i pre unit time
        (5) VM_cost(i) = VM_base * exp^R_base
        """
        return self._vm_base * exp(processor.capacity)

    def _get_cost(self, task):
        """
        Calculates the monetary cost for executing task v_j on processor p_i
        (6) cost(i, j) = VM_cost(i) * ETC(i, j)
        """
        return self._get_vm_cost(task.processor) * self._get_etc(task)

    def get_total_cost(self):
        """
        Calculates total cost
        (7) totalCost = sum(cost(i, j))
        """
        total_cost = 0
        for task in self.get_tasks():
            total_cost += self._get_cost(task)

        return total_cost

    def calculate(self):
        self.clear()

        if self._task_duplicator is not None:
            self._calculate_st_ft(duplication_enabled=False)

            time = self.get_total_time()
            cost = self.get_total_cost()

            while True:
                duplicated_task = self._calculate_st_ft(duplication_enabled=True)

                if duplicated_task is None:
                    break

                time_duplicated = self.get_total_time()
                cost_duplicated = self.get_total_cost()

                if self._task_duplicator.task_duplication_condition(time=time, time_duplicated=time_duplicated,
                                                                    cost=cost, cost_duplicated=cost_duplicated):
                    # Scheduling is better with duplicated task -> Keep it
                    time = time_duplicated
                    cost = cost_duplicated
                else:
                    # Scheduling is worse with duplicated task -> Throw it
                    self._task_duplicator.blacklist.append(duplicated_task)
                    self._graph.remove_node(duplicated_task)

        self._calculate_st_ft(duplication_enabled=False)

    def _sort_tasks_condition(self, task):
        communication_cost = 0
        number_of_successors = len(self._graph.successors(task))

        for successor in self._graph.successors(task):
            communication_cost += self._graph.get_edge_data(task, successor)['weight']

        return self._alpha * number_of_successors + self._beta * communication_cost

    def _sort_tasks(self, tasks):
        return sorted(tasks, key=self._sort_tasks_condition, reverse=True)

    def clear(self):
        """
        Delete duplicates, st & ft
        """
        if self._task_duplicator is not None:
            self._task_duplicator.blacklist.clear()

        for task in self.get_tasks():
            if task.duplicated is True:
                self._graph.remove_node(task)
            else:
                task.processed = False

    def _calculate_st_ft(self, duplication_enabled=True):
        """
        Calculate start & finish times
        """
        duplicated_task = None

        # Delete previous calculations
        for task in self.get_tasks():
            task.processed = False

        # Calculate start time & finish time for entry task and their's duplicates
        entry_tasks = list(filter(lambda x: len(self._graph.predecessors(x)) == 0, self.get_tasks()))
        for t in entry_tasks:
            t.st = self._get_st(t)
            t.ft = self._get_ft(t)
            t.processed = True

        successors = self._sort_tasks(self._graph.successors(self._get_entry_task()))
        while len(successors) > 1:
            for successor in successors:
                successor.st = self._get_st(successor)
                successor.ft = self._get_ft(successor)
                if duplication_enabled is True and duplicated_task is None:
                    duplicated_task = self._task_duplicator.try_add_duplicated_task_before(self, successor)

                successor.st = self._get_st(successor, False)
                successor.ft = self._get_ft(successor, False)
                successor.processed = True

            # Find all successors level above
            successors_of_successors = []
            for successor in successors:
                for successors_of_successor in self._graph.successors(successor):
                    if successors_of_successor not in successors_of_successors:
                        successors_of_successors.append(successors_of_successor)
            successors = self._sort_tasks(successors_of_successors)

        self._schedule_exit_task()

        return duplicated_task

    def draw_graph(self):
        """
        Visualise the graph.
        """
        nx.draw_networkx(self._graph, with_labels=True)
        plt.show()

    def draw_schedule(self):
        """
        Visualise scheduled tasks
        """
        fig = plt.figure()
        ax = fig.add_subplot(111)

        for task in self.get_tasks():
            processor_index = task.processor.index
            left_offset = processor_index * 1.0
            face_color = "#ff0000" if task.duplicated is True else "#0000ff"

            rectangle = patches.Rectangle((left_offset, task.st),  0.9,  task.ft - task.st,
                                          alpha=0.4, edgecolor="#000000", facecolor=face_color)
            ax.add_patch(rectangle)

            # Print task name
            rx, ry = rectangle.get_xy()
            cx = rx + rectangle.get_width() / 2.0
            cy = ry + rectangle.get_height() / 2.0
            ax.annotate('v' + str(task.index + 1), (cx, cy), ha='center', va='center')

        if self._task_duplicator is not None:
            for task in self._task_duplicator.blacklist:
                processor_index = task.processor.index
                left_offset = processor_index * 1.0

                rectangle = patches.Rectangle((left_offset, task.st), 0.9, task.ft - task.st,
                                              alpha=0.05, edgecolor="#000000", facecolor="#000000")
                ax.add_patch(rectangle)

                # Print task name
                rx, ry = rectangle.get_xy()
                cx = rx + rectangle.get_width() / 2.0
                cy = ry + rectangle.get_height() / 2.0
                ax.annotate('v' + str(task.index + 1), (cx, cy), ha='center', va='center', color="#aaaaaa")

        ax.autoscale_view(True, True, True)
        plt.show()

    def print_schedule(self):
        """
        Print scheduled tasks
        """
        for processor in self._processors:
            tasks_str = ''
            for task in filter(lambda x: x.processor == processor, self.get_tasks()):
                tasks_str += 'v' + str(task.index + 1) + ' (' + str(task.st) + ' - ' + str(task.ft) + '), '
            print('Processor #' + str(self._processors.index(processor) + 1) + ': ' + tasks_str)
