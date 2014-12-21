import sort_utils
import random

def insertion_sort(arr):
    for i in range(1, len(arr)):
        for j in range(i, 0, -1):
            if arr[j] < arr[j - 1]:
                arr[j], arr[j - 1] = arr[j - 1], arr[j]
            else:
                break

a = sort_utils.generate_random_array(10000)

random.shuffle(a)
insertion_sort(a)
sort_utils.verify_sort(a)
