from tga_utility import *
from bitpack_utility import *
from sys import exit, argv
from math import log10

COLOURS = ['blue', 'green', 'red']


class Errors(object):
    """Oblicza błąd średniokwadratowy (MSE) i
     stosunek sygnału do szumu (SNR) obrazu.
     """

    def __init__(self):
        self._mse = dict()
        self._snr = dict()
        self._count = dict()
        for colour in COLOURS:
            self._mse[colour] = 0
            self._snr[colour] = 0
            self._count[colour] = 0

    def register_val(self, original_value: int, quantized_value: int, colour: str):
        """Podczas kwantyzacji obrazu ta metoda gromadzi wszystkie składniki sumowania.
         """
        self._mse[colour] += (original_value - quantized_value) ** 2
        self._snr[colour] += original_value ** 2
        self._count[colour] += 1

    def calc_mse(self, colour: str = ''):

        if colour in COLOURS:
            return self._mse[colour] / self._count[colour]
        else:
            # oblicz jako cały piksel
            top = 0
            bottom = 0
            for c in COLOURS:
                top += self._mse[c]
                bottom += self._count[c]
            return top / bottom

    def calc_snr(self, colour: str = ''):

        top = 0
        bottom = 0
        if colour in COLOURS:
            # (1/N) / (1/N) = 1
            top = self._snr[colour]
            bottom = self._mse[colour]
        else:
            # oblicz jako cały piksel
            for c in COLOURS:
                top += self._snr[c]
                bottom += self._mse[c]
        if bottom > 0:
            return top / bottom
        else:
            return float('inf')


if __name__ == '__main__':

    if len(argv) < 3:
        exit('python errors.py first_image second_image')

    first_image = argv[1]
    second_image = argv[2]

    err = Errors()

    with open(first_image, 'rb+') as f1:
        with BitReader(f1) as reader1:
            with open(second_image, 'rb+') as f2:
                with BitReader(f2) as reader2:

                    # przeczytaj nagłówki plików
                    first_image_width, first_image_height = read_and_write_tga_header(
                        reader1, None)
                    image_width, image_height = read_and_write_tga_header(
                        reader2, None)

                    if image_width != first_image_width or image_height != first_image_height:
                        exit('images do not have the same sizes')

                    # iteruj po wszystkich pikselach w obu plikach
                    for _ in range(image_width * image_height):
                        # odczytaj piksel z pierwszego pliku
                        pixel1 = bitpack_list(reader1, 3)
                        # odczytaj piksel z drugiego pliku
                        pixel2 = bitpack_list(reader2, 3)
                        # zarejestruj się dla każdego koloru
                        i = 0
                        for c in COLOURS:
                            err.register_val(pixel1[i], pixel2[i], c)
                            i += 1

    print('MSE   =', err.calc_mse())
    for colour in COLOURS[::-1]:
        print('MSE(' + colour[0] + ')=', err.calc_mse(colour))

    print('SNR   =', err.calc_snr(),
          '(' + str(10 * log10(err.calc_snr(''))) + ' dB)')
    for colour in COLOURS[::-1]:
        print('SNR(' + colour[0] + ')=', err.calc_snr(colour),
              '(' + str(10 * log10(err.calc_snr(colour))) + ' dB)')