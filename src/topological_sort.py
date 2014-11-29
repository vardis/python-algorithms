"""
Computes the topological sort for a DAG.

    Run a DFS on G.
    As each vertex is visited, at post-order time, it is pushed to a stack.
    At the end of the DFS the stack contains the ordering of the vertices.


Runs in O(n + m) time where n is the number of vertices and m is the
number of edges.
"""
import graph_utils


class TopologicalSort:

    def __init__(self, graph):
        self.G = graph
        self.visited = [False for i in range(graph.V())]
        self.count = self.G.V() - 1
        self.ordering = []

    def topological_sort(self):
        for v in range(self.G.V()):
            if not self.visited[v]:
                self.visited[v] = True
                self.post_dfs(v)

    def post_dfs(self, v):
        for e in self.G.edges(v):
            if not self.visited[e]:
                self.visited[e] = True
                self.post_dfs(e)
        # stack push
        self.ordering.insert(0, v)
        self.count -= 1



if __name__ == "__main__":
    course_graph = graph_utils.Digraph(13)

    course_count = 0
    course_by_name = {}
    course_by_id = {}

    f = open("../data/jobs.txt")
    for l in f.readlines():
        courses = l.split('/')
        current_curse = courses[0]
        if current_curse not in course_by_name:
            course_by_name[current_curse] = course_count
            course_by_id[course_count] = current_curse
            course_count += 1
        current_curse_id = course_by_name[current_curse]

        for c in [cu.strip() for cu in courses[1:]]:
            if c not in course_by_name:
                course_by_name[c] = course_count
                course_by_id[course_count] = c
                course_count += 1
            course_graph.add_edge(current_curse_id, course_by_name[c])

    print(course_by_name)

    topo_sort = TopologicalSort(course_graph)
    topo_sort.topological_sort()
    print(topo_sort.ordering)

    for i in topo_sort.ordering:
        print(course_by_id[i])