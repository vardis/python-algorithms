"""
The UnionFind data structure provides an efficient way to respond to queries regarding the connectivity between a set of elements.

Connectivity queries and the linkage of the elements is provided through two operations:
    - Find(p) - returns an integer that indicates the connected component in which p belongs
    - Union(p, q) - connects the elements p and q
    - Connected(p, q) - returns a boolean that indicates whether p and q are within the same component

The connectivity between two elements is supposed to exhibit the following properties:

- Reflexive : p is connected to p.
- Transitive : If p is connected to q and q is connected to r, then p is connected to r.
- Symmetric : If p is connected to q, then q is connected to p.

In the implementation that follows we use an array of integers to represent the elements. Each integer represents
a component or site, into which the respective element belongs. Components are assigned, arbitrarily, an integer
between 0 and N-1, where N is the number of components.For example, array[0] denotes the site or connected component
in which the 0-th element belongs.

For each connected component we maintain a leader or root element. All elements within the same component have an
array entry that equals the root element of their component. If the 1st and 2nd elements belong in the same component
for which the 4th element is the root, then array[0] = array[1] = 3.

The root element has the property that array[root] = root.

However, elements can be linked to their root indirectly through successive union operations. For example an element
could be initially rooted to element 0 but after a union operation between 0 and 1, the new root is 1. Therefore to
safely calculate the root of an arbitrary element p we have to follow all the element references in the array until
we encounter a root element. In the worst case we will need to traverse up to O(N) links to arrive to the root from
another random element. We therefore want to minimise the number of steps required to reach the root from any element.



This particular implementation goes by the name of Union by Rank with Path Compression.

For each root we maintain its rank, the maximum number of links we have to follow from a leaf to reach the root. When
connecting two roots, we aim to link the root with the smallest rank beneath the root with the higher rank in order
to minimize the height of the tree. Using this tactic, the height of the tree increases only when merging two roots
of the same rank. For N elements we can merge two equally-ranked roots up to logN times which places logN as the upper
bound for the tree's height and therefore the cost of the Find operation. This cost can be reduced even further by
applying path compression.

The term path compression refers to the operation of caching the root lookup result for an element whenever the
Find operation is called and updating the components array with that information. This reduces the lookup time for
future Find operations on the same element, in the best case from logN down to 1.

It provides amortized constant time for both find and union operations.

"""

class UnionFind:

    def __init__(self, max_elements):
        self.N = max_elements
        self.num_components = self.N
        self.elements = [i for i in range(self.N)]
        self.ranks = [1 for _ in range(self.N)]

    def find(self, p):
        assert 0 <= p < self.N

        while self.elements[p] != p:
            # path compression by directly caching the lookup result in the component array
            self.elements[p] = self.elements[self.elements[p]]
            p = self.elements[p]

        return p

    def union(self, p, q):
        assert 0 <= p < self.N
        assert 0 <= q < self.N

        if p != q:
            p_root = self.find(p)
            q_root = self.find(q)

            if p_root != q_root:
                p_rank = self.ranks[p_root]
                q_rank = self.ranks[q_root]

                if p_rank < q_rank:
                    self.elements[p_root] = q_root
                elif q_rank < p_rank:
                    self.elements[q_root] = p_root
                else:
                    self.elements[q_root] = p_root
                    self.ranks[p_root] += 1

                self.num_components -= 1

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def count_components(self):
        return self.num_components

if __name__ == "__main__":

    N = 100000
    uf = UnionFind(N)

    for i in range(N):
        assert i == uf.find(i)

    assert uf.count_components() == N

    for even in range(2, N, 2):
        uf.union(0, even)

    for odd in range(3, N, 2):
        uf.union(1, odd)

    assert uf.count_components() == 2

    for even in range(2, N, 2):
        assert uf.connected(0, even)

    for odd in range(3, N, 2):
        assert uf.connected(1, odd)

    uf.union(0, 1)

    assert uf.count_components() == 1

    with open('../data/mediumUF.txt', 'r') as input_file:
        N = int(input_file.readline())
        uf = UnionFind(N)

        for ln in input_file.readlines():
            p, q = [ int(x) for x in ln.split()]
            uf.union(p, q)

    print uf.count_components(), ' connected components'
