__author__ = 'giorgos'

"""
Determines if a graph contains a cycle. The graph is expected to be
in adjacency list representation.

Uses depth first search to explore the graph, if a vertex is visited
twice then a cycle exists.

Runs in O(n + m) time where n is the number of vertices and m is the
number of edges.
"""

class DirectedCycleDetector:
    def __init__(self, g):
        self._G = g
        self._marked = [False for i in range(g.V())]
        self._cycle = []

        # whenever a vertex is visited it enters this list and it pops off when we have
        # a DFS for that vertex
        self._call_stack = [None for i in range(g.V())]

        # _parentChain[v] = w means that we reached v through w
        self._parentChain = [None for i in range(g.V())]

    def has_cycle(self):
        for v in range(self._G.V()):
            if not self._marked[v]:
                self.dfs(v)

            if self.__has_cycle():
                break

        return self.__has_cycle()

    def dfs(self, v):
        self._call_stack[v] = True
        self._marked[v] = True
        for w in self._G.edges(v):
            if self.__has_cycle():
                return

            # support for weighted digraphs
            if type(w) is list or type(w) is tuple:
                w = w[0]

            if not self._marked[w]:
                self._parentChain[w] = v
                self.dfs(v, w)
            elif self._call_stack[w]:
                # just found a cycle, store the cyclic path
                self._cycle = []
                p = v
                while True:
                    self._cycle.insert(0, p)
                    p = self._parentChain[p]
                    if p is None or p == w: break

                self._cycle.insert(0, w)
                self._cycle.insert(0, v)

        self._call_stack[v] = False

    def cycle(self):
        return self._cycle

    def __has_cycle(self):
        return len(self._cycle) > 0


class CycleDetector:
    def __init__(self, g):
        self._G = g
        self._marked = [False for i in range(g.V())]
        self._cycle = []
        # _parentChain[v] = w means that we reached v through w
        self._parentChain = [None for i in range(g.V())]

    def has_cycle(self):
        for v in range(self._G.V()):
            if not self._marked[v]:
                self.dfs(-1, v)

            if self.__has_cycle():
                break

        return self.__has_cycle()

    def dfs(self, u, v):
        self._marked[v] = True
        for w in self._G.edges(v):

            if self.__has_cycle():
                return

            if not self._marked[w]:
                self._parentChain[w] = v
                self.dfs(v, w)
            elif w != u:
                # just found a cycle, store the cyclic path
                self._cycle = []
                p = v
                while True:
                    self._cycle.insert(0, p)
                    p = self._parentChain[p]
                    if p is None or p == w: break

                self._cycle.insert(0, w)
                self._cycle.insert(0, v)

    def cycle(self):
        return self._cycle

    def __has_cycle(self):
        return len(self._cycle) > 0

if __name__ == "__main__":
    import graph_utils
    G = graph_utils.load_graph("../data/cyclicG.txt")
    detector = CycleDetector(G)
    assert detector.has_cycle()
    assert [3, 0, 1, 2, 3] == detector.cycle()

    G = graph_utils.load_graph("../data/tinyG.txt")
    detector = CycleDetector(G)
    assert detector.has_cycle()
    print(detector.cycle())
