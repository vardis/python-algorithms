import random

def verify_sort(a):
    for i in range(1, len(a)):
        if (a[i-1] > a[i]):
            raise Exception("Sort is invalid at {0} position ({1} > {2})".format(i, a[i-1], a[i]))

def generate_random_array(length):
    return [int(1000 * random.random()) for _ in range(length)]
