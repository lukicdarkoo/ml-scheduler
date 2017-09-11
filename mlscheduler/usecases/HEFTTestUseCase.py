from importers.PredefinedImporter import PredefinedImporter
from importers.RandomImporter import RandomImporter
from schedulers.ga.GAScheduler import GAScheduler
from schedulers.TaskDuplicator import TaskDuplicator
from schedulers.HEFTScheduler import HEFTScheduler
import matplotlib.pyplot as plt


class HEFTTestUseCase(object):
    @staticmethod
    def run():
        print("Running: " + HEFTTestUseCase.__name__)
        print("-----------------------------------------")

        task_graph = PredefinedImporter.get_task_graph()
        heft_scheduler = HEFTScheduler(task_graph=task_graph.copy())

        heft_graph = heft_scheduler.calculate()

        print('Total Time:', heft_graph.get_total_time())
        print('Total Cost:', heft_graph.get_total_cost())

        heft_graph.print_schedule()
        heft_graph.draw_schedule()



