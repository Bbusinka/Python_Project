from sys import argv, exit
from typing import List
import math


class Node(object):

    def __init__(self, parent, weight=0, left=None, right=None, char=''):
        self._parent = parent
        self._weight = weight
        self._left = left
        self._right = right
        self._char = char

    @property
    def parent(self): return self._parent
    @parent.setter
    def parent(self, new_parent): self._parent = new_parent 

    @property
    def weight(self): return self._weight
    @weight.setter
    def weight(self, new_weight): self._weight = new_weight

    @property
    def left(self): return self._left
    @left.setter
    def left(self, new_left): self._left = new_left

    @property
    def right(self): return self._right
    @right.setter
    def right(self, new_right): self._right = new_right

    @property
    def char(self): return self._char
    @char.setter
    def char(self, new_char): self._char = new_char

    def is_leaf(self):
        return self._left is None and self._right is None


class HuffmanCoding(object):
    def __init__(self):
        self._NYT = Node(None, 0, char='NYT')
        self._root = self._NYT
        self._all_chars: List[Node] = [None] * 256
        self._all_nodes_sorted: List[Node] = []

    def _is_already_added(self, char: str):
        if ord(char) > 255:
            raise Exception('IndexError: >256')

        if self._all_chars[ord(char)] is not None:
            return True
        return False

    def _register_char(self, char: str):
        curr = self._all_chars[ord(char)]

        if curr is None:
            nyt = self._NYT
            old_nyt_parent = nyt.parent

            new_parent = None

            if old_nyt_parent is None:
                self._root = Node(None, left=nyt, right=None)
                nyt.parent = self._root
                new_parent = self._root
            else:
                new_parent = Node(old_nyt_parent, weight=1,
                                  left=nyt, right=None)
                old_nyt_parent.left = new_parent
                nyt.parent = new_parent

            new_node = Node(new_parent, weight=1, char=char)
            new_parent.right = new_node

            self._all_nodes_sorted.append(new_node)
            self._all_nodes_sorted.append(new_parent)

            self._all_chars[ord(char)] = new_node

            curr = new_parent.parent

        while curr is not None:
            to_swap = None
            for n in self._all_nodes_sorted:
                if n.weight == curr.weight:
                    to_swap = n
                    break

            if curr is not to_swap and curr is not to_swap.parent and to_swap is not curr.parent:
                self._swap_nodes(curr, to_swap)

            curr.weight += 1
            curr = curr.parent

    def _swap_nodes(self, one: Node, two: Node):
        one_index = self._all_nodes_sorted.index(one)
        two_index = self._all_nodes_sorted.index(two)

        self._all_nodes_sorted[one_index], self._all_nodes_sorted[
            two_index] = self._all_nodes_sorted[two_index], self._all_nodes_sorted[one_index]

        parent = one.parent
        one.parent = two.parent
        two.parent = parent

        if one.parent.left is two:
            one.parent.left = one
        else:
            one.parent.right = one

        if two.parent.left is one:
            two.parent.left = two
        else:
            two.parent.right = two

    def _get_node_code(self, _node: Node):
        code = ''
        node = _node
        while node.parent is not None:
            p = node.parent
            if p.left is node:
                code += '0'
            else:  # p.right is node
                code += '1'
            node = p
        return code[::-1]

    def _get_code(self, char: str):
        if self._is_already_added(char):
            node = self._all_chars[ord(char)]
            return self._get_node_code(node)
        else:
            return self._get_node_code(self._NYT) + bin(ord(char))[2:].zfill(8)

    def encode_single_character(self, char: str) -> str:
        code = self._get_code(char)
        self._register_char(char)
        return code

    def decode(self, encoded: str) -> List[int]:
        output = []

        first_char = chr(int(encoded[:8], 2))

        output.append(ord(first_char))

        self._register_char(first_char)

        node = self._root

        i = 8
        while i < len(encoded):
            curr = encoded[i]

            if curr == '0':
                node = node.left
            elif curr == '1':
                node = node.right
            else:
                raise Exception("Niepoprawny kod Huffmana (tylko 0 lub 1)")

            char = node.char

            if char:
                if char == 'NYT':
                    char = chr(int(encoded[i+1:i+9], 2))
                    i += 8
                output.append(ord(char))
                self._register_char(char)
                node = self._root

            i += 1

        return output

    def get_avg_code_length(self):
        lengths = []
        count = 0

        for char in self._all_chars:
            if char is None:
                continue
            lengths.append(len(self._get_node_code(char)))
            count += 1
        if count == 0:
            count += 1
        return sum(lengths) / count

    def get_entropy(self):
        output = 0

        for char in self._all_chars:
            if char is None:
                continue
            output += char.weight * (-math.log2(char.weight))
        if self._root.weight == 0:
            self._root.weight += 1

        output /= self._root.weight

        return output + math.log2(self._root.weight)


if __name__ == "__main__":
    args = argv[1:]

    if len(args) < 3:
        print("HelpToRun: main.py input_file output_file -k/-d (-k dla kodowania, -d dla dekodowania)")
        exit("RunError: zle wprowadzone argumenty")

    input_file = args[0]
    output_file = args[1]
    mode = args[2]

    huffman = HuffmanCoding()

    if mode == "-d":
        with open(output_file, "wb+") as fo:
            with open(input_file, "rb") as fi:
                input_bits = ""
                tmp = fi.read(1)
                padding_used = ord(tmp)

                tmp = fi.read(1)
                while tmp:
                    tmp = ord(tmp)
                    for i in range(0, 8):
                        if (tmp >> (7-i)) & 0b1:
                            input_bits += '1'
                        else:
                            input_bits += '0'
                    tmp = fi.read(1)

                input_bits = input_bits[:-padding_used]

                bytes_ = huffman.decode(input_bits)
                for b in bytes_:
                    fo.write(b.to_bytes(1, byteorder="big"))

                print('Dekodowanie zakonczylo sie sukcesem')

    else:
        with open(output_file, "wb+") as fo:
            with open(input_file, "rb") as fi:
                output = ""
                byte = fi.read(1)
                count = 1
                while byte:
                    output += huffman.encode_single_character(byte)
                    byte = fi.read(1)
                    count += 1

                output_bytes = []
                padding_used = 0
                for i in range(0, math.ceil(len(output)/8)):
                    tmp = output[(i*8):((i+1)*8)]
                    if len(tmp) != 8:
                        padding_used = 8-len(tmp)
                        tmp += "0" * padding_used
                    tmp = int(tmp, 2)
                    output_bytes.append(tmp)
                output_bytes = [padding_used] + output_bytes

                for b in output_bytes:
                    fo.write(b.to_bytes(1, byteorder='big'))

                print("Entropia:  ", huffman.get_entropy())
                print("Srednia dlugosc:  ", huffman.get_avg_code_length())
                print("Poziom kompresji:  ", count/len(output_bytes))
