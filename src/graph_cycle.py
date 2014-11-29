__author__ = 'giorgos'

"""
Determines if a graph contains a cycle. The graph is expected to be
in adjacency list representation.

Uses depth first search to explore the graph, if a vertex is visited
twice then a cycle exists.

Runs in O(n + m) time where n is the number of vertices and m is the
number of edges.
"""

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
                self._cycle = [v, w]
                p = self._parentChain[v]
                while p is not None and p != w:
                    self._cycle.insert(0, p)
                    p = self._parentChain[p]
                self._cycle.insert(0, w)

    def cycle(self):
        return self._cycle

    def __has_cycle(self):
        return len(self._cycle) > 0

if __name__ == "__main__":
    import graph_utils
    G = graph_utils.load_graph("cyclicG.txt")
    detector = CycleDetector(G)
    assert detector.has_cycle()
    assert [0, 1, 2, 3, 0] == detector.cycle()

    G = graph_utils.load_graph("tinyG.txt")
    detector = CycleDetector(G)
    assert detector.has_cycle()
    print(detector.cycle())
