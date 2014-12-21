"""
Computes the shortest path from a single source and in the context of directed
acyclic graphs.
The algorithm works by first running a topological sort on the graph and the
traversing the graph following the sort order.
At each step we pick a vertex and relax its outgoing edges in a manner similar
to Dijkstra's algorithm.
"""
import topological_sort
import graph_cycle

class DAGShortestPath:

    def __init__(self, g):
        self.g = g

        self.parentChain = [None for i in range(g.V())]

        cycle_detector = graph_cycle.DirectedCycleDetector(g)
        if cycle_detector.has_cycle():
            raise AssertionError("Not a valid graph, it contains cycles")

        topo = topological_sort.TopologicalSort(g)
        self.sorted = topo.topological_sort()


    def shortest_path(self, source):
        self.distances = [1e1000 for i in range(self.g.V())]
        self.distances[source] = 0
        for v in self.sorted:
            for (adj, weight) in self.g.edges(v):
                if self.distances[adj] > self.distances[v] + weight:
                    self.distances[adj] = self.distances[v] + weight
                    self.parentChain[adj] = v

    def longest_path(self, source):
        self.distances = [0.0 for i in range(self.g.V())]
        self.distances[source] = 0
        for v in self.sorted:
            for (adj, weight) in self.g.edges(v):
                if self.distances[adj] < self.distances[v] + weight:
                    self.distances[adj] = self.distances[v] + weight
                    self.parentChain[adj] = v

    def distance_to(self, v):
        return self.distances[v]

    def path_to(self, v):
        path = []
        p = v
        while p is not None:
            path.insert(0, p)
            p = self.parentChain[p]

        return path

if __name__ == "__main__":
    import graph_utils

    dag = graph_utils.load_weighted_digraph('../data/tinyEWDAG.txt', True)

    dag_sp = DAGShortestPath(dag)

    source = 5
    dag_sp.shortest_path(source)

    for i in range(dag.V()):
        print "%d to %d (%f): " % (source, i, dag_sp.distance_to(i)), dag_sp.path_to(i)

    dag_sp.longest_path(source)

    for i in range(dag.V()):
        print "%d to %d (%f): " % (source, i, dag_sp.distance_to(i)), dag_sp.path_to(i)
