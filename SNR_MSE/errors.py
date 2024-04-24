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

    def calc_mse(self, colour: str):

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

    def calc_snr(self, colour: str):

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
