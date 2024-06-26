from sys import exit, argv
from random import random
from utilities import *

if __name__ == "__main__":

    if len(argv) < 3:
        exit('python compare.py first_file second_file')

    file_one = argv[1]
    file_two = argv[2]

    differences = 0

    with open(file_one, 'rb+') as f1, open(file_two, 'rb+') as f2:
        # przeczytaj jeden bajt
        b1 = f1.read(1)
        b2 = f2.read(1)
        while b1 and b2:

            b1 = ord(b1)
            b2 = ord(b2)

            # porównaj dwa zestawy 4-bitowych bloków
            if (b1 >> 4) != (b2 >> 4) or (b1 & 0b1111) != (b2 & 0b1111):
                differences += 1

            b1 = f1.read(1)
            b2 = f2.read(1)

    print('differences:', differences)
