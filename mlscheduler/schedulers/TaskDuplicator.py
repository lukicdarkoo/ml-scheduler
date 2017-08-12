from copy import deepcopy


class Slot(object):
    def __init__(self, st, ft):
        self.st = st
        self.ft = ft

    def __str__(self):
        return 'Slot(' + str(self.st) + ', ' + str(self.ft) + ')'


class TaskDuplicator(object):
    def __init__(self, w):
        self._w = w

    """
    If processor p_k is ready to execute task v_i before the arrival of the execution results from its predecessor,
    there will be idle-time on the processor which can be recorded as slot(v_i, p_k) [4].
    """
    def _get_slot_before(self, task_graph, task):
        ft_max = 0

        for task_i in task_graph.get_tasks_of_processor(task.processor):
            if task_i.ft <= task.st and task_i.ft >= ft_max:
                ft_max = task_i.ft

        if ft_max != task.st:
            return Slot(st=ft_max, ft=task.st)
        return None

    """
    Calculates if task should be duplicated
    (15) - (delta(cost) / delta(time)) < k * Maxprice
    """
    def task_duplication_condition(self, cost, cost_duplicated, time, time_duplicated):
        max_price = max([cost, cost_duplicated])
        k = pow(self._w / (1 - self._w), 2)

        if abs(time_duplicated - time) is 0:
            return True

        return (abs(cost_duplicated - cost) / abs(time_duplicated - time)) > (k * max_price)

    def try_add_duplicated_task_before(self, task_graph, task):
        slot = self._get_slot_before(task_graph, task)

        predecessors = task_graph._graph.predecessors(task)
        for predecessor in predecessors:
            # print(task.processor.index, slot, task_graph._etc[predecessor.index][task.processor.index])
            if slot is not None and task_graph.get_etc(predecessor, task.processor) <= (slot.ft - slot.st):
                duplicated_task = deepcopy(predecessor)
                duplicated_task.st = slot.st
                duplicated_task.ft = slot.st + task_graph.get_etc(predecessor, task.processor)
                duplicated_task.processor = task.processor

                task_graph.insert_duplicated_task(predecessor, duplicated_task)
                return duplicated_task

        return None
