from importers.PredefinedImporter import PredefinedImporter
from schedulers.ga.GAScheduler import GAScheduler
from schedulers.TaskDuplicator import TaskDuplicator


class GASchedulerTestUseCase(object):
    @staticmethod
    def run():
        print("Running: " + GASchedulerTestUseCase.__name__)
        print("-----------------------------------------")

        task_graph = PredefinedImporter.get_task_graph()
        task_graph.set_task_duplicator(task_duplicator=TaskDuplicator(w=0.2))
        ga_scheduler = GAScheduler(task_graph=task_graph, nind=150, max_terminate=150, no_change_terminate=20, w=1)

        individual = ga_scheduler.calculate()

        task_graph.draw_schedule()

        print('Total cost:', individual.total_cost)
        print('Total time:', individual.total_time)

