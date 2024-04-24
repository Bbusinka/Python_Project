from typing import List, Tuple, Iterable
from sys import argv, exit, stderr
from errors import Errors, COLOURS
from math import log10
import os


def one_byte(f) -> int:
    #Odczytaj jeden bajt i zwróć go jako liczbę całkowitą.
    return ord(f.read(1))


def byte_list(f, count: int) -> Tuple[int]:
    #Odczytaj `count` bajty i zwróć ją jako krotkę liczb całkowitych.
    return tuple(int(x) for x in f.read(count))


def int_from_bytes(bytes_) -> int:
    #Oblicza liczbę całkowitą z podanych bajtów.
    output = 0
    for i in range(0, len(bytes_)):
        output += bytes_[i] * (2**(8*i))
    return output


def quantize(input_image: str, output_image: str, r_bits: int, g_bits: int, b_bits: int):

    err = Errors()

    with open(input_image, 'rb+') as fi:
        # przeczytaj pierwszą część nagłówka
        header_header = byte_list(fi, 12)
        image_width_raw = byte_list(fi, 2)
        image_width = int_from_bytes(image_width_raw)
        image_height_raw = byte_list(fi, 2)
        image_height = int_from_bytes(image_height_raw)
        # przeczytaj resztę nagłówka
        pixel_depth = one_byte(fi)
        image_descriptor = one_byte(fi)

        with open(output_image, 'wb') as fo:

            # skopiuj nagłówek nad
            fo.write(bytes(header_header))
            fo.write(bytes(image_width_raw))
            fo.write(bytes(image_height_raw))
            fo.write(bytes([pixel_depth]))
            fo.write(bytes([image_descriptor]))
            # zawijaj bity w wygodną listę
            colour_bits_count = [b_bits, g_bits, r_bits]

            # przetwarzaj piksele
            for _ in range(0, image_height):
                for __ in range(0, image_width):
                    # weź trzy bajty na każdy piksel (BGR *not* RGB)
                    pixel = byte_list(fi, 3)
                    quantized_pixel = []
                    for colour in [0, 1, 2]:
                        # ile bitów trzeba odciąć
                        shift = 8 - colour_bits_count[colour]
                        q = pixel[colour]
                        if shift > 0:
                            # usuń niepotrzebne kawałki
                            q = q >> shift
                            # aby upewnić się, że mamy średnią wartość zakresu, który pochodzi z
                            # kwantyzacja piksela dodaj jedynkę, a resztę wypełnij zerami
                            q = q << 1
                            q += 1
                            if shift > 1:
                                q = q << shift-1
                        fo.write(bytes([q]))
                        # dodaj odpowiednie wartości do SNR i MSE
                        err.register_val(pixel[colour], q, COLOURS[colour])

            # skopiuj stopkę nad
            x = fi.read(1)
            while x:
                fo.write(x)
                x = fi.read(1)

    return err


def generate_all_RGB_combinations(pixel_bits_count: int):
    #Generuje wszystkie możliwe kombinacje rozłożenia bitów we wszystkich kanałach kolorów.
    for r in range(0, pixel_bits_count+1):
        for g in range(0, pixel_bits_count+1):
            for b in range(0, pixel_bits_count+1):
                if r + g + b == pixel_bits_count:
                    yield (r, g, b)


if __name__ == '__main__':

    if len(argv) < 5:
        exit('python main.py input_file output_file bit_depth MSE v SNR')

    input_image = argv[1]
    output_image = argv[2]
    pixel_depth = int(argv[3])
    bit_spread_measure = argv[4]

    tmp_output_image = '__tmp__' + output_image

    if bit_spread_measure not in ['MSE', 'SNR']:
        exit('invalid option for bit spread measure; only „MSE” or „SNR” are allowed')

    # przejdź przez wszystkie możliwe kombinacje spreadów RGB
    rgb_combinations = generate_all_RGB_combinations(pixel_depth)

    # uruchomiamy pierwszy raz, więc mamy z czym porównać
    best_bit_spread = next(rgb_combinations)
    best_results = quantize(input_image, output_image, *best_bit_spread)


    # przejdź przez resztę wygenerowanych rozkładów bitów
    for bit_spread in rgb_combinations:
        # przechowuj go w osobnym pliku, aby nie nadpisywać najlepszego znalezionego do tej pory obrazu wyjściowego
        results = quantize(input_image, tmp_output_image, *bit_spread)
        # jeśli faktycznie jest lepiej, zamień obraz na nowo wygenerowany
        better = False
        if bit_spread_measure == 'MSE':
            # porównaj najwyższy MSE
            if max(results.calc_mse(c) for c in COLOURS) < max(best_results.calc_mse(c) for c in COLOURS):
                better = True
        else: # bit_spread_measure == 'SNR'
            # porównaj najniższy SNR
            if min(results.calc_snr(c) for c in COLOURS) > min(best_results.calc_snr(c) for c in COLOURS):
                better = True

        if better:
            best_results = results
            best_bit_spread = bit_spread
            # nadpisz istniejący plik z najlepszymi wynikami
            os.remove(output_image)
            os.rename(tmp_output_image, output_image)
            # report
            print('found a better bit spread!', str(best_bit_spread), file=stderr)

    # clean
    if os.path.exists(tmp_output_image):
        os.remove(tmp_output_image)

    # print najlepszy bit spread
    print('RGB bit spread:', str(best_bit_spread))

    # print bledy
    print('MSE   =', best_results.calc_mse(''))
    for colour in COLOURS[::-1]:
        print('MSE(' + colour[0] + ')=', best_results.calc_mse(colour))

    print('SNR   =', best_results.calc_snr(''),
          '(' + str(10 * log10(best_results.calc_snr(''))) + ' dB)')
    for colour in COLOURS[::-1]:
        print('SNR(' + colour[0] + ')=', best_results.calc_snr(colour),
              '(' + str(10 * log10(best_results.calc_snr(colour))) + ' dB)')
