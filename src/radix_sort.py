"""
Implementation for radix sort or LSD sort.

We sort keys that can be represented as a series of digits. As everything is stored in binary
it is trivial to find a corresponding number for a key. For example, strings are a series of
characters and each character can correspond to an ASCII or Unicode code.

The algorithm considers the digits in a radix R and traverses them in a right-to-left fashion.
The first step starts with the rightmost or least significant digit. At step i of the algorithm
we sort the keys using the i-th digit.

The algorithm does not use comparisons in order to order the keys by their digits. Instead the
digit of a key determines its distribution in the final sorted order.

The running time is d*(N + 2^r), where d is the number of digits per key and r is the number of
bits required to represent a digit of base R. For example, using R=10 and considering keys of 32 bits
in length, then we have r = 4, d = 8 and T(N) = 8*N + 128.

 As a small proof of the running time formula, consider that each pass of the algorithm is a counting
 sort whose running time is Theta(N + 2^r). For keys of d digits the total running time is then Theta(d*(N + 2^r)).
"""
import math

def counting_sort(arr):
    num_buckets = max(arr) + 1
    counts = [0 for _ in range(num_buckets)]
    for i in arr:
        counts[i] += 1

    accum = 0
    for i in range(num_buckets):
        old_count = counts[i]
        counts[i] = accum
        accum += old_count

    ordered = [0 for _ in range(len(arr))]
    for i in arr:
        ordered[counts[i]] = i
        counts[i] += 1

    return ordered

def radix_sort(arr):
    def nth_digit(num, d, radix):
        return (num // radix ** d) % radix

    def count_digits(num, radix):
        return int(math.ceil(math.log(num, radix)))

    radix = 10
    ordered = [0 for _ in range(len(arr))]
    steps = count_digits(max(arr), radix)
    aux = arr[:]
    for s in range(steps):
        counts = [0 for _ in range(radix)]
        for i in aux:
            counts[nth_digit(i, s, radix)] += 1

        accum = 0
        for i in range(radix):
            old_count = counts[i]
            counts[i] = accum
            accum += old_count

        for i in aux:
            digit = nth_digit(i, s, radix)
            ordered[counts[digit]] = i
            counts[digit] += 1

        aux, ordered = ordered, aux

    return aux

import sort_utils

a = sort_utils.generate_random_array(1000000)
# print a

b = counting_sort(a)
# print b
sort_utils.verify_sort(b)

b = radix_sort(a)
# print b
sort_utils.verify_sort(b)
