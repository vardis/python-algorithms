"""
Finds the max-spacing k-clusterings for a set of N points.

The points and their distances are modelled as a weighted un-directed graph where each point
corresponds to a vertex and the edge weights correspond to the euclidean distance between
the two connecting vertices.

This implementation uses a greedy algorithm which resembles a lot Kruskal's algorithm for the
minimum spanning tree.

We start by assigning each vertex into each own cluster (i.e. connected component) and at each
step of the algorithm we pick the next edge with the minimum weight. If the vertices corresponding
to that edge are not in the same cluster, we merge their clusters into a single one.

We repeat the above process until we end up with k clusters, where k is a user provided parameter.
"""

import graph_utils
from union_find import UnionFind

class SingleLinkedClustering:

    def __init__(self, k, graph):
        self.graph = graph
        self.k = k
        self.spacing = 1e100
        self.__cluster()

    def __cluster(self):

        uf = UnionFind(self.graph.V())

        min_spacing = 1e100

        for edge in self.__sorted_edges():

            u, v, w = edge

            if uf.count_components() > self.k and not uf.connected(u, v):
                uf.union(u, v)

            elif not uf.connected(u, v):
                # once we have k clusters,
                # examine each cross-clusters edge and pick the minimum
                if min_spacing > w:
                    min_spacing = w

        self.spacing = min_spacing

    def __sorted_edges(self):
        edges = []
        for u in range(self.graph.V()):
            for e in self.graph.edges(u):

                # source vertex, dest vertex, edge weight
                edges.append((u, e[0], e[1]))

        def compare_edges(e1, e2):
            return cmp(e1[2], e2[2])

        return sorted(edges, compare_edges)

    def max_spacing(self):
        return self.spacing


if __name__ == "__main__":

    graph = graph_utils.load_weighted_graph('../data/clustering1.txt', False)
    slk = SingleLinkedClustering(4, graph)

    print slk.max_spacing()
