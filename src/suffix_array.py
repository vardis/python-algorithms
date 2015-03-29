import sys

sys.setrecursionlimit(10000)


class SuffixArray:
    def __init__(self, text):
        self.text = text
        self.N = len(text)
        self.__create_suffixes()

    def longest_repeated_substring(self):
        max_lcp = 0
        suffix = None
        for i in range(1, self.N):
            prev_suffix = self.suffixes[i-1]
            current_suffix = self.suffixes[i]
            lcp = self.__lcp(prev_suffix, current_suffix)
            if lcp > max_lcp:
                max_lcp, suffix = lcp, current_suffix

        if suffix is None:
            return (0, None)
        else:
            return max_lcp, self.text[suffix:suffix+max_lcp]

    def print_debug(self):
        for i in range(len(self.suffixes)):
            print self.text[self.suffixes[i]:]

    def search(self, key):
        found = -1
        i = self.__rank(key)
        if 0 <= i <= self.N-1:
            suffix = self.text[self.suffixes[i]:]
            if suffix.startswith(key):
                found = self.suffixes[i]
        return found

    def __rank(self, key):
        i = 0
        j = self.N - 1
        while i < j:
            mid = (i + j) / 2
            comp = self.__compare_key_with_suffix(self.suffixes[mid], key)
            if comp < 0:
                i = mid + 1
            elif comp > 0:
                j = mid - 1
            else:
                return mid

        return i

    def __lcp(self, i, j):
        lcp = 0
        while i < self.N and j < self.N and self.text[i] == self.text[j]:
            lcp += 1
            i += 1
            j += 1
        return lcp

    def __create_suffixes(self):
        self.suffixes = [x for x in range(self.N)]
        self.__sort_suffixes()

    def compare_suffixes(self, i, j):
        # smaller string length results to a smaller outcome
        # the smaller the index, the larger the suffix length
        on_equal = -1*cmp(i, j)

        while i < self.N and j < self.N:
            if self.text[i] > self.text[j]:
                return 1
            elif self.text[i] < self.text[j]:
                return -1
            i += 1
            j += 1

        return on_equal

    def __compare_key_with_suffix(self, suffix, key):
        i = suffix
        j = 0
        K = len(key)
        len_comparison = cmp(self.N - i, K)

        while i < self.N and j < K:
            if self.text[i] > key[j]:
                return 1
            elif self.text[i] < key[j]:
                return -1
            i += 1
            j += 1

        # print self.text[suffix:], self.text[suffix:].startswith(key)
        return 0 if self.text[suffix:].startswith(key) else len_comparison

    def __sort_suffixes(self):

        def partition(arr, left, right):
            pivot = left
            i = left + 1
            for j in range(left + 1, right + 1):
                if self.compare_suffixes(arr[j], arr[pivot]) < 0:
                    arr[j], arr[i] = arr[i], arr[j]
                    i += 1

            arr[pivot], arr[i - 1] = arr[i - 1], arr[pivot]
            return i - 1

        def qsort_pass(arr, start, end):
            if end > start:
                pivot = partition(arr, start, end)
                qsort_pass(arr, start, pivot - 1)
                qsort_pass(arr, pivot + 1, end)

        qsort_pass(self.suffixes, 0, self.N - 1)

if __name__ == "__main__":
    arr = SuffixArray("ABRACADABRA")
    assert (4, 'ABRA') == arr.longest_repeated_substring()

    arr = SuffixArray("123123123123")
    assert (9, '123123123') == arr.longest_repeated_substring()

    moby = open("../data/mobydick.txt", 'r')
    text = moby.read()

    arr = SuffixArray(text)

    print 'Longest repeated substring: ', arr.longest_repeated_substring()

    while True:
        pattern = raw_input('Search for text: ')
        i = arr.search(pattern)
        if i < 0:
            print("Pattern not found")
        else:
            print("Found in context:")
            context = 30
            start = max(i-context, 0)
            plen = len(pattern)
            end = min(i + plen + context, len(text))
            print('...' + text[start:i] + '<b>' + text[i:i+plen] + '</b>' + text[i+plen:end] + '...')
