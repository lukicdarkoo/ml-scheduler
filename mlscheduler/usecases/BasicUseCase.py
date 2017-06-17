from importers.RandomImporter import RandomImporter
from importers.PredefinedImporter import PredefinedImporter


class BasicUseCase(object):
    @staticmethod
    def run():
        print("Running Basic use case")

        # chromosome = [1, 2, 3, 2, 3, 1, 3, 1]
        chromosome = [1, 2, 3, 3, 3, 2, 1, 2]
        task_graph = PredefinedImporter.get_task_graph()
        task_graph.set_schedule(chromosome)

        # ft = task_graph.get_ft(task_graph._tasks[9])
        total_time = task_graph.get_total_time()
        total_cost = task_graph.get_total_cost()
        print('Chromosome:', chromosome)
        print('Total Time:', total_time)
        print('Total Cost:', total_cost)

        task_graph.print_schedule()
        # task_graph.draw_graph()
        task_graph.draw_schedule()

