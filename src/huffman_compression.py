"""
The key idea of Huffman compression is to represent the most frequently occurring symbols with the shortest possible
bit strings. The Huffman algorithm builds an optimal prefix-free code, i.e. there's no other prefix-free code that
can encode the input with fewer bits.

The algorithm tries to assign a variable and prefix-free code to each symbol, i.e. no code is a prefix of any of the
other codes. This allows us to interpret a compressed bit stream in a unique way without the need of separators between
the bit strings of the symbols.

The encoding of each symbol is represented by a trie. The code for each character corresponds to the path from the root
of the trie to the node containing the character. Left links correspond to a 0 while right links correspond to a 1.

The construction works in 2 passes. In the first pass we scan through the whole input and calculate the frequency of
each input symbol. The second pass constructs the trie in an iterative bottom-up fashion. In pseudo-code:

    Construct a trie node for each input symbol
    While there are 2 or more nodes to process
        Pick the 2 nodes x and y with the smallest frequencies
        Create a new node P and parent it to x and y with a frequency P.freq = x.freq + y.freq
        Insert P in the set of nodes to process

As a result of the construction process, all symbols end-up in leaf nodes and thus have prefix-free codes. Additionally,
nodes with low frequencies end up far down in the trie, and nodes with high frequencies end up near the root of the trie.

When we compress an input text we must also include the trie representation in the output so that the expansion
process can work. The method to serialise the trie goes as follows:

    Traverse the trie in a pre-order mode
    When you encounter an internal node, output a 0 bit
    When you encounter a leaf node, output a 1 bit followed by the character of the leaf

Then the compressed output is built simply by scanning through the input and replacing each symbol with its bitstring.

The trie de-serialisation process goes as follows:
    While there are bits to read
    Read a bit
        If a bit is a 1
            Read a character from the input and create a new leaf Node with that character
        Else
            Create an internal node and recursively read its left and right subtrees

The expansion process starts after de-serialising the trie and continues by reading every bit of the compressed
output.

    We traverse the tree for every bit read from the input until we reach a leaf.
    At that point we output the character of the leaf to the output
    We reset the tree node back to the root and continue with the rest bits in the input.

"""
from priority_queue import PriorityQueue
from bitarray import bitarray
import struct
import math


class Huffman:
    class Node:
        def __init__(self, symbol, freq=0, left=None, right=None):
            self.symbol = symbol
            self.freq = freq
            self.left = left
            self.right = right

        def is_leaf(self):
            return self.left is None and self.right is None

        def __cmp__(self, other):
            return cmp(self.freq, other.freq)

        def __hash__(self):
            return hash(self.symbol) * 17 + hash(self.freq)

    def __init__(self, filename):
        self.filename = filename

        # maps symbols to their frequencies
        self.frequencies = {}

        # the root node of the binary trie
        self.trie = None

        self.num_tries_nodes = 0

        # maps symbols to their bit-stream representation
        self.encoding_map = {}

    def compress(self, output_filename):
        self.__calculate_frequencies()
        self.__construct_trie()
        self.__build_encoding_map()
        self.__serialise_trie(output_filename)
        self.__encode_input(output_filename)

    def expand(self, output_filename):
        with open(self.filename, 'rb') as input_file:
            bit_stream = self.__deserialise_trie(input_file)
            self.__decode_input(bit_stream, input_file, output_filename)

    def __calculate_frequencies(self):
        """
        Builds a histogram of the bytes in the input file
        """
        frequencies = {}
        with open(self.filename, 'rb', 4096) as input_file:
            while True:
                input_byte = input_file.read(1)

                if not input_byte:
                    break

                if input_byte not in frequencies:
                    frequencies[input_byte] = 0

                frequencies[input_byte] += 1

        self.frequencies = frequencies

    def __construct_trie(self):
        queue = PriorityQueue.heapify([Huffman.Node(k, v) for (k, v) in self.frequencies.items()])

        self.num_tries_nodes = queue.size()

        while queue.size() > 1:
            x = queue.del_min()
            y = queue.del_min()
            parent = Huffman.Node(0, x.freq + y.freq, x, y, )
            queue.insert(parent)

            self.num_tries_nodes += 1

        self.trie = queue.del_min()

    def __build_encoding_map(self):

        # a sentinel element which indicates that we must pop
        # the last value in bit_trace
        POP = 1

        # argument stack for the next node to process
        node_stack = [self.trie]

        # argument stack for the bit trace of the next node to process
        bit_trace = [bitarray()]

        while len(node_stack) > 0:

            node = node_stack.pop()

            if node is POP:
                bit_trace.pop()
                continue

            # for internal nodes we recurse into their children
            # for leaf nodes, we have the final bit-stream and we insert
            # it into the encoding map
            if node.symbol == 0:

                parent_bit_trace = bit_trace[-1]

                node_stack.append(POP)

                if node.right is not None:
                    right_bit_trace = bitarray(parent_bit_trace)
                    right_bit_trace.append(True)
                    bit_trace.append(right_bit_trace)
                    node_stack.append(node.right)

                if node.left is not None:
                    left_bit_trace = bitarray(parent_bit_trace)
                    left_bit_trace.append(False)

                    bit_trace.append(left_bit_trace)
                    node_stack.append(node.left)


            else:
                bit_stream = bit_trace.pop()
                self.encoding_map[node.symbol] = bit_stream


    def __serialise_trie(self, output_filename):
        """
            Traverse the trie in a pre-order mode
                When you encounter an internal node, output a 0 bit
                When you encounter a leaf node, output a 1 bit followed by the character of the leaf
        """
        trie_bits = bitarray()

        # used as a stack
        node_stack = [self.trie]

        while len(node_stack) > 0:

            node = node_stack.pop()

            if node.symbol == 0:
                trie_bits.append(False)

                # process first left and then right
                node_stack.append(node.right)
                node_stack.append(node.left)

            else:
                symbol_bits = bitarray()
                symbol_bits.frombytes(node.symbol)
                trie_bits.append(True)
                trie_bits.extend(symbol_bits)

        with open(output_filename, "wb+") as of:
            of.write(struct.pack("<i", len(trie_bits)))
            trie_bits.tofile(of)


    def __encode_input(self, output_filename):
        """
        Encodes the input as a compressed bit array and writes it in the output file.
        The format of the output is: <int4: number of encoded bits> <array of bits padded to multiple of 8>
        """
        with open(output_filename, 'ab+') as of:
            bit_stream = bitarray()

            with open(self.filename, 'rb', 4096) as input_file:

                # read bytes on a one-by-one basis
                while True:

                    input_byte = input_file.read(1)

                    if not input_byte:
                        break

                    assert input_byte in self.encoding_map

                    bit_stream.extend(self.encoding_map[input_byte])
                    assert bit_stream is not None

            num_input_bits = len(bit_stream)

            print 'encoded', num_input_bits, 'bits'

            # writes number of bits followed by the actual bits
            of.write(struct.pack(">i", num_input_bits))
            bit_stream.tofile(of)


    def __deserialise_trie(self, input_file):
        """
        While there are bits to read
        Read a bit
            If a bit is a 1
                Read a character from the input and create a new leaf Node with that character
            Else
                Create an internal node and recursively read its left and right subtrees
        """

        def read_node(bit_stream):
            """
            Helper recursive function for reading nodes from a bit stream.
            """
            if len(bit_stream) == 0:
                return (bit_stream, None)

            if bit_stream.pop(0):
                symbol = bit_stream[0:8].tobytes()
                bit_stream = bit_stream[8:]
                leaf_node = Huffman.Node(symbol)
                return (bit_stream, leaf_node)

            else:
                internal_node = Huffman.Node(0)
                bit_stream, internal_node.left = read_node(bit_stream)
                bit_stream, internal_node.right = read_node(bit_stream)

                return (bit_stream, internal_node)


        # struct.unpack always returns a tuple, take the first elements
        num_trie_bits = struct.unpack("<i", input_file.read(4))[0]

        trie_bytes = int(math.ceil(num_trie_bits / 8.0))
        padding_bits = trie_bytes * 8 - num_trie_bits

        bit_stream = bitarray()
        bit_stream.fromfile(input_file)

        self.num_tries_nodes = 0
        bit_stream, self.trie = read_node(bit_stream)

        print self.num_tries_nodes

        # skip padding
        bit_stream = bit_stream[padding_bits:]

        return bit_stream

    def __decode_input(self, bit_stream, input_file, output_filename):
        """
        We traverse the tree for every bit read from the input until we reach a leaf.
        At that point we output the character of the leaf to the output
        We reset the tree node back to the root and continue with the rest bits in the input.

        As an implementation node, we reverse the bits of the bitarray in order to use
        bitarray.pop() instead of bitarray.pop(0). The format has a O(1) cost while the
        latter has a O(N) cost and leads to a huge number of allocations.
        """
        with open(output_filename, "wb+", 4096) as of:

            # parse the number of encoded bits header
            if len(bit_stream) < 32:
                bit_stream.frombytes(self.__read_bytes(input_file, 32))

            if len(bit_stream) < 32:
                raise AssertionError("EOF while parsing the header")

            bit_stream.reverse()

            num_encoded_bits = 0
            for i in range(0, 32):
                num_encoded_bits = (num_encoded_bits << 1) | bit_stream.pop()

            print num_encoded_bits, 'encoded bits'

            processed_bits = 0

            while processed_bits < num_encoded_bits:

                # symbol decoding loop, starts from the root until it encounters a leaf
                node = self.trie

                while node.symbol == 0:

                    if len(bit_stream) == 0:
                        # read more bytes from file and append to bit_stream
                        bit_stream.frombytes(self.__read_bytes(input_file))
                        bit_stream.reverse()

                    # EOF while decoding
                    if len(bit_stream) == 0:
                        raise AssertionError("EOF while still decoding input")

                    if bit_stream.pop():
                        node = node.right
                    else:
                        node = node.left

                    processed_bits += 1

                assert node is not None
                assert node.symbol is not None

                of.write(node.symbol)

    def __read_bytes(self, file_obj, buffer_size=32):
        """
        Helper method to read a chunk of bytes from a file object.
        Returns the read bytes as a byte string
        """
        b = file_obj.read(1)
        buffer = bytearray()
        while b:
            buffer.append(b)
            if len(buffer) == buffer_size:
                break
            b = file_obj.read(1)

        return str(buffer)


if __name__ == "__main__":

    import cProfile

    huff = Huffman("../data/mobydick.txt")
    cProfile.run('huff.compress("moby.huff")')

    huff = Huffman("../data/moby.huff")
    cProfile.run('huff.expand("../data/mobydick_expanded.txt")')

    with open("../data/mobydick.txt", 'r') as moby:
        original_text = moby.read()

    with open("../data/mobydick_expanded.txt", 'r') as moby_expanded:
        expanded_text = moby_expanded.read()

    assert expanded_text == original_text
