from importers.PredefinedImporter import PredefinedImporter
from schedulers.GAScheduler import GAScheduler


class GASchedulerTestUseCase(object):
    @staticmethod
    def run():
        print("Running: " + GASchedulerTestUseCase.__name__)
        print("-----------------------------------------")

        task_graph = PredefinedImporter.get_task_graph()
        ga_scheduler = GAScheduler(task_graph=task_graph, nind=50, max_terminate=150, no_change_terminate=10)

        individual = ga_scheduler.calculate()
        print('Total cost:', individual.total_cost)
        print('Total time:', individual.total_time)

