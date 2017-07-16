from copy import deepcopy


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
    def try_add_duplicated_task_before(task_graph, task):
        slot = TaskDuplicator.get_slot_before(task_graph, task)

        predecessors = task_graph._graph.predecessors(task)
        for predecessor in predecessors:
            # print(task.processor.index, slot, task_graph._etc[predecessor.index][task.processor.index])
            if slot is not None and task_graph.get_etc(predecessor, task.processor) <= (slot.ft - slot.st):
                duplicated_task = deepcopy(predecessor)
                duplicated_task.st = slot.st
                duplicated_task.ft = slot.st + task_graph.get_etc(predecessor, task.processor)
                duplicated_task.processor = task.processor

                task_graph.insert_duplicated_task(predecessor, duplicated_task)
                break

    @staticmethod
    def apply(task_graph):
        successors = task_graph._graph.successors(task_graph._get_entry_task())

        while len(successors) > 1:
            # Process successors
            for successor in successors:
                slot = TaskDuplicator.get_slot_before(task_graph, successor)
                predecessors = task_graph._graph.predecessors(successor)
                for predecessor in predecessors:
                    # print(task.processor.index, slot, task_graph._etc[predecessor.index][task.processor.index])
                    if slot is not None and task_graph.get_etc(predecessor, successor.processor) <= (slot.ft - slot.st):
                        duplicated_task = deepcopy(predecessor)
                        duplicated_task.st = slot.st
                        duplicated_task.ft = slot.st + task_graph.get_etc(predecessor, successor.processor)
                        duplicated_task.processor = successor.processor
                        duplicated_task.duplicated = True
                        duplicated_task.processed = True

                        task_graph.insert_duplicated_task(predecessor, duplicated_task)

                        # print(successor.processor.index, slot)
                        print(duplicated_task, duplicated_task.processor, duplicated_task.st, duplicated_task.ft,
                              duplicated_task.processed)
                        break

            # Find all successors level above
            successors_of_successors = []
            for successor in successors:
                for successors_of_successor in task_graph._graph.successors(successor):
                    if successors_of_successor not in successors_of_successors:
                        successors_of_successors.append(successors_of_successor)
            successors = successors_of_successors

            task_graph.clear()
            task_graph.calculate_st_ft()

    @staticmethod
    def apply2(task_graph):
        entry_task = task_graph._get_entry_task()

        for task in task_graph.get_tasks():
            slot = TaskDuplicator.get_slot_before(task_graph, task)

            predecessors = task_graph._graph.predecessors(task)
            for predecessor in predecessors:

                # print(task.processor.index, slot, task_graph._etc[predecessor.index][task.processor.index])
                if slot is not None and task_graph.get_etc(predecessor, task.processor) <= (slot.ft - slot.st):
                    duplicated_task = deepcopy(predecessor)
                    duplicated_task.st = slot.st
                    duplicated_task.ft = slot.st + task_graph.get_etc(predecessor, task.processor)
                    duplicated_task.processor = task.processor

                    task_graph.insert_duplicated_task(predecessor, duplicated_task)

                    print(task.processor.index, slot)
                    print(duplicated_task, duplicated_task.processor, duplicated_task.st, duplicated_task.ft, duplicated_task.processed)
                    break

                task_graph.clear()
                task_graph.calculate_st_ft()



