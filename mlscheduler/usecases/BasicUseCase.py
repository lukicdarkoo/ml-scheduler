from mlscheduler.importers.RandomImporter import RandomImporter
from mlscheduler.importers.PredefinedImporter import PredefinedImporter


class BasicUseCase(object):
    @staticmethod
    def run():
        print("Running Basic use case")
        task_graph = PredefinedImporter.get_task_graph()
        task_graph.set_schedule([1, 2, 3, 2, 3, 1, 3, 1])


        # task_graph.draw()
        # ft = task_graph.get_ft(task_graph._tasks[9])
        total_time = task_graph.get_total_time()
        total_cost = task_graph.get_total_cost()
        print('Total Time:', total_time)
        print('Total Cost:', total_cost)

