from scipy.misc import imread
import bsc_functions as bsc
import numpy as np

# glowna funkcja programu
def main():
    print ("Podaj prawdopodobienstwo bledu (0-100): ")
    fault_prob = int(input())

    img = imread("zdjecie.png", True, 'L')  # odczyt obrazu 
    bits = bsc.imageToBitArray(img)         # konwersja na tablicę bitów

    result = bsc.hamminging(bits)
    bits_errors = bsc.generateErrors(result, fault_prob, 30)

    result2 = bsc.rehamminging(bits_errors)

    # print(len(result))
    incorrect_bits_rate, incorrect_byte_rate = bsc.countErrors(bits, result2)

    print("Procent prawidlowo przeslanych pikseli (ciag 8 bajtow): %.3f%%" %incorrect_byte_rate)
    print("Procent prawidlowo przeslanych bitów: %.3f%%" %incorrect_bits_rate)
    xbytes = bsc.bitsToBytes(result2)
    bsc.bytesToImg(xbytes, 'wynik.png')

main()