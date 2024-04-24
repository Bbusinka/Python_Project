# nagłówki i stopki plików

from bitwiseio import BitReader, BitWriter
from bitpack_utility import *


def read_and_write_tga_header(reader: BitReader, writer: BitWriter):
    """Odczytuje nagłówek TGA z otwartego pliku wejściowego i zapisuje go do
     program do zapisywania plików wyjściowych.
     """
    # przeczytaj pierwszą część oryginalnego nagłówka
    header_header = bitpack_list(reader, 12)
    image_width_raw = bitpack_list(reader, 2)
    image_width = int_from_bytes(image_width_raw)
    image_height_raw = bitpack_list(reader, 2)
    image_height = int_from_bytes(image_height_raw)
    # przeczytaj resztę nagłówka
    header_the_rest = bitpack_list(reader, 2)

    # writer jest opcjonalny
    if writer is not None:
        # skopiuj oryginalny nagłówek nad
        writer.writebits(int_from_bytes(bytes(header_header[::-1])), 12 * 8)
        writer.writebits(int_from_bytes(bytes(image_width_raw[::-1])), 2 * 8)
        writer.writebits(int_from_bytes(bytes(image_height_raw[::-1])), 2 * 8)
        writer.writebits(int_from_bytes(bytes(header_the_rest[::-1])), 2 * 8)

    return image_width, image_height


def read_and_write_tga_footer(reader: BitReader, writer: BitWriter):
    """Odczytuje stopkę TGA z otwartego pliku wejściowego i zapisuje ją do
     program do zapisywania plików wyjściowych.
     """
    while reader.read:
        x = reader.readbits(8)
        writer.writebits(x, 8)