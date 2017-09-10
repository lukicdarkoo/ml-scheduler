from importers.PredefinedImporter import PredefinedImporter
from importers.RandomImporter import RandomImporter
from schedulers.ga.GAScheduler import GAScheduler
from schedulers.TaskDuplicator import TaskDuplicator
from schedulers.HEFTScheduler import HEFTScheduler
import matplotlib.pyplot as plt


class ComparisonUseCase(object):
    @staticmethod
    def run():
        print("Running: " + ComparisonUseCase.__name__)
        print("-----------------------------------------")
        w = 0.5

        heft_times = []
        ga_times = []
        heft_costs = []
        ga_costs = []
        number_of_tasks = []
        for i in range(8, 30, 4):
            task_graph = RandomImporter.get_task_graph(n_tasks=i)
            task_graph.set_task_duplicator(task_duplicator=TaskDuplicator(w=w))
            ga_scheduler = GAScheduler(task_graph=task_graph.copy(), nind=90, max_terminate=80, no_change_terminate=15, w=w)
            heft_scheduler = HEFTScheduler(task_graph=task_graph.copy())

            heft_graph = heft_scheduler.calculate()
            ga_graph = ga_scheduler.calculate()

            number_of_tasks.append(i)
            heft_times.append(heft_graph.get_total_time())
            ga_times.append(ga_graph.get_total_time())
            heft_costs.append(heft_graph.get_total_cost())
            ga_costs.append(ga_graph.get_total_cost())

        plt.plot(number_of_tasks, heft_times, 'r')
        plt.plot(number_of_tasks, ga_times, 'b')
        plt.ylabel('Time')
        plt.xlabel('Number of tasks')
        plt.show()

        plt.plot(number_of_tasks, heft_costs, 'r')
        plt.plot(number_of_tasks, ga_costs, 'b')
        plt.ylabel('Cost')
        plt.xlabel('Number of tasks')
        plt.show()



