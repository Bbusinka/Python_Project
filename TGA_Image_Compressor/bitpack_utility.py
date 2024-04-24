# Odczytywanie poszczególnych bajtów lub paczek bitów o innych rozmiarach niż size=8


from bitwiseio import BitReader
from typing import Tuple


def one_bitpack(f: BitReader, size: int = 8) -> int:
    """Odczytuje serię bitów `size` i zwraca ją jako liczbę całkowitą.
     Domyślnie pakiet bitów ma rozmiar 8 bitów (jeden bajt).
     Ta funkcja oczekuje `BitReader`, który odczytuje pojedyncze bity, a nie bajty.
     """
    return f.readbits(size)


def bitpack_list(f: BitReader, count: int, size: int = 8) -> Tuple[int]:
    """Czyta `count` pakiety bitów i zwraca je jako krotkę liczb całkowitych.
     Domyślnie bajty.
     Ta funkcja oczekuje `BitReader`, który odczytuje pojedyncze bity, a nie bajty.
     """
    return tuple(one_bitpack(f, size=size) for _ in range(count))


def int_from_bytes(bytes_) -> int:
    """Oblicza liczbę całkowitą z podanych bajtów.
     """
    output = 0
    for i in range(0, len(bytes_)):
        output += bytes_[i] * (2**(8*i))
    return output