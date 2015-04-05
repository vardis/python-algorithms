"""
A minimum priority queue which allows clients to associate an integer with each key.
"""


class IndexedPriorityQueue:
    def __init__(self, maxItems):
        self.maxItems = maxItems
        self.N = 0

        # the binary heap, contains indexes
        self.heap = [None for _ in range(maxItems)]

        # maps from indexes to heap indexes
        self.index = [-1 for _ in range(maxItems)]

        # maps from indexes to keys
        self.keys = [None for _ in range(maxItems)]

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
        while i >= 1 and self._key_of(p) > self._key_of(i):
            self._exchange(p, i)
            i = p
            p = self._parent(p)

    def sink(self, i):
        while self._left_child(i) < self.N:
            l, r = self._left_child(i), self._right_child(i)
            min_child = l if (l == self.N - 1 or self._key_of(l) < self._key_of(r)) else r
            if self._key_of(min_child) < self._key_of(i):
                self._exchange(min_child, i)
                i = min_child
            else:
                return

    def insert(self, index, key):
        assert self.N <= self.maxItems
        if self.keys[index] is not None:
            if self.keys[index] < key:
                self.increase(index, key)
            else:
                self.decrease(index, key)
            return

        self.keys[index] = key
        self.heap[self.N] = index
        self.index[index] = self.N
        self.N += 1
        self.swim(self.N - 1)

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
        self.index[min_index] = -1
        # self.heap[self.N] = None
        self.heap[self.N - 1] = None
        self.N -= 1

        self.sink(0)

        return (v, k)

    def min_index(self):
        return self.heap[0]

    def min_key(self):
        return self.keys[self.heap[0]]

    def key_of(self, index):
        assert self.contains(index)
        return self.keys[index]

    def size(self):
        return self.N

    def is_empty(self):
        return self.N == 0

    def contains(self, index):
        return index in self.heap


class PriorityQueue:
    """
    A general binary heap implementation which can handle either plain comparable keys
    or key-value pairs.

    Using plain keys:
        pq = PriorityQueue(10)
        for i in range(1, 11):
            pq.insert(i)

        for i in range(1, 11):
            assert pq.del_min() == i

    Using key-value pairs:

        pq = PriorityQueue(10)
        pq.insert(1000.0, "!")
        pq.insert(0.0, "Hello ")
        pq.insert(12.44, "World")
        pq.insert(-5.1, "> ")

        s = ""
        while not pq.is_empty():
            s = s + pq.del_min()

        assert s == "> Hello World!"

        import random

        arr = [x for x in range(1, 11)]
        random.shuffle(arr)
        pq = PriorityQueue.heapify(arr)
        print pq.heap

        for i in range(1, 11):
            assert pq.del_min() == i
    """

    def __init__(self, maxItems):
        self.maxItems = maxItems
        self.N = 0

        # the binary heap, contains indexes
        self.heap = [None for _ in range(maxItems)]

        # maps from keys to values
        self.values = {}

    @staticmethod
    def heapify(arr):
        pq = PriorityQueue(len(arr))
        pq.heap = [x for x in arr]
        pq.N = len(arr)

        for i in range(pq.N / 2, -1, -1):
            pq.sink(i)

        for x in pq.heap:
            pq.values[x] = x
        return pq

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

    def _is_minpq(self, i):

        if i >= self.N:
            return True

        left = self._left_child(i)
        right = self._right_child(i)

        if left < self.N and self.heap[i] > self.heap[left]:
            return False

        if right < self.N and self.heap[i] > self.heap[right]:
            return False

        val = self._is_minpq(left) and self._is_minpq(right)
        if not val:
            print val
        return val

    def swim(self, i):
        p = self._parent(i)
        while i >= 1 and self.heap[p] > self.heap[i]:
            self._exchange(p, i)
            i = p
            p = self._parent(p)

    def sink(self, i):
        while self._left_child(i) < self.N:
            l, r = self._left_child(i), self._right_child(i)
            min_child = l if (l == self.N - 1 or self.heap[l] < self.heap[r]) else r
            if self.heap[min_child] is not None and self.heap[min_child] < self.heap[i]:
                self._exchange(min_child, i)
                i = min_child
            else:
                return

    def insert(self, key, val=None):
        assert self.N <= self.maxItems
        if val is None:
            val = key

        if key in self.values:
            self.values[key] = val
        else:
            self.values[key] = val
            self.heap[self.N] = key
            self.N += 1
            self.swim(self.N - 1)

        assert self._is_minpq(0)

    def del_min(self):
        if self.N == 0:
            raise Exception("Queue is empty")

        k = self.heap[0]
        assert k in self.values

        v = self.values[k]

        self._exchange(0, self.N - 1)
        del self.values[k]

        self.N -= 1
        self.heap[self.N] = None

        self.sink(0)

        assert self._is_minpq(0)

        return v

    def min_key(self):
        return self.heap[0]

    def size(self):
        return self.N

    def is_empty(self):
        return self.N == 0


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

    pq.insert(4, 0.0)
    pq.increase(4, 100.0)

    i, k = pq.del_min()
    assert k == 0.2 and i == 2

    pq.insert(3, 10.0)

    i, k = pq.del_min()
    assert k == 1.0 and i == 0

    pq.decrease(3, 1.0)

    i, k = pq.del_min()
    assert k == 1.0 and i == 3

    i, k = pq.del_min()
    assert k == 1.5 and i == 1

    assert (4, 100.0) == pq.del_min()

    assert pq.is_empty()

    N = 1000
    pq = IndexedPriorityQueue(N)

    nums = []
    queue = PriorityQueue(N)

    for i in range(N):
        nums.append(i)
        pq.insert(i, i)

    import random

    random.shuffle(nums)
    # for n in nums:
    # queue.insert(n)

    queue = PriorityQueue.heapify(nums)

    def sort_indexed_pairs(p1, p2):
        return cmp(p1[1], p2[1])

    for i in range(N):
        k = pq.del_min()[1]
        w = queue.del_min()

        cmp1 = i == k
        cmp2 = i == w
        if not cmp1 or not cmp2:
            print "invalid"

        assert cmp1
        assert cmp2

    pq = PriorityQueue(10)

    pq.insert(1000.0, "!")
    pq.insert(0.0, "Hello ")
    pq.insert(12.44, "World")
    pq.insert(-5.1, "> ")

    s = ""
    while not pq.is_empty():
        s = s + pq.del_min()
    assert s == "> Hello World!"

    import random

    arr = [x for x in range(1, 11)]
    random.shuffle(arr)
    pq = PriorityQueue.heapify(arr)
    print pq.heap

    for i in range(1, 11):
        assert pq.del_min() == i



