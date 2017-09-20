from importers.PredefinedImporter import PredefinedImporter
from importers.RandomImporter import RandomImporter
from schedulers.ga.GAScheduler import GAScheduler
from schedulers.TaskDuplicator import TaskDuplicator
from schedulers.HEFTScheduler import HEFTScheduler
import matplotlib.pyplot as plt
import matplotlib.backends.backend_pdf
import os
import numpy as np


class ParamCollection(object):
    def __init__(self, params):
        self.params = params

    def get(self, name, iter_name, iter_value):
        if name == iter_name:
            return iter_value
        else:
            param = [param for param in self.params if param.name == name][0]
            return param.default


class Param(object):
    def __init__(self, min=0.0, max=50.0, step=4.0, name='w', default=25.0):
        self.min = min
        self.max = max
        self.step = step
        self.name = name
        self.default = default


class GATuningUseCase(object):
    @staticmethod
    def run():
        print("Running: " + GATuningUseCase.__name__)
        print("-----------------------------------------")
        pdf = matplotlib.backends.backend_pdf.PdfPages(os.path.dirname(os.path.abspath(__file__)) + '/../../output.pdf')
        task_graph = RandomImporter.get_task_graph(n_tasks=15)

        pc = ParamCollection([
            Param(min=0.01, max=0.99, step=0.2, name='w', default=0.5),
            Param(min=2, max=50, step=5, name='nind', default=10),
            Param(min=2, max=30, step=5, name='max_terminate', default=15),
            Param(min=2, max=10, step=2, name='no_change_terminate', default=5),
            Param(min=1, max=10, step=2, name='n_populations', default=1),
            Param(min=0.01, max=0.99, step=0.1, name='k1', default=0.6),
            Param(min=0.01, max=0.99, step=0.1, name='k2', default=0.8),
            Param(min=0.01, max=0.99, step=0.1, name='k3', default=0.1),
            Param(min=0.01, max=0.99, step=0.1, name='k4', default=0.05)
        ])

        for param in pc.params:
            changable_param_values = []
            ga_times = []
            ga_costs = []

            for i in np.arange(param.min, param.max, param.step):
                w = pc.get('w', param.name, i)
                nind = pc.get('nind', param.name, i)
                max_terminate = pc.get('max_terminate', param.name, i)
                no_change_terminate = pc.get('no_change_terminate', param.name, i)
                n_populations = pc.get('n_populations', param.name, i)
                k1 = pc.get('k1', param.name, i)
                k2 = pc.get('k2', param.name, i)
                k3 = pc.get('k3', param.name, i)
                k4 = pc.get('k4', param.name, i)

                task_graph.set_task_duplicator(task_duplicator=TaskDuplicator(w=w))
                ga_scheduler = GAScheduler(task_graph=task_graph.copy(),
                                           nind=nind,
                                           max_terminate=max_terminate,
                                           no_change_terminate=no_change_terminate,
                                           n_populations=n_populations,
                                           w=w,
                                           k1=k1,
                                           k2=k2,
                                           k3=k3,
                                           k4=k4)

                ga_graph = ga_scheduler.calculate()

                changable_param_values.append(i)
                ga_times.append(ga_graph.get_total_time())
                ga_costs.append(ga_graph.get_total_cost())

            plt.clf()
            plt.plot(changable_param_values, ga_times, 'b')
            plt.ylabel('Time')
            plt.xlabel(param.name)
            pdf.savefig(1)

            plt.clf()
            plt.plot(changable_param_values, ga_costs, 'r')
            plt.ylabel('Cost')
            plt.xlabel(param.name)
            pdf.savefig(1)

        pdf.close()


