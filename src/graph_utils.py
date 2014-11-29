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

def load_digraph(path, zero_based=True):
    return load_graph(path, True, zero_based)


def load_weighted_digraph(path):
    f = open(path, "r")
    num_vertex = int(f.readline())
    g = WeightedDigraph(num_vertex)
    for ln in f.readlines():
        fields = ln.split()
        u = int(fields[0]) - 1
        for x in fields[1:]:
            (v, w) = x.split(",")
            (v, w) = (int(v), int(w))
            # data specifies vertices with 1-based indices
            v -= 1
            g.add_weighted_edge(u, v, w)
    return g

if __name__ == "__main__":
    g = load_graph("tinyG.txt")
    print(g)

    g = load_digraph("tinySCC.txt")
    print(g)

    g = load_digraph("tinySCC.txt")
    print(g.reverse())

