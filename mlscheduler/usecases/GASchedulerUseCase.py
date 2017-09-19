from importers.PredefinedImporter import PredefinedImporter
from importers.RandomImporter import RandomImporter
from schedulers.ga.GAScheduler import GAScheduler
from schedulers.TaskDuplicator import TaskDuplicator
from schedulers.HEFTScheduler import HEFTScheduler
import matplotlib.pyplot as plt


class GASchedulerUseCase(object):
    @staticmethod
    def run():
        print("Running: " + GASchedulerUseCase.__name__)
        print("-----------------------------------------")
        w = 0.5

        ga2_times = []
        ga_times = []
        ga2_costs = []
        ga_costs = []
        number_of_tasks = []
        for i in range(8, 30, 4):
            task_graph = RandomImporter.get_task_graph(n_tasks=i)

            task_graph.set_task_duplicator(task_duplicator=TaskDuplicator(w=w))
            ga_scheduler = GAScheduler(task_graph=task_graph.copy(), nind=20, max_terminate=20, no_change_terminate=5, n_populations=1, w=w)
            ga_scheduler2 = GAScheduler(task_graph=task_graph.copy(), nind=20, max_terminate=20, no_change_terminate=5, n_populations=5, w=w)

            ga2_graph = ga_scheduler2.calculate()
            ga_graph = ga_scheduler.calculate()

            number_of_tasks.append(i)
            ga2_times.append(ga2_graph.get_total_time())
            ga_times.append(ga_graph.get_total_time())
            ga2_costs.append(ga2_graph.get_total_cost())
            ga_costs.append(ga_graph.get_total_cost())

        plt.plot(number_of_tasks, ga2_times, 'r')
        plt.plot(number_of_tasks, ga_times, 'b')
        plt.ylabel('Time')
        plt.xlabel('Number of tasks')
        plt.show()

        plt.plot(number_of_tasks, ga2_costs, 'r')
        plt.plot(number_of_tasks, ga_costs, 'b')
        plt.ylabel('Cost')
        plt.xlabel('Number of tasks')
        plt.show()



