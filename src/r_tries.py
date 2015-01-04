"""
Implementation of r-way.
"""
class Alphabet:

    def __init__(self, N = 256):
        self.N = N

    def size(self):
        return self.N

    def ord(self, symbol):
        pass

class LatinAlphabet(Alphabet):
    Extras = "!.,;:[]{}/*-+$%&><-_^'()=?"
    def __init__(self):
        Alphabet.__init__(self, 52 + len(LatinAlphabet.Extras))

        self.symbols_map = { }
        index = 0
        for symbol in range(ord('a'), ord('z')):
            self.symbols_map[chr(symbol)] = index
            index += 1

        for symbol in range(ord('A'), ord('Z')):
            self.symbols_map[chr(symbol)] = index
            index += 1

        extras_index = 52

        for symbol in LatinAlphabet.Extras:
            self.symbols_map[symbol] = extras_index
            extras_index += 1

    def ord(self, symbol):
        if symbol in self.symbols_map:
            return self.symbols_map[symbol]
        else:
            raise ValueError("This alphabet does not contain the given symbol: " + symbol)

class RTrie:

    class Node:
        def __init__(self, alphabet_size=32):
            self.R = alphabet_size
            self.val = None
            self.chars = [None for _ in range(self.R)]

        def is_empty(self):
            for c in self.chars:
                if c is not None:
                    return False
            return True

        def num_nodes(self):
            return 1 + sum([c.num_nodes() for c in self.chars if c is not None])

    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.R = alphabet.size()
        self.root = RTrie.Node(self.R)

    def insert(self, key, value = None):
        assert key is not None

        # values are optional, if not present use the key
        value = value if value is not None else key

        self.root = self.__insert(self.root, key, value, len(key), 0)

    def search(self, key):
        assert key is not None
        node = self.__search(self.root, key)
        return node.val if node is not None else None

    def contains(self, key):
        return self.search(key) is not None

    def remove(self, key):
        assert key is not None
        max_depth = len(key)
        depth = 0
        backstack = []
        node = self.root

        while node is not None:
            if depth == max_depth:
                node.val = None
                break
            else:
                next_symbol = self.alphabet.ord(key[depth])
                backstack.append((node, next_symbol))
                node = node.chars[next_symbol]
                depth += 1

        # Cleans up the empty nodes
        while len(backstack) > 0:
            node, symbol = backstack.pop()
            child = node.chars[symbol]
            if child.is_empty():
                node.chars[symbol] = None

    def keys_with_prefix(self, prefix):
        """
        Finds the node the corresponds to the prefix and then visits
        all the reachable nodes from that common parent.

        The code is a bit verbose because we avoid recursion in favor
        of iterations.
        """
        prefix_node = self.__search(self.root, prefix)
        if prefix_node is None:
            return []
        else:
            matches = []
            if prefix_node.val is not None:
                matches.append(prefix_node.val)

            callstack = [(prefix_node, 0)]
            while len(callstack) > 0:
                prefix_node, i = callstack.pop()
                while i < self.R:
                    c = prefix_node.chars[i]
                    i += 1
                    if c is not None:
                        if c.val is not None:
                            matches.append(c.val)
                        callstack.append((prefix_node, i))
                        prefix_node = c
                        i = 0
            return matches

    def longest_prefix_of(self, word):
        node = self.root
        max_depth = len(word)
        best_match = 0
        depth = 0
        while node is not None and depth < max_depth:
            if node.val is not None:
                best_match = depth

            next_symbol = self.alphabet.ord(word[depth])
            node = node.chars[next_symbol]
            depth += 1

        return word[0:best_match]

    def num_nodes(self):
        if self.root is None:
            return 0
        else:
            return self.root.num_nodes()

    def __search(self, node, key):
        """
        Returns the node that corresponds to the key.
        A non-None returned node doesn't mean that the key is contained
        in the Trie. If the node doesn't contain a value then the key
        is not in the Trie.
        """
        max_depth = len(key)
        depth = 0
        while node is not None:
            if depth == max_depth:
                return node
            else:
                next_symbol = self.alphabet.ord(key[depth])
                node = node.chars[next_symbol]
                depth += 1
        return None

    def __insert(self, node, key, value, max_depth, depth):
        if node is None:
            node = RTrie.Node(self.R)

        if depth == max_depth:
            node.val = value
        else:
            next_symbol = self.alphabet.ord(key[depth])
            node.chars[next_symbol] = self.__insert(node.chars[next_symbol], key, value, max_depth, depth + 1)
        return node

if __name__ == '__main__':
    trie = RTrie(LatinAlphabet())
    assert trie.num_nodes() == 1

    trie.insert('hello', 'world!')
    assert trie.num_nodes() == len('hello') + 1
    assert trie.search('hello') == 'world!'

    trie.remove('hello')
    assert trie.num_nodes() == 1

    trie.insert("hell")
    assert trie.search("hell") is not None

    trie.insert("help")
    assert trie.search("help") is not None
    assert trie.search("hell") is not None

    trie.insert("hello")
    assert trie.search("hello") is not None

    trie.insert("helios")
    assert trie.search("helios") is not None

    keys = trie.keys_with_prefix('hel')
    assert len(keys) == 4

    keys = trie.keys_with_prefix('hell')
    assert len(keys) == 2
    
    keys = trie.longest_prefix_of("hello!")
    assert "hello" == keys
