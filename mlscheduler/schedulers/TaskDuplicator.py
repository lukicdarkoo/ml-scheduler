class Slot(object):
    def __init__(self, processor, st, ft):
        self.processor = processor
        self.st = st
        self.ft = ft


class TaskDuplicator(object):
    @staticmethod
    def _find_slots(task_graph):
        tasks_per_processor = task_graph._tasks_per_processor
        for processor in tasks_per_processor:
            for task in processor:
                pass


