import queue
from numpy import save


# A function to do pre order tree traversal on the huffman tree to find the code words
def build_codetable(root, code, code_table):
    if root is not None:
        # when reaching a leaf value store its code word in the dictionary
        if root.value is not None:
            code_table[root.value] = code
        # Then recur on left child and append a 0 to the code
        build_codetable(root.left, code + "0", code_table)
        # Finally recur on right child and append a 1 to the code
        build_codetable(root.right, code + "1", code_table)


def bitstring_to_bytes(s):
    # convert bitstring to an integer then convert the integer to a byte.
    #    int(input, base)        to_bytes(len, big endian)
    return int(s, 2).to_bytes(1, byteorder='big')


def huff_encode(input_list, code_table, filename):
    freq = {}

    # Construct frequency array
    for ch in input_list:
        if ch in freq.keys():
            freq[ch] = freq[ch] + 1
        else:
            freq[ch] = 1

    # find the probability
    prob = {}

    for ch in freq.keys():
        prob[ch] = freq[ch] / len(input_list)

    # make a class for nodes

    class Node:
        def __init__(self, value, weight, right, left):
            self.value = value
            self.weight = weight
            self.right = right
            self.left = left

    queue1 = queue.PriorityQueue()

    # counter is used to prevent errors due to the nearly similar values of probability when inserting
    # in the priority queue
    counter = 0

    # add leaf nodes to the queue
    for ch in prob.keys():
        node1 = Node(ch, prob[ch], None, None)
        counter = counter + 1
        queue1.put((node1.weight, counter, node1))

    # build huffman tree
    while len(queue1.queue) > 1:
        counter = counter + 1

        min1 = queue1.get()
        min2 = queue1.get()

        new_node = Node(None, min1[0] + min2[0], min1[2], min2[2])
        queue1.put((new_node.weight, counter, new_node))

    # generating code table
    # building the code table
    build_codetable(queue1.queue[0][2], "", code_table)

    # encoding
    # prepare binary string
    coded_string = ""

    for ch in input_list:
        coded_string = coded_string + code_table[ch]

    # store the coded file in a file
    # if the length of the coded file is not a multiple of 8 append zeroes at the end so that it becomes a multiple of 8
    number_of_extra_bits = 8 - (len(coded_string) % 8)
    if number_of_extra_bits != 8:
        for i in range(number_of_extra_bits):
            coded_string = coded_string + '0'

    binary_string = b""
    # append all the bits of code words as a string of (bytes) where the number of bits will always be a multiple of 8
    a = int(len(coded_string) / 8)
    for i in range(a):
        binary_string = binary_string + bitstring_to_bytes(coded_string[(8*i):(i*8)+8])

    # encode the number of extra zeroes appended at the end of
    # the file and write it as the first byte for decoding purpose
    binary_string = number_of_extra_bits.to_bytes(1, byteorder='big') + binary_string

    save(filename, binary_string)
    return binary_string


