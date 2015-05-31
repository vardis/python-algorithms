"""
Implementation of the Stack ADT using a fixed-size array and a single linked list.

All operations have O(1) running time.
"""

class ArrayStack:
    """
    Stack backed by an array of fixed size.
    """
    def __init__(self, max_size):
        self._top = -1
        self._size = 0
        self._capacity = max_size
        self._array = [None for _ in range(self._capacity)]

    def push(self, item):
        if self._size == self._capacity:
            raise OverflowError('Stack overflow')

        self._top += 1
        self._array[self._top] = item
        self._size += 1

    def pop(self):
        if self._size == 0:
            raise OverflowError('Stack underflow')

        ret = self._array[self._top]
        self._array[self._top] = None
        self._top -= 1
        return ret

    def top(self):
        if self._size == 0:
            raise AttributeError('Empty stack')

        return self._array[self._top]

    def size(self):
        return self._size

    def capacity(self):
        return self._capacity

    def __iter__(self):
        return self

    def next(self):
        if self._size == 0:
            raise StopIteration
        return self.pop()


class LinkedStack:
    """
    A stack based on a single linked list.
    """
    class _Node:
        def __init__(self, item, next):
            self.item = item
            self.next = next

    def __init__(self, max_size):
        self._top = None
        self._size = 0
        self._capacity = max_size

    def push(self, item):
        if self._size == self._capacity:
            raise OverflowError('Stack overflow')

        new_top = LinkedStack._Node(item, self._top)
        self._top = new_top
        self._size += 1

    def pop(self):
        if self._size == 0:
            raise OverflowError('Stack underflow')

        ret = self._top.item
        self._top = self._top.next
        return ret

    def top(self):
        if self._size == 0:
            raise AttributeError('Empty stack')

        return self._top.item

    def size(self):
        return self._size

    def capacity(self):
        return self._capacity

    def __iter__(self):
        return self

    def next(self):
        if self._size == 0:
            raise StopIteration
        return self.pop()

if __name__ == "__main__":

    def test_stack_impl(s):
        for i in range(10):
            s.push(i)

        try:
            s.push(1)
            assert False
        except OverflowError:
            assert True

        for i in range(9, 0, -1):
            assert i == s.top()
            assert i == s.pop()

    test_stack_impl(LinkedStack(10))
    test_stack_impl(ArrayStack(10))