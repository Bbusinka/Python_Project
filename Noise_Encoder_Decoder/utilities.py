def get_nth_bit(block, n, blocksize=4) -> int:
    """Zwraca n-ty bit w bloku `rozmiaru` bitu, licząc od lewej,
     indeksy bitowe zaczynają się od 1.
     """
    return block >> (blocksize-n) & 0b1
