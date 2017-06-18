class Slot(object):
    def __init__(self, processor, st, ft):
        self.processor = processor
        self.st = st
        self.ft = ft


class TaskDuplicator(object):
    """
    If processor p_k is ready to execute task v_i before the arrival of the execution results from its predecessor,
    there will be idle-time on the processor which can be recorded as slot(v_i, p_k) [4].
    """

    @staticmethod
    def _find_slots(task_graph):
        tasks_per_processor = task_graph._tasks_per_processor
        graph = task_graph._graph

        for processor in tasks_per_processor:
            previous_task = processor[0]
            for task in processor:
                pass


