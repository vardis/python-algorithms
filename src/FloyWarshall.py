"""
The Floyd-Warshall algorithm is an application of the dynamic programming paradigm and provides a way
to efficiently evaluate all-pairs shortest paths for a given graph.

The algorithm is iterative. In each iteration we calculate the shorted distance between all pairs of
vertices using a maximum number of K intermediate vertices. We iterate through all possible N intermediate
vertices K and through all possible pairs of vertices (u, v) and check whether using the k-th vertex
as an intermediary helps us by leading us to a shorter path u -> v than we previously knew.

This condition can be stated as follows:

    W[i][j](k) = min( W[i][j][k-1], W[i][k][k-1] + W[k][j][k-1])

where W[i][j][k] is the weight of the path i -> j having k intermediary vertices.

For a graph with N vertices we represent the shortest paths using an adjacency matrix of NxN. This
matrix is initialized as:

    Adj[i][j] = Eij, if i != j and there's an edge between i, j
    Adj[i][j] = 0, if i = j
    Adj[i][j] = +INF, if i != j and there's no edge between i, j

At the end of the algorithm, the adjacency matrix provides the transitive closure of a graph. An entry
Adj[i][j] provides the length of the shortest path between i and j or +INF in case no such path exists.

Under the presence of negative cycles, the diagonal of the adjacency matrix will contain negative values
for at least one vertex.
"""

class FloydWarshall:

    def __init__(self, graph):
        self.num_vertices = graph.V()
        self.weights = {}

        INF = 1e100

        for v in range(graph.V()):
            self.weights[v] = [ INF if x != v else 0 for x in range(self.num_vertices)]
            for (u, w) in graph.edges(v):
                self.weights[v][u] = w

    def all_shortest_paths(self):
        for k in range(self.num_vertices):
            print(k)
            for i in range(self.num_vertices):
                for j in range(self.num_vertices):
                    through_k = self.weights[i][k] + self.weights[k][j]
                    if self.weights[i][j] > through_k:
                        self.weights[i][j] = through_k

    def shortest_shortest(self):
        shortest_path = 1e100
        for v in self.weights.values():
            shortest_path = min(min(v), shortest_path)
        return shortest_path

    def has_negative_cycle(self):
        for k in range(self.num_vertices):
            if self.weights[k][k] < 0:
                return True
        return False

if __name__ == "__main__":
    import graph_utils

    G = graph_utils.load_weighted_digraph('../data/floy-warshall-negative_cycle.txt')

    fw = FloydWarshall(G)
    fw.all_shortest_paths()
    assert fw.has_negative_cycle()


    G = graph_utils.load_weighted_digraph('../data/floyd-warshall-1000.txt')

    fw = FloydWarshall(G)
    fw.all_shortest_paths()
    assert not fw.has_negative_cycle()
    print(fw.shortest_shortest())
