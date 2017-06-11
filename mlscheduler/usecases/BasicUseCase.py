from mlscheduler.misc.GraphDrawer import GraphDrawer
from mlscheduler.importers.RandomImporter import RandomImporter


class BasicUseCase(object):
    @staticmethod
    def run():
        print("Running Basic use case")
        graph = RandomImporter.get_graph()
        GraphDrawer.draw(graph)
