"""
The UF algorithm provides an efficient way to respond to queries regarding the connectivity between a set of elements.

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
we encounter a root element.

This particular implementation goes by the name of Weighted Quick Union with Path Compression. The term path compression
refers to the operation of caching the root lookup result for an element whenever the Find operation is called and
updating the components array with that information. This reduces the lookup time for future Find operations on the
same element, in the best case from logN down to 1.

It provides amortized constant time for both find and union operations.

"""

class UnionFind:

    def __init__(self, max_elements):
        self.N = max_elements
        self.num_components = self.N
        self.elements = [i for i in range(self.N)]
        self.root_weights = [1 for _ in range(self.N)]

    def find(self, p):
        assert 0 <= p < self.N
        element = p
        while self.elements[p] != p:
            p = self.elements[p]

        # cache the root information
        self.elements[element] = p

        return p

    def union(self, p, q):
        assert 0 <= p < self.N
        assert 0 <= q < self.N

        if p != q:
            p_root = self.find(p)
            q_root = self.find(q)

            if p_root != q_root:
                p_root_weight = self.root_weights[p_root]
                q_root_weight = self.root_weights[q_root]

                if p_root_weight < q_root_weight:
                    self.elements[p_root] = q_root
                    self.root_weights[q_root] += self.root_weights[p_root]
                else:
                    self.elements[q_root] = p_root
                    self.root_weights[p_root] += self.root_weights[q_root]

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
