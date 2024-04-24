from sys import exit, argv
from utilities import *

# deklaracja podstawowa (czyli jak w kodzie Humminga (7,4)) indeksy bitów parzystości
INTEGRITY_BITS_DEFINITION = [
    [1, 3, 5, 7],
    [2, 3, 6, 7],
    [4, 5, 6, 7]
]
# uwaga: kolumny są tutaj reprezentowane poziomo, a nie pionowo
PARITY_CHECK_MATRIX = [
    [],  # fikcyjna kolumna, aby zachować globalną regułę rozpoczynania indeksów od 1
    [1, 0, 0, 1],
    [0, 1, 0, 1],
    [1, 1, 0, 1],
    [0, 0, 1, 1],
    [1, 0, 1, 1],
    [0, 1, 1, 1],
    [1, 1, 1, 1],
    [0, 0, 0, 1]
]


def decode(block: int) -> (int, bool):
    """Koduje pojedynczy 8-bitowy blok słowa kodowego szumiącego z powrotem do
     oryginalny 4-bitowy blok. Zwraca oryginalny blok i wartość logiczną
     równa True, jeśli wystąpiły dwa błędy, których nie można naprawić.
     """
    # oblicz podstawowy syndrom
    basic_syndrome = [
        sum([get_nth_bit(block, n, blocksize=8) for n in integrity_def]) % 2
        for integrity_def in INTEGRITY_BITS_DEFINITION
    ]

    # oblicz syndrom parzystości
    parity_syndrome = sum([get_nth_bit(block, n, blocksize=8)
                           for n in range(1, 8+1)]) % 2

    bit_to_fix_index = 0
    uncorrectable_error = False

    if sum(basic_syndrome) != 0 and parity_syndrome == 1:
        # słowo kodowe jest niepoprawne - poprawka na podstawie wyniku syndromu podstawowego
        bit_to_fix_index = PARITY_CHECK_MATRIX.index(basic_syndrome + [parity_syndrome])
    elif sum(basic_syndrome) == 0 and parity_syndrome == 1:
        # słowo kodowe jest nieprawidłowe - naprawiono na podstawie wyniku syndromu parzystości
        # (ostatni bit musi być poprawiony)
        bit_to_fix_index = 8
    elif sum(basic_syndrome) != 0 and parity_syndrome == 0:
        # słowo kodowe jest nieprawidłowe - błąd nie do naprawienia
        uncorrectable_error = True

    # najpierw popraw słowo kodowe, jeśli to konieczne
    if bit_to_fix_index > 0:
        if get_nth_bit(block, bit_to_fix_index, blocksize=8) == 1:
            block -= (1 << (8-bit_to_fix_index))
        else: # == 0
            block += (1 << (8-bit_to_fix_index))

    # usuń rzeczywisty 4-bitowy blok, który zawiera wysłane informacje
    indicies = [3, 5, 6, 7]
    output = 0
    for index in indicies:
        output += get_nth_bit(block, index, blocksize=8)
        output <<= 1

    return output >> 1, uncorrectable_error


if __name__ == "__main__":

    if len(argv) < 3:
        exit('python decoder.py input_file output_file')

    input_file = argv[1]
    output_file = argv[2]

    uncorrectable_errors = 0

    with open(input_file, 'rb+') as fi, open(output_file, 'wb+') as fo:
        # odczytaj dwa bajty do dekodowania
        inp = fi.read(2)
        while inp:
            # dekoduj dwa bajty
            inp = list(inp)
            one, error_one = decode(inp[0])
            two, error_two = decode(inp[1])
            fo.write(bytes([(one << 4) + two]))
            # zbierz wszystkie błędy
            uncorrectable_errors += int(error_one) + int(error_two)

            inp = fi.read(2)

    print('uncorrectable errors:', uncorrectable_errors)