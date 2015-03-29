"""
A Bloom filter is a probabilistic data structure that provides very fast responses to queries
regarding the existence of an element within a set of elements. To answer these queries the
filter doesn't need to store the elements themselves so it has few space requirements.

False positives are possible but not false negatives. Essentially the reply from a bloom filter
can be considered to mean "possibly in the set" or "definitely not in the set".

A Bloom filter with 1% error and an optimal value of k, in contrast, requires only about 9.6 bits
per element - regardless of the size of the elements.

Insertion and query run in O(k), where k is the number of hashing functions.

A Bloom filter with a constant size can represent a set of an arbitrary number of elements.
Adding elements never fails but the error rate will increase with the number of elements.

A Bloom filter consists of m bits and k hash functions. Whenever we insert an element into the
filter, the element is hashed k times with each hashed value corresponding to one of the m bits
which is then set to 1. When we query an element, we hash it again using all k hash functions
and if all the bit positions are set, we then conclude that the element is in the filter. Otherwise,
if any of the k bit positions is not set, we conclude that the element is not in the filter.

Given a desired error rate p, the optimal values for k and m are as follows:

k = (m/n)*ln2
m = -(n*lnp) / (ln2)^2
"""

import  math
from bitarray import bitarray

class BloomFilter:
    def __init__(self, N, error_rate):
        ln2 = math.log(2)
        self.m = int(-N*math.log(error_rate) / (ln2*ln2))
        self.k = int(ln2*self.m / N)
        self.bits = bitarray(self.m)
        self.primes = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
        print "using k = %d and m = %d" % (self.k, self.m)

    def insert(self, value):
        for i in range(self.k):
            pos = self.hash_value(i, value)
            self.bits[pos] = True

    def exists(self, value):
        for i in range(self.k):
            pos = self.hash_value(i, value)
            if not self.bits[pos]:
                return False
        return True

    def size(self):
        print "%d bits are set" % self.bits.count()
        return int(-self.m*math.log(1.0 - self.bits.count()/float(self.m)) / self.k)

    @staticmethod
    def nth_digit(num, d, radix=2):
        return (num // radix ** d) % radix

    @staticmethod
    def count_digits(num, radix=2):
        return int(math.ceil(math.log(num, radix))) if num != 0 else 0

    def hash_value(self, k, value):
        p = self.primes[k % len(self.primes)]
        return p*hash(value) % self.m
        # return hash(p*value) % self.m

    def __str__(self):
        return str(self.bits)

if __name__ == "__main__":
    N = 1000000
    error_rate = 0.01
    print "Testing bloom filter with max size of %d and target error rate of %f" % (N, error_rate)

    bf = BloomFilter(N, error_rate)

    for i in range(N):
        bf.insert(i)

    print "there are about %d items in the filter" % bf.size()

    false_positives = 0
    for i in range(N, 2*N):
        if bf.exists(i):
            false_positives += 1

    print "Got %d false positives, an error rate of %f" % (false_positives, false_positives/float(N))

