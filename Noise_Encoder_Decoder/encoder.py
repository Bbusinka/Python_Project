from sys import exit, argv
from utilities import *

# deklaracja podstawowa (czyli jak w kodzie Humminga (7,4)) indeksy bitów parzystości
BASIC_PARITY_DEFINITION = [
    [1, 2, 4],
    [1, 3, 4],
    [2, 3, 4]
]


def encode(block: int) -> int:
    """Koduje pojedynczy 4-bitowy blok w 8-bitowy blok kodowany przez szum.
     """
    output = 0

    # oblicz wszystkie podstawowe bity parzystości
    basic_parity = [
        sum([get_nth_bit(block, n) for n in parity_def]) % 2
        for parity_def in BASIC_PARITY_DEFINITION
    ]

    # złóż pierwsze siedem bitów
    # p_1 do p_2 parytet podstawowy
    for i in range(0, 2):
        output += basic_parity[i]
        output <<= 1
    # i_1
    output += get_nth_bit(block, 1)
    output <<= 1
    # p_3
    output += basic_parity[2]
    output <<= 1
    # od i_2 do i_4
    for i in range(2, 4+1):
        output += get_nth_bit(block, i)
        output <<= 1

    # oblicz ostatni bit parzystości
    output += sum([
        get_nth_bit(output, n, blocksize=8)
        for n in range(1, 7+1)]
    ) % 2

    return output


if __name__ == "__main__":

    if len(argv) < 3:
        exit('python encoder.py input_file output_file')

    input_file = argv[1]
    output_file = argv[2]

    with open(input_file, 'rb+') as fi, open(output_file, 'wb+') as fo:
        # przeczytaj jeden bajt
        inp = fi.read(1)
        while inp:

            inp = ord(inp)

            # podziel ten bajt na dwie 4-bitowe części
            part_one = inp >> 4
            part_two = inp & 0b1111

            # zakoduj dwa bloki i zapisz je
            fo.write(bytes([encode(part_one)]))
            fo.write(bytes([encode(part_two)]))

            inp = fi.read(1)
