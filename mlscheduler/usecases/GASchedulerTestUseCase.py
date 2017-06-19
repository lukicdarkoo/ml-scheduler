from importers.PredefinedImporter import PredefinedImporter
from schedulers.GAScheduler import GAScheduler


class GASchedulerTestUseCase(object):
    @staticmethod
    def run():
        print("Running: " + GASchedulerTestUseCase.__name__)
        print("-----------------------------------------")

        task_graph = PredefinedImporter.get_task_graph()
        ga_scheduler = GAScheduler(task_graph=task_graph)

        ga_scheduler.calculate()

