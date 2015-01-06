class BoyerMooreSearch:
    """
    Tries to match the pattern by scanning the text in a left-to-right fashion
    and the pattern in a right-to-left fashion trying to benefit from the fact
    that a mismatch will allows us to skip up M characters, where M is the length
    of the pattern.

    To know how many characters we can skip after a mismatch, we use a precomputed
    array of offsets. There's one entry in the array per character in the alphabet.

    Algorithm:

    Scan through the text in a left-to-right fashion
    Scan through the pattern in a right-to-left fashion
        Compare the text character with the pattern character
            If they are equal
                advance the text pointer by 1 and reduce the pattern pointer by one
            If they are not equal and the text character does not appear in the pattern
                advanced the text pointer by one
                reset the pattern point to |M|
            If they are not equal and the text character appears in the pattern
                advance the text pointer by the precomputed offset for that pattern position
                reset the pattern point to |M|
    """

    def contains(self, text, pattern):
        offsets = self.__precompute_offsets(pattern)
        N = len(text)
        M = len(pattern)
        i = 0
        j = M - 1
        while i < N - M:
            while j >= 0:
                t = text[i + j]
                # if mismatch, check if the mismatched character appears in the pattern
                # in that case, use the precomputed offset to advance the text pointer
                # otherwise just advance one position
                if pattern[j] != t:
                    if t in offsets:
                        skip = j - offsets[t]
                        if skip > 0:
                            # the text cannot match the pattern for at least skip characters
                            i += skip
                        else:
                            i += 1
                    else:
                        i += 1
                    j = M - 1
                    break

                j -= 1

            if j < 0:
                return i
        return -1

    def __precompute_offsets(self, pattern):
        offsets = {}
        for i in range(len(pattern)):
            c = pattern[i]
            offsets[c] = pattern.rindex(c)

        return offsets

if __name__ == "__main__":
    substrSearch = BoyerMooreSearch()
    assert substrSearch.contains("this is a message", "is a") >= 0
    assert substrSearch.contains("this is a message", "is not a") < 0

    moby = open("../data/mobydick.txt", 'r')
    text = moby.read()

    while True:
        pattern = raw_input('Search for text: ')
        i = substrSearch.contains(text, pattern)
        if i < 0:
            print("Pattern not found")
        else:
            print("Found in context:")
            context = 30
            start = max(i-context, 0)
            end = min(i + len(pattern) + context, len(text))
            print('...' + text[start:end] + '...')
