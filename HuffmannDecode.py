import queue

# levels and prob are two lists passed by the encoder where
# levels: the levels in the input_list for huffman
# prob: probability of each level in the input list


def rebuild_tree(levels, prob):
    # make a class for nodes
    class Node:
        def __init__(self, value, weight, right, left):
            self.value = value
            self.weight = weight
            self.right = right
            self.left = left

    huff_tree = queue.PriorityQueue()

    # counter is used to prevent errors due to the nearly similar values of probability when inserting
    # in the priority queue
    counter = 0

    # add leaf nodes to the queue
    for index in range(len(levels)):
        leaf = Node(levels[index], prob[index], None, None)
        counter = counter + 1
        huff_tree.put((leaf.weight, counter, leaf))

    # build huffman tree
    while len(huff_tree.queue) > 1:
        counter = counter + 1

        min1 = huff_tree.get()
        min2 = huff_tree.get()

        new_node = Node(None, min1[0] + min2[0], min1[2], min2[2])
        huff_tree.put((new_node.weight, counter, new_node))
    return huff_tree


def huff_decode(levels_list, prob_list,  coded_file, decoded_list):
    to_be_decoded_string = ""
    # we get the first byte which contains the number of extra zeroes appended at the end of the file
    extra_bits = coded_file[0]

    for byte in coded_file:
        # turn a byte into bit string using ("{0:{fill}8b}".format(byte, fill='0'))
        to_be_decoded_string = to_be_decoded_string + ("{0:{fill}8b}".format(byte, fill='0'))

    # remove the first byte and the extra zeroes to keep only the encoded text in the string
    to_be_decoded_string = to_be_decoded_string[8: len(to_be_decoded_string) - (extra_bits % 8)]

    huff_tree = rebuild_tree(levels_list, prob_list)

    current_node = huff_tree.queue[0][2]
    for bit in to_be_decoded_string:
        if bit == '0':
            current_node = current_node.left
        elif bit == '1':
            current_node = current_node.right
        # we have reached a leaf
        if current_node.value is not None:
            decoded_list.append(int(current_node.value))
            current_node = huff_tree.queue[0][2]

    print(decoded_list)
