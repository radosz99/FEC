from scipy.misc import imread
import bsc_functions as bsc
import numpy as np
import random
import cv2

#generowanie błędów modelem gilberta - zapisywanie w zależności od stanow
def gilbert_model(bit_array):
    correct_prob = 9.9
    injure_prob = 10 - correct_prob
    
    state = 1 # 1 = correct, 0 = error

    bit_error_array = []

    for x in range(0, len(bit_array)):
        #losowanie czy następuje zmiana stanu
        r = random.random()
        if (state == 1):
            if (r*100 <= injure_prob):
                state = 0
        else:
            if (r*100 <= correct_prob):
                state = 1
        #zapisywanie w zależności od aktualnego stanu
        if (state == 0):
            bit_error_array.append(int(not bit_array[x]))   # jeśli r <= prawdopodobieństwo - zapisz negację bitu
        else:
            bit_error_array.append(bit_array[x])    

    return bit_error_array




def main():
    random.seed(30)
    sum_bits = 0
    sum_bytes = 0
    img = cv2.imread("../zdjecie.png", 0)
    
    for x in range(0, 10):
        bits = bsc.imageToBitArray(img)         # konwersja na tablicę bitów
        bits_errors = gilbert_model(bits)  # generowanie błędów
        incorrect_bits_rate, incorrect_byte_rate = bsc.countErrors(bits, bits_errors)
        sum_bits += incorrect_bits_rate
        sum_bytes += incorrect_byte_rate

    sum_bits = sum_bits / 10
    sum_bytes = sum_bytes / 10

    print("Procent prawidlowo przeslanych pikseli (ciag 8 bitów): %d / 59200" %sum_bytes)
    print("Procent prawidlowo przeslanych bitów: %d / 473600" %sum_bits)

main()