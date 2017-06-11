import networkx as nx
import matplotlib.pyplot as plt


class GraphDrawer(object):
    @staticmethod
    def draw(g):
        nx.draw_networkx(g, with_labels=True)
        plt.show()
