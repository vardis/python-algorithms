"""
Examines the effect of applying different strategies in choosing the partitioning element in quicksort.
The following options are considered:
    -First element: The first element is used as the pivot
    -Last element: The last element in the input array is used as the pivot
    -Median element: We compute the median of the first, last and middle element of the input array and use that
                    as the pivot

    The median element strategy appears to lead to more balanced partitions and thus less comparisons leading
    to a faster execution.
"""

import sys

sys.setrecursionlimit(10000)

def pickFirstElementAsPivot(arr, left, right):
    return left

def pickLastElementAsPivot(arr, left, right):
    return right

def pickMedianElementAsPivot(arr, left, right):
    l = arr[left]
    r = arr[right]
    sz = right - left + 1
    if (sz % 2) == 1:
        m = left + sz / 2
    else:
        m = left + (sz / 2) - 1

    s = [l, arr[m] ,r]
    s.sort()
    if l == s[1]:
        return left
    elif r == s[1]:
        return right
    else:
        return m

def qsort(arr, left, right, pivotStrategy):
    partition_size = right - left + 1
    comparisons = 0
    if right > left:
        pivot = pivotStrategy(arr, left, right)
        arr[left], arr[pivot] = arr[pivot], arr[left]

        pivot = partition(arr, left, right)
        comparisons = partition_size - 1
        comparisons += qsort(arr, left, pivot - 1, pivotStrategy)
        comparisons += qsort(arr, pivot + 1, right, pivotStrategy)
    return comparisons

"""
    i: points after the end of the subarray with entries less than the pivot
    j: points at the beginning of the subarray with entries that haven't been examined yet
"""
def partition(arr, left, right):
    pivot = arr[left]
    i = left + 1
    for j in range(left + 1, right + 1):
        if arr[j] < pivot:
            arr[j], arr[i] = arr[i], arr[j]
            i += 1

    arr[left], arr[i - 1] = arr[i - 1], arr[left]
    return i - 1

a = []
f = open("../data/qsort_input.txt", "r")
for l in f.readlines():
    if len(l) > 0:
        num = int(l)
        a.append(num)

import sort_utils

b = []
b.extend(a)

c = []
c.extend(a)

comps = qsort(a, 0, len(a) - 1, pickFirstElementAsPivot)
sort_utils.verify_sort(a)

print 'a comparisons', comps

b[0], b[-1] = b[-1], b[0]
comps = qsort(b, 0, len(b) - 1, pickLastElementAsPivot)
sort_utils.verify_sort(b)
print 'b comparisons', comps

p = pickMedianElementAsPivot(c, 0, len(c) - 1)
c[0], c[p] = c[p], c[0]
comps = qsort(c, 0, len(c) - 1, pickMedianElementAsPivot)
sort_utils.verify_sort(c)
print 'c comparisons', comps