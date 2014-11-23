"""
Implements the binary heap data structure.
"""

__author__ = 'giorgos'

class Heap():

    @staticmethod
    def less(i, j):
        return i < j

    @staticmethod
    def greater(i, j):
        return i > j

    def __init__(self, arr=None, comp=less):
        if not arr: arr = []
        self.h = arr
        self.N = len(arr)
        self.comp = comp

        # builds a heap from the input array
        # Runs in O(N) time. Although there are O(N) nodes to sink and each sink operation
        # runs in O(lgN) time, the amount of work is reduced as we go up towards the root
        # and the time is more tightly bound by O(N) instead of O(NlgN)
        if self.N > 0:
            for i in range(self.N // 2, -1, -1):
                self._sink(i)

    """
    Inserts a new element in the heap.
    Initially the element is placed at the end of the heap and it is then
    kept pushed up until it is correctly ordered within the heap.
    Runs in O(lgN)
    """
    def add(self, e):
        self.h.append(e)
        self.N += 1
        self.swim(self.N - 1)

    """
    Returns the current head of the queue which can correspond to the minimum
    or the greatest element of the heap depending on the ordering operator.
    Runs in O(1)
    """
    def min(self):
        if self.N == 0: raise IndexError
        return self.h[0]

    """
    Reduces the size of the heap and returns the current head of the queue
    which can correspond to the minimum or the greatest element of the heap
    depending on the ordering operator.
    The current head is actually placed at the end of the queue to support
    in-place sorting of arrays.
    Runs in O(lgN)
    """
    def delMin(self):
        m = self.h[0]
        self._exchg(0, self.N - 1)
        self.N -= 1
        self._sink(0)
        return m

    # Runs in O(NlgN)
    def heapsort(self):
        for i in range(self.N, 1, -1):
            self._exchg(0, self.N - 1)
            self.N -= 1
            self._sink(0)


    """
    Sinks down the elements sitting at index i to its appropriate place
    within the heap. While the element is not in the right order with
    respect to its children, it's exchanged with the child would correct
    the heap constraints. The element is keep being pushed until it is
    in a position that satisfies the heap's constraint.
    Runs in O(lgN)
    """
    def _sink(self, i):
        while self._hasChild(i):
            n, c2 = self._children(i)
            v = self.h[n]
            if c2 < self.N and not self._isOrderingConsistent(n, c2):
            # if c2 < self.N and self.h[c2] < v:
                n, v = c2, self.h[c2]

            if self._isOrderingConsistent(n, i):
            # if self.h[i] > v:
                self._exchg(i, n)
                i = n
            else: break

    """
    Pushes the element sitting at index i within the heap up along the tree until
    its ordering is consistent with respect to its children. The element is being
    pushed until a correct ordering is achieved.
    Runs in O(lgN)
    """
    def swim(self, i):
        while i > 0:
            p = self._parent(i)
            if self._isOrderingConsistent(i, p):
            # if self.h[p] > self.h[i]:
                self._exchg(i, p)
                i = p
            else:
                return

    def _hasChild(self, i):
        return (2*i + 1) < self.N

    def _exchg(self, i, j):
        self.h[i], self.h[j] = self.h[j], self.h[i]

    def _isOrderingConsistent(self, i, j):
        return True if self.comp(self.h[i], self.h[j]) else False

    @staticmethod
    def _parent(i):
        return i // 2

    @staticmethod
    def _children(i):
        return (2*i + 1, 2*i + 2)

    def __str__(self):
        return str(self.h)

import random

N = 1000000
arr = []

for i in xrange(N):
    # arr.append(random.randint(0, 100))
    arr.append(i)

random.shuffle(arr)
# print arr

heap = Heap(arr, Heap.greater)

heap.heapsort()

# print arr

def verify_sort(a):
    for i in range(1, len(a)):
        if (a[i-1] > a[i]): raise Exception("Sort is invalid")

verify_sort(arr)
