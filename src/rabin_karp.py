class RabinKarpSearch:
    """
    Implements the Rabin-Karp algorithm for finding a pattern within a given text.
    It uses rolling hashing to detect possible occurrences of the pattern in an
    efficient manner.

    The running time is O(N + M) where N is the number of keys and M is the length
    of the pattern.
    """
    def __init__(self, base=65536, prime=920419813):
        self.Q = prime
        self.R = base

    def contains(self, text, pattern):
        M = len(pattern)
        RM = 1

        for i in range(M - 1):
            RM = self.R*RM % self.Q

        fingerprint = self.hash(pattern)

        N = len(text)
        h = self.hash(text[0:M])

        for i in range(M, N):
            if fingerprint == h:
                return i
            h -= (ord(text[i-M]) * RM) % self.Q
            h %= self.Q
            h = (self.R*h + ord(text[i])) % self.Q

        return -1

    def hash(self, text):
        h = 0
        for c in text:
            h = (self.R * h + ord(c)) % self.Q
        return h

if __name__ == "__main__":
    rk = RabinKarpSearch(2)
    assert rk.contains("this is a message", "is a") >= 0
    assert rk.contains("this is a message", "is not a") < 0

    moby = open("../data/mobydick.txt", 'r')
    text = moby.read()
    substrSearch = RabinKarpSearch()
    while True:
        pattern = input('Search for text: ')
        i = substrSearch.contains(text, pattern)
        if i < 0:
            print("Pattern not found")
        else:
            print("Found in context:")
            context = 30
            start = max(i-context, 0)
            end = min(i + len(pattern) + context, len(text))
            print('...' + text[start:end] + '...')