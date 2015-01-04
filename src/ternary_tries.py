
class TernaryTrie:
    """
    An implementation of a ternary trie. Each trie node has a symbol, a value and 3 links corresponding
    to symbols less, equal or greater than the symbol of the node.
    The root node of the trie has multiple links, one for each initial letter of the symbols in the trie.

    Search is similar as in a binary search tree, at each step we compare the current character of
    the key with the key of the node and we then follow the appropriate link according to the result
    of the comparison. Whenever we match a character with a key, we advance to the next character
    of the substring we are looking for. A successful search ends by matching the last character
    of the substring with the key of a node that has a non null value.

    The running time is Theta(lnN) for search misses, where N is the number of keys in the trie.
    For successful searches the running time is Theta(|M|) where M is the pattern we are looking for.
    """

    class Node:
        """
        A node of a ternary trie contains a key (a single character), a value (for nodes that
        correspond to actual words) and links to nodes with keys less & greater than the key
        of the current node. There's also a link, self.equal, that is used when the key of the
        node matches the character of the substring and there are more characters in the substring
        to examine.
        """
        def __init__(self, key, value=None):
            self.key = key
            self.value = value
            self.less = None
            self.equal = None
            self.greater = None

        def is_empty(self):
            return self.less is None and self.equal is None and self.greater is None

        def num_nodes(self):
            size = 1
            size += self.less.num_nodes() if self.less is not None else 0
            size += self.equal.num_nodes() if self.equal is not None else 0
            size += self.greater.num_nodes() if self.greater is not None else 0
            return size

    def __init__(self):
        self.links = {}

    def __get_start_node(self, key):
        k = key[0]
        if k not in self.links:
            self.links[k] = TernaryTrie.Node(k)
        return self.links[k]

    def insert(self, key, value=None):
        k = key[0]
        value = value if value is not None else key
        if len(key) == 1:
            self.links[k] = TernaryTrie.Node(key, value)
        else:
            start_node = self.__get_start_node(key)
            self.links[k] = self.__insert(start_node, key, value)

    def __insert(self, node, key, value):
        k = key[0]
        if node is None or node.key == k:
            if node is None:
                node = TernaryTrie.Node(k)

            if len(key) == 1:
                node.value = value
            else:
                node.equal = self.__insert(node.equal, key[1:], value)
        elif node.key > k:
            node.less = self.__insert(node.less, key, value)
        else:
            node.greater = self.__insert(node.greater, key, value)

        return node

    def search(self, key):
        node = self.__get_start_node(key)
        if len(key) > 1:
            node = self.__search(node, key)
        return node.value if node is not None else None

    def contains(self, key):
        return self.search(key) is not None

    def __search(self, node, key):
        if node is None:
            return None

        k = key[0]
        if len(key) == 1 and node.key == k:
            return node
        else:
            if node.key > k:
                return self.__search(node.less, key)
            elif node.key == k:
                return self.__search(node.equal, key[1:])
            elif node.key < k:
                return self.__search(node.greater, key)

    def remove(self, key):
        k = key[0]
        start_node = self.__get_start_node(key)
        self.links[k] = self.__remove(start_node, key)

    def __remove(self, node, key):
        if node is None:
            return None

        k = key[0]
        if len(key) == 1 and node.key == k and node.value is not None:
            node.value = None
            return None if node.is_empty() else node
        else:
            if node.key > k:
                node.less = self.__remove(node.less, key)
            elif node.key == k:
                node.equal = self.__remove(node.equal, key[1:])
            elif node.key < k:
                node.greater = self.__remove(node.greater, key)

        if node.is_empty():
            return None

    def keys_with_prefix(self, prefix):
        start_node = self.__get_start_node(prefix)
        prefix_node = self.__search(start_node, prefix)
        if prefix_node is None:
            return []
        else:
            return self.__traverse(prefix, prefix_node, [])

    def __traverse(self, prefix, start_node, nodes):
        if start_node is None:
            return nodes

        if start_node.less is not None:
            self.__traverse(prefix, start_node.less, nodes)

        if start_node.equal is not None:
            self.__traverse(prefix, start_node.equal, nodes)

        if start_node.greater is not None:
            self.__traverse(prefix, start_node.greater, nodes)

        if start_node.value is not None and start_node.value.startswith(prefix):
            nodes.append(start_node)

        return nodes

    def longest_prefix_of(self, word):
        start_node = self.__get_start_node(word)
        return self.__longest_prefix_of(start_node, word)

    def __longest_prefix_of(self, node, word):
        last_match = None

        while node is not None:
            k = word[0]
            if node.key > k:
                node = node.less
            elif node.key == k:
                if node.value is not None:
                    last_match = node.value
                node = node.equal
                word = word[1:]
            elif node.key < k:
                node = node.greater

        return last_match

    def num_nodes(self):
        return sum([n.num_nodes() for n in self.links.values() if n is not None])


if __name__ == '__main__':
    trie = TernaryTrie()

    trie.insert('hello', 'world!')
    assert trie.num_nodes() == len('hello')
    assert trie.search('hello') == 'world!'

    trie.remove('hello')
    assert trie.num_nodes() == 0

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
