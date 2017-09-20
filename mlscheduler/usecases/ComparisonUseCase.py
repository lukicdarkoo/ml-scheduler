from importers.PredefinedImporter import PredefinedImporter
from importers.RandomImporter import RandomImporter
from schedulers.ga.GAScheduler import GAScheduler
from schedulers.TaskDuplicator import TaskDuplicator
from schedulers.HEFTScheduler import HEFTScheduler
import matplotlib.pyplot as plt
import datetime


class ComparisonUseCase(object):
    @staticmethod
    def time_diff(start, end):
        diff = end - start
        millis = diff.days * 24 * 60 * 60 * 1000
        millis += diff.seconds * 1000
        millis += diff.microseconds / 1000
        return millis

    @staticmethod
    def run():
        print("Running: " + ComparisonUseCase.__name__)
        print("-----------------------------------------")
        w = 0.5

        heft_times = []
        ga_times = []
        heft_executions = []
        ga_executions = []
        heft_costs = []
        ga_costs = []
        number_of_tasks = []
        for i in range(8, 30, 4):
            task_graph = RandomImporter.get_task_graph(n_tasks=i)
            task_graph.set_task_duplicator(task_duplicator=TaskDuplicator(w=w))
            ga_scheduler = GAScheduler(task_graph=task_graph.copy(), nind=20, max_terminate=20, no_change_terminate=5, w=w)
            heft_scheduler = HEFTScheduler(task_graph=task_graph.copy())

            heft_start = datetime.datetime.now()
            heft_graph = heft_scheduler.calculate()
            heft_end = datetime.datetime.now()

            ga_start = datetime.datetime.now()
            ga_graph = ga_scheduler.calculate()
            ga_end = datetime.datetime.now()

            number_of_tasks.append(i)
            heft_times.append(heft_graph.get_total_time())
            ga_times.append(ga_graph.get_total_time())
            heft_costs.append(heft_graph.get_total_cost())
            ga_costs.append(ga_graph.get_total_cost())
            heft_executions.append(ComparisonUseCase.time_diff(heft_start, heft_end))
            ga_executions.append(ComparisonUseCase.time_diff(ga_start, ga_end))

        plt.plot(number_of_tasks, heft_executions, 'r')
        plt.plot(number_of_tasks, ga_executions, 'b')
        plt.ylabel('Execution Time')
        plt.xlabel('Number of tasks')
        plt.show()

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



