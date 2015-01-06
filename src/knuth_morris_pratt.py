
class KnuthMorrisPrattSearch:
    """
    Implements the Knuth-Morris-Pratt sub-string search algorithm.

    The algorithm operates in two phases. In the first phase a deterministic finite state automaton
    is built. Each state of the DFA corresponds to a character in the pattern. Also each state N is
    assigned a value M which represents the overlap between the pattern and the text in case of a
    mismatch between a character in the text and the Nth character in the pattern. The value M indicates
    us that the search should continue by comparing the next text character with the Mth character
    in the pattern.

    The second pass of the algorithm is the actual sub-string search. We scan the text in a left-to-right
    fashion consuming one text character at a time. Each text character is compared with a pattern
    character. If the characters match we advance the text and pattern pointers. While in case of a
    mismatch we offset the pattern pointer by the value indicated by the DFA and taking into account
    the text character that caused the mismatch.

    This algorithm can operate in streaming mode as it doesn't require to backup in the text in order
    to resume the search after a mismatch. This makes it ideal in cases where we cannot afford to save
    or buffer the input text.
    """
    def __init__(self, pattern):
        self.pattern = pattern
        self.M = len(pattern)
        self.dfa = {}
        self.__build_dfa()


    def contains(self, text):
        j = 0
        for c in text:
            j = self.dfa[c][j] if c in self.dfa and j in self.dfa[c] else 0

            if j == self.M:
                return True

        return False

    def __build_dfa(self):
        for p in self.pattern:
            self.dfa[p] = {}

        restart_state = 0
        p = self.pattern[0]
        self.dfa[p][0] = 1

        for i in range(1, self.M):
            c = self.pattern[i]

            # point to the restart state for all input
            for p in self.pattern:
                self.dfa[p][i] = self.dfa[p][restart_state] if restart_state in self.dfa[p] else 0

            # and to the next state in case of a match
            self.dfa[c][i] = i + 1

            # update restart state
            restart_state = self.dfa[c][restart_state] if restart_state in self.dfa[c] else 0

if __name__ == "__main__":
    substrSearch = KnuthMorrisPrattSearch("is a")
    assert substrSearch.contains("this is a message")

    substrSearch = KnuthMorrisPrattSearch("is not a")
    assert not substrSearch.contains("this is a message")

    moby = open("../data/mobydick.txt", 'r')
    text = moby.read()

    while True:
        pattern = raw_input('Search for text: ')
        substrSearch = KnuthMorrisPrattSearch(pattern)

        if substrSearch.contains(text):
            print("Pattern found")
        else:
            print("Pattern not found")
