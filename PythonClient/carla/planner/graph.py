import math
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import collections as mc


def string_to_node(string):
    vec = string.split(',')
    return (int(vec[0]), int(vec[1]))


def string_to_floats(string):
    vec = string.split(',')
    return (float(vec[0]), float(vec[1]), float(vec[2]))


def sldist(c1, c2):
    return math.sqrt((c2[0] - c1[0])**2 + (c2[1] - c1[1])**2)


def sldist3(c1, c2):
    return math.sqrt((c2[0] - c1[0])**2 + (c2[1] - c1[1])
                     ** 2 + (c2[2] - c1[2])**2)


class Graph(object):
    """
    A simple directed, weighted graph
    """

    def __init__(self, graph_file=None):

        self._nodes = set()
        self._angles = {}
        self._edges = {}
        self._distances = {}
        self._node_density = 50
        if graph_file is not None:
            with open(graph_file, 'r') as file:
                # Skipe the first four lines that
                lines_after_4 = file.readlines()[4:]

                # the graph resolution.
                linegraphres = lines_after_4[0]
                self._resolution = string_to_node(linegraphres)
                for line in lines_after_4[1:]:

                    from_node, to_node, d = line.split()
                    from_node = string_to_node(from_node)
                    to_node = string_to_node(to_node)

                    if from_node not in self._nodes:
                        self.add_node(from_node)
                    if to_node not in self._nodes:
                        self.add_node(to_node)

                    self._edges.setdefault(from_node, [])
                    self._edges[from_node].append(to_node)
                    self._distances[(from_node, to_node)] = float(d)

    def add_node(self, value):
        self._nodes.add(value)

    def project_pixel(self, pixel):
        node = []
        node.append((pixel[0]) / self._node_density - 2)
        node.append((pixel[1]) / self._node_density - 2)

        return tuple(node)

    def make_orientations(self, node, heading):

        import collections
        distance_dic = {}
        for node_iter in self._nodes:
            if node_iter != node:
                distance_dic[sldist(node, node_iter)] = node_iter

        distance_dic = collections.OrderedDict(
            sorted(distance_dic.items()))

        self._angles[node] = heading
        for k, v in distance_dic.iteritems():


            start_to_goal = np.array([node[0] - v[0], node[1] - v[1]])

            print(start_to_goal)

            self.angles[v] = start_to_goal / np.linalg.norm(start_to_goal)

    def add_edge(self, from_node, to_node, distance):
        self._add_edge(from_node, to_node, distance)

    def _add_edge(self, from_node, to_node, distance):
        self._edges.setdefault(from_node, [])
        self._edges[from_node].append(to_node)
        self._distances[(from_node, to_node)] = distance

    def intersection_nodes(self):

        intersect_nodes = []
        for node in self._nodes:
            if len(self._edges[node]) > 2:
                intersect_nodes.append(node)

        return intersect_nodes

    # This contains also the non-intersection turns...

    def turn_nodes(self):

        return self._nodes

    def plot_ori(self, c):
        line_len = 1

        lines = [[(p[0], p[1]), (p[0] + line_len * self._angles[p][0],
                                 p[1] + line_len * self._angles[p][1])] for p in self.nodes]
        lc = mc.LineCollection(lines, linewidth=2, color='green')
        fig, ax = plt.subplots()
        ax.add_collection(lc)

        ax.autoscale()
        ax.margins(0.1)

        xs = [p[0] for p in self._nodes]
        ys = [p[1] for p in self._nodes]

        plt.scatter(xs, ys, color=c)

    def plot(self, c):

        xs = [p[0] for p in self._nodes]
        ys = [p[1] for p in self._nodes]

        plt.scatter(xs, ys, color=c)