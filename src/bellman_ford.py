
class BellmanFordShortestPath:
    """
    Implementation of the Bellman-Ford algorithm for finding shortest paths in weighted digraphs.
    This is a general algorithm that works even under the presence of cycles in the graph. Negative
    cycles prevent the algorithm from calculating a shortest path and thus it will abort once such
    a cycle is detected.

    The algorithm performs V-1 passes over all the edges in the graph. In each iteration it relaxes
    each one of the edges in the graph. At the end of the iteration it checks for the presence of a
    negative cycle in which case it aborts.

    The reason we perform exactly V-1 passes it because a shortest path can only contain up to V-1 edges
    from the source vertex s, resulting to a maximum shortest path length of V vertices. Any more edges
    and we have a cyclic path which is not a shortest path.

    It has an asymptotic complexity of O(V*E), in dense graph E can be O(V^2) so in that case the algorithm
    will run in O(V^3).
    """
    INFINITY = 1e1000

    def __init__(self):
        self.edge_to = {}
        self.paths = {}

    def shortest_path(self, G, s):
        """
        Returns all the shortest paths in the given graph G starting from the vertex s
        Vertices that are not reachable by s will have a shortest path of infinite weight.
        """
        self.__initialisation_pass(G, s)

        for i in range(G.V() - 1):
            self.__relax_edges(G)

        if self.__has_negative_cycle(G):
            raise AssertionError("Negative cycle detected")


    def __initialisation_pass(self, G, s):
        for v in range(G.V()):
            self.paths[v] = BellmanFordShortestPath.INFINITY
            self.edge_to[v] = None

        self.paths[s] = 0

    def __relax_edges(self, G):
        for edge in G.edge_list():
            (v, u, w) = edge

            if self.paths[u] > self.paths[v] + w:
                self.paths[u] = self.paths[v] + w
                self.edge_to[u] = v


    def __has_negative_cycle(self, G):
        for v in range(G.V()):
            for (u, w) in G.edges(v):
                if self.paths[u] > self.paths[v] + w:
                    return True
        return False

    def path_length(self, v):
        return self.paths[v]

    def path_to(self, v):
        path = [v]
        while self.edge_to[v] is not None:
            p = self.edge_to[v]
            path.append(p)
            v = p
        path.reverse()
        return path


if __name__ == "__main__":
    import graph_utils

    def report_results(G, s, bf):
        for v in range(G.V()):
            sp = ' -> '.join([str(x) for x in bf.path_to(v)])
            print "%d to %d (%.2f) %s" % (s, v, bf.path_length(v), sp)

    source = 0
    bf = BellmanFordShortestPath()

    # test graph with negative edges
    G = graph_utils.load_weighted_digraph('../data/tinyEWDNeg.txt', True)
    bf.shortest_path(G, source)
    report_results(G, source, bf)

    # test graph with negative cycle
    try:
        G = graph_utils.load_weighted_digraph('../data/tinyEWDNegCyc.txt', True)
        bf.shortest_path(G, source)
    except AssertionError:
        print 'Negative cycle exists'


