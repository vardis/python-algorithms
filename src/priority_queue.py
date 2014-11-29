"""
A minimum priority queue which allows clients to associate an integer with each key.
"""

class IndexedPriorityQueue:

    def __init__(self, maxItems):
        self.maxItems = maxItems
        self.N = 0

        # the binary heap, contains indexes
        self.heap = [None for i in range(maxItems)]

        # maps from indexes to heap indexes
        self.index = [-1 for i in range(maxItems)]

        # maps from indexes to keys
        self.keys = [None for i in range(maxItems)]

    def _key_of(self, i):
        return self.keys[self.heap[i]]

    @staticmethod
    def _left_child(i):
        return 1 + i * 2

    @staticmethod
    def _right_child(i):
        return 2 + i * 2

    @staticmethod
    def _parent(i):
        return (i - 1) // 2

    def _exchange(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.index[self.heap[i]] = i
        self.index[self.heap[j]] = j

    def swim(self, i):
        p = self._parent(i)
        while i > 1 and self._key_of(p) > self._key_of(i):
            self._exchange(p, i)
            i = p
            p //= 2

    def sink(self, i):
        while self._left_child(i) <= self.N:
            l, r = self._left_child(i), self._right_child(i)
            min_child = l if (l == self.N or self._key_of(l) < self._key_of(r)) else r
            if self._key_of(min_child) < self._key_of(i):
                self._exchange(min_child, i)
                i = min_child
            else:
                return

    def insert(self, index, key):
        assert self.N < self.maxItems
        self.keys[index] = key
        self.heap[self.N] = index
        self.index[index] = self.N
        self.N += 1
        self.swim(self.N-1)

    def increase(self, index, key):
        self.keys[index] = key
        self.sink(self.index[index])

    def decrease(self, index, key):
        self.keys[index] = key
        self.swim(self.index[index])

    def del_min(self):
        min_index = self.min_index()
        k, v = self.keys[min_index], min_index

        self._exchange(0, self.N - 1)
        self.keys[min_index] = None
        self.index[min_index] = self.N
        self.N -= 1

        return (v, k)

    def min_index(self):
        return self.heap[0]

    def min_key(self):
        return self.keys[self.heap[0]]

    def key_of(self, index):
        assert 0 <= index <= self.N
        assert self.contains(index)
        return self.keys[index]

    def size(self):
        return self.N

    def is_empty(self):
        return self.N == 0

    def contains(self, index):
        return self.keys[index] is not None

if __name__ == "__main__":
    pq = IndexedPriorityQueue(10)
    pq.insert(0, 1.0)
    pq.insert(1, 1.5)
    pq.insert(2, 0.2)

    assert pq.size() == 3
    assert not pq.is_empty()
    assert pq.key_of(0) == 1.0
    assert pq.key_of(1) == 1.5
    assert pq.key_of(2) == 0.2
    assert pq.contains(0)
    assert pq.contains(1)
    assert pq.contains(2)
    assert not pq.contains(3)

    assert pq.min_key() == 0.2
    assert pq.min_index() == 2

    i, k = pq.del_min()
    assert k == 0.2 and i == 2

    i, k = pq.del_min()
    assert k == 1.0 and i == 0

    i, k = pq.del_min()
    assert k == 1.5 and i == 1

    assert pq.is_empty()

