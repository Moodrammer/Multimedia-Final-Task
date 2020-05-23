from numpy import load


def huff_decode(code_table, decoded_list, coded_file):
    to_be_decoded_string = ""
    # we get the first byte which contains the number of extra zeroes appended at the end of the file
    extra_bits = coded_file[0]

    for byte in coded_file:
        # turn a byte into bit string using ("{0:{fill}8b}".format(byte, fill='0'))
        to_be_decoded_string = to_be_decoded_string + ("{0:{fill}8b}".format(byte, fill='0'))

    # remove the first byte and the extra zeroes to keep only the encoded text in the string
    to_be_decoded_string = to_be_decoded_string[8: len(to_be_decoded_string) - (extra_bits % 8)]

    codeword = ""

    # Loop on the binary string, append the bits and check for a code word in the dictionary
    # when a code word is found find its corresponding key in the dictionary & write it to the decoded file
    for bits in to_be_decoded_string:
        codeword = codeword + bits
        if codeword in code_table.values():
            for ch in code_table.keys():
                if code_table[ch] == codeword:
                    decoded_list.append(ch)
            codeword = ""
