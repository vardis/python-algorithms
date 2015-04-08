"""
Kruskal's algorithm for calculating the minimum spanning tree of a graph.

This is a greedy algorithm which aims at each step to integrate the next minimum
remaining edge of the graph into the mst. If including the considered edge does not
create a cycle then the edge is indeed included in the mst, otherwise it is rejected.

To detect cycles this implementation utilises the union-find data structure which
provides amortized constant time for answering connectivity queries.


The running time of the algorithm is O(NlogN) which is actually the time to sort the
edges of the graph.
"""

import graph_utils
from union_find import UnionFind

class KruskalMST:

    def __init__(self, graph):
        self.graph = graph
        self.w = 0
        self.mst = []
        self.__mst()

    def __mst(self):
        uf = UnionFind(self.graph.V())

        for edge in self.__sorted_edges():
            u, v, w = edge
            if not uf.connected(u, v):
                self.mst.append((u, v))
                uf.union(u, v)
                self.w += w

    def __sorted_edges(self):
        edges = []
        for u in range(self.graph.V()):
            for e in self.graph.edges(u):

                # source vertex, dest vertex, edge weight
                edges.append((u, e[0], e[1]))

        def compare_edges(e1, e2):
            return cmp(e1[2], e2[2])

        return sorted(edges, compare_edges)

    def weight(self):
        return self.w

if __name__ == "__main__":

    graph = graph_utils.load_weighted_graph('../data/tinyEWG.txt')
    mst = KruskalMST(graph)

    assert abs(1.81 - mst.weight()) < 0.0001

    graph = graph_utils.load_weighted_graph('../data/mediumEWG.txt')
    mst = KruskalMST(graph)

    assert abs(10.46351 - mst.weight()) < 0.0001
