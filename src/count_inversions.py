
"""
Adapts the mergesort algorithm to efficiently count the number of inversions
in an input array.
The inversions are counted during the merge phase.
"""

__author__ = 'giorgos'

def merge_sort_top_down(arr):
    if len(arr) < 2:
        return arr

    aux = [None] * len(arr)
    return merge_sort(arr, aux, 0, len(arr) - 1)


def merge_sort(arr, aux, lo, hi):
    inversions = 0
    if hi > lo:
        mid = lo + (hi - lo) // 2
        inversions = merge_sort(arr, aux, lo, mid)
        inversions += merge_sort(arr, aux, mid + 1, hi)
        inversions += merge(arr, aux, lo, mid, hi)
    return inversions

# left part is [lo, mid], right part is [mid+1, hi]
def merge(arr, aux, lo, mid, hi):
    for i in range(lo, hi+1):
        aux[i] = arr[i]

    inversions = 0
    pa, pb = lo, mid + 1
    for i in range(lo, hi+1):
        # left part exhausted
        if pa > mid:
            arr[i] = aux[pb]
            pb += 1

        # right part exhausted
        elif pb > hi:
            arr[i] = aux[pa]
            pa += 1

        # left element greater then right
        # Optimization note: if pb is less than pa, it is then less than all the elements between
        # pa and the mid element so we can increase the inversions count already
        elif aux[pa] > aux[pb]:
            arr[i] = aux[pb]
            pb += 1
            inversions += mid - pa + 1

        # right element greater then left
        else:
            arr[i] = aux[pa]
            pa += 1

    return inversions

a = []
# for i in range(10, 0, -1):
#     a.append(i)
#
# print a
f = open("IntegerArray.txt", "r")
for l in f.readlines():
    if len(l) > 0:
        num = int(l)
        a.append(num)

print 'read %d numbers' % len(a)

print 'found %d inversions' % merge_sort_top_down(a)


