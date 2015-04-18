"""
An algorithm that finds a minimum spanning tree, given a graph using greedy
heuristics. The heuristic in this case being the minimum edge that connects
the set of already visited vertices to the set of the un-visited vertices.

It is very similar to Dijkstra's shortest-path algorithm. In pseudo-code
it goes like this:

Prim-MST(G)
    Select an arbitrary vertex s to start the tree from.
    While (there are still non-tree vertices)
        Select the edge of minimum weight between a tree and non-tree vertex
        Add the selected edge and vertex to the tree Tprim.

The algorithm goes through each of the N vertices and loops all M edges of the vertex.
This results in O(N*M) complexity

However, using a priority queue to find the minimum crossing edge at each iteration
of the algorithm reduces the time to O(MlogN)

With N,M being the number of vertices and edges, respectively.

"""
from graph_utils import *
import priority_queue


class PrimMST:
    def __init__(self, graph):
        self.graph = graph
        self.mst_weight = 0
        self.mst()

    def mst(self):
        source = 0
        processed = {source}
        remaining = set([i for i in range(0, self.graph.V()) if i != source])

        pq = priority_queue.IndexedPriorityQueue(graph.V())

        for (vtx, weight) in self.graph.edges(source):
            pq.insert(vtx, weight)

        while len(remaining) > 0 and pq.size() > 0:
            v, w = pq.del_min()

            if v not in processed and v in remaining:
                # print 'Adding ', v, ' weight ', w
                self.mst_weight += w
                processed.add(v)
                remaining.remove(v)

                for (vtx, weight) in self.graph.edges(v):
                    if vtx not in processed:
                        if not pq.contains(vtx):
                            pq.insert(vtx, weight)
                        elif pq.key_of(vtx) > weight:
                            pq.decrease(vtx, weight)


    def weight(self):
        return self.mst_weight

if __name__ == "__main__":
    graph = load_weighted_graph('../data/tinyEWG.txt', True)
    mst = PrimMST(graph)
    print mst.weight()
    assert 1.81 == mst.weight()

    graph = load_weighted_graph('../data2.txt', False)
    mst = PrimMST(graph)
    print mst.weight()

