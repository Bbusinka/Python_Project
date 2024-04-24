import sys
import math

def elias_omega(number, bit_width):
    code = "0"
    k = number
    while k > 1:
        binary_k = bin(k)[2:]
        code = binary_k + code
        k = len(binary_k) - 1
    return code

def encode(input_file, output_file, func=elias_omega):
    with open(input_file, "rb") as inp, open(output_file, "wb") as output:
        dictionary = {}
        for i in range(256):
            dictionary[chr(i)] = i

        input_bytes = inp.read()

        bitstring_output = ""
        P = chr(int.from_bytes([input_bytes[0]], "big"))
        bit_width = 9  # początkowa długość bitu do zakodowania

        for byte in input_bytes[1:]:
            C = chr(int.from_bytes([byte], "big"))

            if P + C in dictionary:
                P = P + C
            else:
                bitstring_output += func(dictionary[P], bit_width)
                dictionary[P + C] = len(dictionary)

                if len(dictionary) < 2**bit_width:
                    bit_width = max(bit_width, int(math.ceil(math.log2(len(dictionary)))))

                P = C

        bitstring_output += func(dictionary[P], bit_width)

        if (len(bitstring_output) + 3) % 8 != 0:
            pad_len = (len(bitstring_output) + 3) % 8
            bitstring_output = bin(pad_len)[2:].zfill(3) + bitstring_output + "0" * pad_len
        else:
            bitstring_output = "000" + bitstring_output

        b = bytes(int(bitstring_output[i : i + 8], 2) for i in range(0, len(bitstring_output), 8))
        output.write(b)

        for l in dictionary: print("\n",l)
        
        return b

def entropy(freq, num_of_symbols):
    H = 0
    for i in freq:
        H += freq[i] / num_of_symbols * -math.log(freq[i] / num_of_symbols, 2)
    return H

def get_freq(sth):
    freq = {}
    for symbol in sth:
        if not symbol:
            break
        if symbol in freq:
            freq[symbol] += 1
        else:
            freq[symbol] = 1
    return freq

def stats(input_file, output):
    with open(input_file, "rb") as f:
        inp = f.read()
        input_len = len(inp)
        input_freq = get_freq(inp)

    output_len = len(output)
    output_freq = get_freq(output)

    print("Input entropy: ", entropy(input_freq, input_len))
    print("Output entropy: ", entropy(output_freq, output_len))
    print("Input size: ", input_len)
    print("Output size: ", output_len)
    print("Compression ratio: ", input_len / output_len)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        res = encode(sys.argv[1], sys.argv[2], func=lambda x, y: elias_omega(x, y))
        stats(sys.argv[1], res)
    else:
        print(
            "encoder input_file output_file"
        )
