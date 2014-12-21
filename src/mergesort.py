"""
An implementation of the top-down variation of Mergesort,
"""
import random
import sort_utils

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

a = sort_utils.generate_random_array(10000)
random.shuffle(a)
merge_sort_top_down(a)
sort_utils.verify_sort(a)
