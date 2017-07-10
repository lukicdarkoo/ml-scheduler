from importers.RandomImporter import RandomImporter
from importers.PredefinedImporter import PredefinedImporter
from schedulers.TaskDuplicator import TaskDuplicator


class TaskDuplicatorTestUseCase(object):
    @staticmethod
    def set_schedule(task_graph, schedule):
        task_graph.clear()

        # Schedule other tasks
        task_index = 0
        for processor_number in schedule:
            processor_index = processor_number - 1
            task_graph.get_tasks()[task_index].processor = task_graph._processors[processor_index]
            task_index += 1

        task_graph.calculate_st_ft()

    @staticmethod
    def run():
        print("Running: " + TaskDuplicatorTestUseCase.__name__)
        print("-----------------------------------------")

        chromosome = [3, 1, 2, 3, 3, 3, 2, 1, 2]
        task_graph = PredefinedImporter.get_task_graph()
        TaskDuplicatorTestUseCase.set_schedule(task_graph, chromosome)

        total_time = task_graph.get_total_time()
        total_cost = task_graph.get_total_cost()
        print('Chromosome:', chromosome)
        print('Total Time:', total_time)
        print('Total Cost:', total_cost)

        task_graph.print_schedule()
        task_graph.draw_schedule()

        # Apply Task Duplicator
        TaskDuplicator.apply(task_graph)
        task_graph.draw_schedule()
