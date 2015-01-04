__author__ = 'giorgos'

"""
Applies Kosaraju's algorithm for finding the strong connected components in
a digraph.

The algorithm is defined as follows:
    -Take the reverse graph G'
    -Run a post order DFS taking note of the order of discovery of the vertices
    -Run a normal DFS on the input graph G by visiting the vertices in the order
     produced from the previous step.
    -Every exhaustive step of the DFS will mark all the vertices that are strongly
     connected
"""

class SCC:
    def __init__(self, g):
        self._G = g
        self._marked = [False for i in range(self._G.V())]

        # stores the order obtained from dfsPostOrder
        self._order = []

        # stores the sizes of the strong connected components
        self._components = []

        # counts the vertices belonging to the current component
        self._count = 0

        self._reverse = None

    def scc(self):
        # obtain the order through a reverse post-order DFS
        self._reverse = self._G.reverse()
        for v in range(self._reverse.V()):
            if not self._marked[v]:
                self.dfs_post_order(v)

        # now run a DFS with the obtained order
        self._marked = [False for i in range(self._G.V())]
        # for v in self._order:
        while len(self._order) > 0:
            v = self._order.pop()
            if not self._marked[v]:
                self._count = 0
                self.dfs(v)
                self._components.append(self._count)

        return self._components

    def dfs(self, v):
        stack = [v]
        while len(stack) > 0:
            v = stack.pop()
            if not self._marked[v]:
                self._marked[v] = True
                self._count += 1
                for w in self._G.edges(v):
                    # support for digraphs
                    if type(w) is list or type(w) is tuple:
                        w = w[0]

                    stack.append(w)


    def dfs_post_order(self, v):
        stack = [v]
        while len(stack) > 0:
            v = stack.pop()
            if v < 0:
                self._order.append(-v)
                continue

            if not self._marked[v]:
                self._marked[v] = True
                stack.append(-v)
                for w in self._reverse.edges(v):
                    # support for digraphs
                    if type(w) is list or type(w) is tuple:
                        w = w[0]
                    stack.append(w)


if __name__ == "__main__":
    import graph_utils
    G = graph_utils.load_digraph("SCC.txt", zero_based=False)
    # G = graph_utils.load_digraph("tinyDG.txt")
    scc = SCC(G)
    comps = sorted(scc.scc())
    comps.reverse()
    print(comps[0:10])
