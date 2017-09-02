from importers.PredefinedImporter import PredefinedImporter
from schedulers.ga.GAScheduler import GAScheduler
from schedulers.TaskDuplicator import TaskDuplicator


class GASchedulerTestUseCase(object):
    @staticmethod
    def run():
        print("Running: " + GASchedulerTestUseCase.__name__)
        print("-----------------------------------------")

        w = 0.99

        task_graph = PredefinedImporter.get_task_graph()
        task_graph.set_task_duplicator(task_duplicator=TaskDuplicator(w=w))
        ga_scheduler = GAScheduler(task_graph=task_graph, nind=150, max_terminate=150, no_change_terminate=20, w=w)

        best_graph = ga_scheduler.calculate()

        print('Total Time:', task_graph.get_total_time())
        print('Total Cost:', task_graph.get_total_cost())

        task_graph.print_schedule()
        best_graph.draw_schedule()


