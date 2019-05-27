from scipy.misc import imread
import bsc_functions as bsc
import numpy as np
import cv2
import random

def code_7_4(bit_array):
    result = []

    G = np.array([
        [1, 1, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0],
        [1, 1, 0, 1, 0, 0, 1]
    ])

    for x in range(0, len(bit_array), 4):
        four_bits = np.array([[0, 0, 0, 0]])
        for y in range(0, 4):                       #konwertowanie tablicy do 'NumPy array'
            four_bits[0][y] = bit_array[x + y]

        data_vector = np.dot(four_bits, G) % 2      #mnożenie przez macierz generującą kod hamminga
        for y in range(0, 7):
            result.append(data_vector[0][y])        #konwersja do tablicy bitów
    return result

#dekodowanie kodu hamminga
def decode(bit_array):
    result = []

    R = np.array([
    [0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 1]
    ])

    for x in range(0, len(bit_array), 7):
        seven_bits = decodeSevenBits(bit_array[x : x + 7])      #odczytywanie każdego bajtu koloru
        output_data = np.dot(R, seven_bits.T)                      #dekodowanie bitów parzystości
        
        for y in range(0, 4):
            result.append(int(output_data[y]))                      #konwersja do tablicy bitów

    return result

#funkcja konwertująca 8 elementów tablicy bitów w 'NumPy array'
def decodeSevenBits(bits):
    H = np.array([
        [1, 0, 1, 0, 1, 0, 1],
        [0, 1, 1, 0, 0, 1, 1],
        [0, 0, 0, 1, 1, 1, 1]
    ])

    seven_bits = np.array([[0, 0, 0, 0, 0, 0, 0]])

    for x in range(0, 7):
        seven_bits[0][x] = bits[x]

    syndrome = np.dot(H, seven_bits.T) % 2

    err_index = 0
    for x in range(0, 3):
        err_index += (2**(x))*int(syndrome[x][0])

    if (err_index != 0):
        err_index -= 1
        seven_bits[0][err_index] = int(not(seven_bits[0][err_index]))
    return seven_bits

def main():
    random.seed(30)
    sum_bits = 0
    sum_bytes = 0

    print ("Podaj prawdopodobienstwo bledu (0-100): ")
    fault_prob = float(input())

    img = cv2.imread("../zdjecie.png", 0)

    for x in range(0, 10):
        bits = bsc.imageToBitArray(img)                             # konwersja na tablicę bitów
        bits_coded = code_7_4(bits)                               # generowanie kodu hamminga
        bits_errors = bsc.generateErrors(bits_coded, fault_prob)    # zapis błędów
        bits_decoded = decode(bits_errors)                     # odczytywanie kodu z wykrywaniem błędów i usuwaniem bitów parzystości
        incorrect_bits_rate, incorrect_byte_rate = bsc.countErrors(bits, bits_decoded)
        sum_bits += incorrect_bits_rate
        sum_bytes += incorrect_byte_rate


    sum_bits = sum_bits / 10
    sum_bytes = sum_bytes / 10

    print("Procent prawidlowo przeslanych pikseli (ciag 8 bitów): %d / 59200" %sum_bytes)
    print("Procent prawidlowo przeslanych bitów: %d / 473600" %sum_bits)

main()