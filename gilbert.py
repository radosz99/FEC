from scipy.misc import imread
import bsc_functions as bsc
import numpy as np
import random
import cv2

#generowanie błędów modelem gilberta - zapisywanie w zależności od stanow
def gilbert_model(bit_array):
    p_dz = 0.9
    p_zd = 0.25
    
    state = 1 # 1 = correct, 0 = error

    bit_error_array = []
    random.seed(30)

    for x in range(0, len(bit_array)):
        #losowanie czy następuje zmiana stanu
        r = random.random()
        if (state == 1):
            if (r <= 1 - p_dz):
                state = 0
        else:
            if (r*100 <= 1 - p_zd):
                state = 1
        #zapisywanie w zależności od aktualnego stanu
        if (state == 0):
            if (r <= 0.1):
                bit_error_array.append(int(not bit_array[x]))
            else:
                bit_error_array.append(bit_array[x])
        else:
            bit_error_array.append(bit_array[x])    

    return bit_error_array




def main():
    img = cv2.imread("zdjecie.png", 0)
    bits = bsc.imageToBitArray(img)         # konwersja na tablicę bitów
    bsc.saveToFile(bits, 'start.txt')       # zapis do pliku

    bits_errors = gilbert_model(bits)  # generowanie błędów
    bsc.saveToFile(bits_errors, 'wynik.txt')                # zapis bitów z błędami do pliku

    # porównanie bitów bez błędów i tych z błędami
    incorrect_bits_rate, incorrect_byte_rate = bsc.countErrors(bsc.readFromFile('start.txt'), bsc.readFromFile('wynik.txt'))
    print("Procent prawidlowo przeslanych pikseli (ciag 8 bitów): %.3f%%" %incorrect_byte_rate)
    print("Procent prawidlowo przeslanych bitów: %.3f%%" %incorrect_bits_rate)

    xbytes = bsc.bitsToBytes(bits_errors)
    bsc.bytesToImg(xbytes, 'wynik.png')

main()