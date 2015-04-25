__author__ = 'giorgos'

import os

class Graph:

    def __init__(self, num_vertex):
        self._num_vertex = num_vertex
        self._num_edges = 0
        self._vertices = [[] for v in range(num_vertex)]

    def add_edge(self, v, w):
        assert v < self._num_vertex
        assert w < self._num_vertex
        self._vertices[v].append(w)
        self._vertices[w].append(v)
        self._num_edges += 1

    def V(self): return self._num_vertex

    def E(self): return self._num_edges

    def edges(self, v):
        assert v < self._num_vertex
        return self._vertices[v]

    def __str__(self):
        s = str(self._num_vertex)
        s2 = str(self._num_edges)
        vs = [str(v) + ' ' + str(w) for v in range(len(self._vertices)) for w in self._vertices[v]]
        return os.linesep.join([s, s2] + vs)

class WeightedGraph(Graph):
    def __init__(self, num_vertex):
        Graph.__init__(self, num_vertex)

    def add_weighted_edge(self, u, v, w):
        assert u < self._num_vertex
        assert v < self._num_vertex
        self._vertices[u].append((v, w))
        self._vertices[v].append((u, w))
        self._num_edges += 2

    def add_edge(self, u, w):
        raise Exception("weight is mandatory")

    def __str__(self):
        s = str(self._num_vertex)
        vs = [str(u) + ' ' + str(v) + ' ' + str(w) for u in range(len(self._vertices)) for (v, w) in self._vertices[u]]
        return os.linesep.join([s] + vs)


class Digraph(Graph):
    def __init__(self, num_vertex):
        Graph.__init__(self, num_vertex)

    def add_edge(self, v, w):
        assert v < self._num_vertex
        assert w < self._num_vertex
        self._vertices[v].append(w)
        self._num_edges += 1

    def reverse(self):
        rg = Digraph(self._num_vertex)
        for v in range(len(self._vertices)):
            for e in self._vertices[v]:
                rg.add_edge(e, v)
        return rg

class WeightedDigraph(Graph):

    def __init__(self, num_vertex):
        Graph.__init__(self, num_vertex)

    def add_edge(self, u, w):
        raise Exception("weight is mandatory")

    def add_weighted_edge(self, u, v, w):
        assert u < self._num_vertex
        assert v < self._num_vertex
        self._vertices[u].append((v, w))
        self._num_edges += 1

    def reverse(self):
        rg = Digraph(self._num_vertex)
        for v in range(len(self._vertices)):
            for e in self._vertices[v]:
                rg.add_weighted_edge(e, v)
        return rg

    def edge_list(self):
        for v in range(self.V()):
            edges = self.edges(v)
            for e in edges:
                (u, w) = e
                yield v, u, w


    def __str__(self):
        s = str(self._num_vertex)
        vs = [str(u) + '-(' + str(w) + ')->' + str(v) for u in range(len(self._vertices)) for (v, w) in self._vertices[u]]
        return os.linesep.join([s] + vs)

def load_graph(path, directed=False, zero_based=True):
    f = open(path, "r")
    num_vertex = int(f.readline())
    g = Graph(num_vertex) if not directed else Digraph(num_vertex)
    for ln in f.readlines():
        v, w = [int(x) for x in ln.strip().split()]
        if not zero_based:
            v -= 1
            w -= 1
        g.add_edge(v, w)
    return g

def load_weighted_graph(path, zero_based=True):
    with open(path, "r") as f:
        num_vertex = int(f.readline())
        g = WeightedGraph(num_vertex)
        for ln in f.readlines():
            (u, v, w) = ln.split()
            u = int(u)
            v = int(v)
            if not zero_based:
                u -= 1
                v -= 1
            w = float(w)

            g.add_weighted_edge(u, v, w)
    return g

def load_digraph(path, zero_based=True):
    return load_graph(path, True, zero_based)


def load_weighted_digraph(path, zero_based=False):
    f = open(path, "r")
    num_vertex = int(f.readline().split()[0])
    g = WeightedDigraph(num_vertex)
    for ln in f.readlines():
        (u, v, w) = ln.split()
        u = int(u)
        if not zero_based:
            u -= 1

        v = int(v)
        w = float(w)

        # data specifies vertices with 1-based indices
        if not zero_based:
            v -= 1
        g.add_weighted_edge(u, v, w)
    return g

if __name__ == "__main__":
    g = load_graph("../data/tinyG.txt")
    print(g)

    g = load_digraph("../data/tinySCC.txt")
    print(g)

    g = load_digraph("../data/tinySCC.txt")
    print(g.reverse())

    g = WeightedDigraph(3)
    g.add_weighted_edge(0, 1, 1.0)
    g.add_weighted_edge(0, 2, 1.3)
    g.add_weighted_edge(1, 2, 4.0)
    g.add_weighted_edge(2, 1, 1.0)
    g.add_weighted_edge(2, 0, -1.0)

    for e in g.edge_list():
        print e

