"""
Implements Dijkstra's algorithm for finding the shortest path from a given source vertex
and assuming a weighted digraph with only positive weights.

The algorithm proceeds as follows:
    -Maintain a sorted set of edges E that are still not processed. Sorted by their weight in ascending order.
    -Maintain a set of distances D per vertex from the source, these correspond to a tree
    -Set the distance of the source vertex from itself to 0
    -Add all the outbound edges from the source vertex s to the sorted set of edges
    -While the are non tree edges to process:
        -Get the smallest edge e = (u, v) from E
        -For each outbound edge of v:
            -Relax the outbound edge
            -If the edge exists in E then update its weight and its position within the set
            -Otherwise add it in E

Edge relaxation is the operation that adjusts the currently known shortest distances to the vertices
discovered so far. For example, if the algorithm discovers a new edge e = u -> v then a relaxation of
edge e will consists of a check about whether the path s -> u -> v is a shorter path than the one that is
already known for reaching v. The vertex s corresponds to the source vertex.

In this implementation the ordered set is maintained by an indexed min priority queue. The keys are the weights
of the edges and the associated integer corresponds to the vertex index at the arrow of the edge.
"""

from graph_utils import *
import priority_queue


class DijkstraShortestPath:

    def __init__(self, graph, source):
        self.graph = graph

        # the starting vertex, all shortest paths start from this vertex
        self.source = source

        # initialise current vertex distances to infinity
        self.distances = [1e1000 for i in range(graph.V())]

        # each entry indicates the parent vertex from which we arrived to the current vertex
        # follow the parent links in reverse order to reconstruct the shortest path to any vertex
        self.parent_chain = [None for i in range(graph.V())]

        # stores the pending edges prioritised by their weight
        self.edges_queue = priority_queue.IndexedPriorityQueue(graph.V())

        self._dijkstra()

    def _dijkstra(self):
        self.distances[self.source] = 0
        self.edges_queue.insert(self.source, 0)
        # for e in self.graph.edges(self.source):
        #     self.edges_queue.insert(e[0], e[1])

        while not self.edges_queue.is_empty():
            self._relax_edges(self.edges_queue.del_min()[0])

    def _relax_edges(self, v):
        for (vtx, weight) in self.graph.edges(v):
            if self.distances[vtx] > weight + self.distances[v]:
                self.distances[vtx] = weight + self.distances[v]
                self.parent_chain[vtx] = v
                if self.edges_queue.contains(vtx):
                    self.edges_queue.decrease(vtx, self.distances[vtx])
                else:
                    self.edges_queue.insert(vtx, self.distances[vtx])

    def distance(self, v):
        assert v < len(self.distances)
        return self.distances[v]

    def path_to(self, v):
        assert v < len(self.distances)
        path = [v]
        while self.parent_chain[v] is None:
            path.append(self.parent_chain[v])
            v = self.parent_chain[v]
        return path.reverse()

    def exists_path(self, v):
        assert v < len(self.distances)
        return self.parent_chain[v] is not None

if __name__ == "__main__":
    graph = load_weighted_digraph('data/dijkstraData.txt')
    dsp = DijkstraShortestPath(graph, 0)
    print(','.join([str(dsp.distance(i-1)) for i in (7,37,59,82,99,115,133,165,188,197)]))
    # print("Distance: " + str(dsp.distance(i)))

    g = WeightedDigraph(5)
    g.add_weighted_edge(0, 1, 1)
    g.add_weighted_edge(0, 2, 2)
    g.add_weighted_edge(2, 3, 1)
    g.add_weighted_edge(1, 3, 1)
    g.add_weighted_edge(3, 4, 4)
    g.add_weighted_edge(2, 4, 2)

    spa = DijkstraShortestPath(g, 0)
    assert spa.exists_path(3)
    assert spa.distance(3) == 2
    assert spa.distance(4) == 4
