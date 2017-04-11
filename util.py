''' Name: Adit Hasan Student ID: 1459800
    Name: Quifeng Du Student ID: 1439484'''

import bitio
import huffman


def read_tree (bitreader):
    '''Read a description of a Huffman tree from the given bit reader,
    and construct and return the tree. When this function returns, the
    bit reader should be ready to read the next bit immediately
    following the tree description.

    Huffman trees are stored in the following format:
      * TreeLeafEndMessage is represented by the two bits 00.
      * TreeLeaf is represented by the two bits 01, followed by 8 bits
          for the symbol at that leaf.
      * TreeBranch is represented by the single bit 1, followed by a
          description of the left subtree and then the right subtree.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.

    Returns:
      A Huffman tree constructed according to the given description.
    '''
    #the function uses recursion to build from the bottom up
    first_bit = bitreader.readbit()
    if first_bit == 1:
        #create a tree branch
        return huffman.TreeBranch(read_tree(bitreader), read_tree(bitreader))
    else:
        second_bit = bitreader.readbit()
        if second_bit == 0:
            #reached end of tree
            return huffman.TreeLeafEndMessage()
        else:
            #create a tree leaf
            return huffman.TreeLeaf(bitreader.readbits(8))


def decompress (compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''
    #reader reads from the encoded compressed file
    reader = bitio.BitReader(compressed)
    #writer writes to a decoded uncompressed file
    writer = bitio.BitWriter(uncompressed)
    #the huffman tree read containing the decoding info
    tree = read_tree(reader)
    while True:
        current_element = huffman.decode(tree, reader)
        #when TreeLeafEndMessage is reached close file
        if current_element == None:
            break
        else:
            writer.writebits(current_element, 8)


def write_tree (tree, bitwriter):
    '''Write the specified Huffman tree to the given bit writer.  The
    tree is written in the format described above for the read_tree
    function.

    DO NOT flush the bit writer after writing the tree.

    Args:
      tree: A Huffman tree.
      bitwriter: An instance of bitio.BitWriter to write the tree to.
    '''
    #similar to read_tree, this function uses recursion
    if isinstance(tree, huffman.TreeLeafEndMessage):
        #if end of tree reached, write the end code
        bitwriter.writebits(0, 2)

    elif isinstance(tree, huffman.TreeLeaf):
        #if tree leaf reached write the corresponding code
        bitwriter.writebits(1, 2)
        bitwriter.writebits(tree.value, 8)

    elif isinstance(tree, huffman.TreeBranch):
        #if tree branch reached call write_tree from left
        #until end of tree reached
        bitwriter.writebit(1)
        write_tree(tree.left, bitwriter)
        write_tree(tree.right, bitwriter)


def compress (tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    #reader reads from the decoded uncompressed file
    reader = bitio.BitReader(uncompressed)
    #writer writes to a encoded compressed file
    writer = bitio.BitWriter(compressed)
    #intialize the table
    table = huffman.make_encoding_table(tree)
    #write the tree to file
    write_tree(tree, writer)

    while True:
        #read the encoded bits from table and write to file
        try:
            original_bits = reader.readbits(8)
            encoded_bits = table[original_bits]
            for i in encoded_bits:
                writer.writebit(i)
        #when end of file reached, write the end code and pad
        #the remaining bits with 0 to complete the byte
        except EOFError:
            encoded_bits = table[None]
            for j in encoded_bits:
                writer.writebit(j)
            remaining_bits = writer.bcount%8
            writer.writebits(0, remaining_bits)
            writer.flush()
            break
