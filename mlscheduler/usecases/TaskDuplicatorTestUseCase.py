from importers.RandomImporter import RandomImporter
from importers.PredefinedImporter import PredefinedImporter
from schedulers.TaskDuplicator import TaskDuplicator


class TaskDuplicatorTestUseCase(object):
    @staticmethod
    def run():
        print("Running: " + TaskDuplicatorTestUseCase.__name__)
        print("-----------------------------------------")

        chromosome = [1, 2, 3, 3, 1, 2, 1, 2]
        task_graph = PredefinedImporter.get_task_graph()
        task_graph.set_task_duplicator(task_duplicator=TaskDuplicator(w=0.2))
        task_graph.set_schedule(chromosome)

        print('Chromosome:', chromosome)
        print('Total Time:', task_graph.get_total_time())
        print('Total Cost:', task_graph.get_total_cost())

        task_graph.print_schedule()
        task_graph.draw_schedule()

