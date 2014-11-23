__author__ = 'giorgos'

import math
import random

def verify_sort(a):
    for i in range(1, len(a)):
        if (a[i-1] > a[i]): raise Exception("Sort is invalid")


a = [int(1000 * random.random()) for i in range(100000)]

# print a


def insertion_sort(arr):
    for i in range(1, len(arr)):
        for j in range(i, 0, -1):
            if arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
            else:
                break


# insertion_sort(a)
# print a
# verify_sort(a)


def merge_sort_top_down(arr):
    if len(arr) < 2:
        return arr

    aux = [None] * len(arr)
    merge_sort(arr, aux, 0, len(arr) - 1)


def merge_sort(arr, aux, lo, hi):
    if hi > lo:
        mid = lo + (hi - lo) // 2
        merge_sort(arr, aux, lo, mid)
        merge_sort(arr, aux, mid + 1, hi)
        merge(arr, aux, lo, mid, hi)

def merge(arr, aux, lo, mid, hi):
    for i in range(lo, hi+1):
        aux[i] = arr[i]

    pa, pb = lo, mid + 1
    for i in range(lo, hi+1):
        if pa > mid:
            arr[i] = aux[pb]
            pb += 1
        elif pb > hi:
            arr[i] = aux[pa]
            pa += 1
        elif aux[pa] > aux[pb]:
            arr[i] = aux[pb]
            pb += 1
        else:
            arr[i] = aux[pa]
            pa += 1


random.shuffle(a)
print a

merge_sort_top_down(a)
print a
verify_sort(a)
