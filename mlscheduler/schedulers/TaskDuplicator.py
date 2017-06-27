class Slot(object):
    def __init__(self, st, ft):
        self.st = st
        self.ft = ft

    def __str__(self):
        return 'Slot(' + str(self.st) + ', ' + str(self.ft) + ')'


class TaskDuplicator(object):
    """
    If processor p_k is ready to execute task v_i before the arrival of the execution results from its predecessor,
    there will be idle-time on the processor which can be recorded as slot(v_i, p_k) [4].
    """

    @staticmethod
    def get_slot_before(task_graph, task):
        ft_max = 0

        for task_i in task_graph.get_tasks_of_processor(task.processor):
            if task_i.ft <= task.st and task_i.ft >= ft_max:
                ft_max = task_i.ft

        if ft_max != task.st:
            return Slot(st=ft_max, ft=task.st)
        return None

    @staticmethod
    def apply(task_graph):
        for task in task_graph._tasks:
            slot = TaskDuplicator.get_slot_before(task_graph, task)

            predecessors = task_graph._graph.predecessors(task)
            for predecessor in predecessors:

                # print(task.processor.index, slot, task_graph._etc[predecessor.index][task.processor.index])
                if slot is not None and task_graph._etc[predecessor.index][task.processor.index] <= (slot.ft - slot.st):
                    print(task.processor.index, slot)


