from typing import List, Tuple, Iterable
from sys import argv, exit, stderr
from getopt import getopt
from bitwiseio import BitReader, BitWriter
from bitpack_utility import *
from tga_utility import *


def add_pixels_mod(one: Tuple[int], two: Tuple[int]):
    """Dodaje wartości dwóch pikseli razem i utrzymuje je w zakresie [0,255].
     """
    return tuple(
        (one[i] + two[i]) % 256 for i in range(0, 3)
    )


def encode(input_image: str, output_file: str, bitdepth: int) -> None:
    """Koduje dany obraz do pliku w zastrzeżonym formacie
    z wyspecjalizowanym nagłówkiem nad nagłówkiem TGA oryginalnego pliku. """

    with open(input_image, 'rb+') as fi:
        with BitReader(fi) as reader:
            with open(output_file, "wb+") as fo:
                with BitWriter(fo) as writer:
                    # skopiuj oryginalny nagłówek i odczytaj wymiary obrazu
                    image_width, image_height = read_and_write_tga_header(
                        reader, writer)

                    # napisz własny nagłówek, który zawiera głębię bitową
                    writer.writebits(bitdepth, 8)

                    # rozpocznij kodowanie od \vec0
                    previous_pixel = (0, 0, 0)

                    for _ in range(image_width * image_height):
                        current_pixel = bitpack_list(reader, 3)
                        # iteruj po wszystkich kolorach
                        quantized_difference = [0 for _ in range(3)]
                        for c in range(0, 3):
                            # oblicz różnicę i skwantuj ją
                            quantized_difference[c] = \
                                (current_pixel[c] - previous_pixel[c])\
                                % 256\
                                >> (8-bitdepth)
                            # zapisz skwantyzowaną różnicę
                            writer.writebits(quantized_difference[c], bitdepth)
                            # powrót do oryginalnego rozmiaru bitowego
                            # (teraz bez zbędnych bitów)
                            quantized_difference[c] = quantized_difference[c] << (
                                8-bitdepth)

                        # zamień stary piksel na obecny
                        previous_pixel = add_pixels_mod(
                            previous_pixel, quantized_difference)

                    # skopiuj oryginalną stopkę nad
                    read_and_write_tga_footer(reader, writer)


def decode(input_file: str, output_image: str) -> None:
    """Dekoduje podany plik binarny z powrotem do oryginalnego obrazu TGA.
     Plik wejściowy musi być plikiem binarnym wygenerowanym przez funkcję `encode`.
     """

    with open(input_file, 'rb+') as fi:
        with BitReader(fi) as reader:
            with open(output_file, "wb+") as fo:
                with BitWriter(fo) as writer:

                    # skopiuj oryginalny nagłówek i odczytaj wymiary obrazu
                    image_width, image_height = read_and_write_tga_header(
                        reader, writer)

                    # przeczytaj zastrzeżony nagłówek
                    bitdepth = one_bitpack(reader)

                    # zacznij od \vec0
                    previous_pixel = (0, 0, 0)

                    for _ in range(image_height * image_width):
                        # odczytaj przesunięcie i przywróć jego oryginalny rozmiar bite
                        current_offset = tuple(map(
                            lambda x: x << (8-bitdepth),
                            bitpack_list(reader, 3, size=bitdepth)
                        ))
                        # odtwórz skwantowany piksel
                        previous_pixel = add_pixels_mod(
                            previous_pixel, current_offset)
                        # zapisz odzyskany piksel
                        for c in range(0, 3):
                            t = previous_pixel[c]
                            writer.writebits(t, 8)

                    # odzyskaj oryginalną stopkę pliku
                    read_and_write_tga_footer(reader, writer)


if __name__ == "__main__":

    raw_args = argv[1:]
    optlist, args = getopt(raw_args, '', ['mode='])

    usage_help = 'python main.py --mode (kod/dekod) input_file output_file bit_depth'

    if len(args) < 2 and len(optlist) < 1:
        exit(usage_help)

    input_file = args[0]
    output_file = args[1]
    bitdepth = None
    if len(args) >= 3:
        bitdepth = int(args[2])

    mode = None
    for opt, arg in optlist:
        if opt == '--mode':
            if arg == 'kod' and bitdepth is None:
                print('encode mode requires bit depth option')
                exit()
            elif arg == 'kod':
                mode = 'e'
            elif arg == 'dekod':
                mode = 'd'
            else:
                print('invalid --mode')
                exit(usage_help)

    if mode == 'e':
        encode(input_file, output_file, bitdepth)
    else:  # mode == 'd'
        decode(input_file, output_file)
