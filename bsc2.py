from scipy.misc import imread
import bsc_functions as bsc
import numpy as np
import cv2

def main():
    print ("BSC (1) or PRZEPLOT (2): ")
    operation_check = int(input())
    print ("Podaj prawdopodobienstwo bledu (0-100): ")
    fault_prob = float(input())

    img = cv2.imread("zdjecie.png", 0)

    bits = bsc.imageToBitArray(img)               # konwersja na tablicę bitów

    if (operation_check == 2):
        bits = bsc.imageToBitArrayTrestle(bits)

    bsc.saveToFile(bits, 'start.txt')       # zapis do pliku
    

    bits_errors = bsc.generateErrors(bits, fault_prob, 30)  # generowanie błędów
    bsc.saveToFile(bits_errors, 'wynik.txt')                # zapis bitów z błędami do pliku

    # porównanie bitów bez błędów i tych z błędami
    incorrect_bits_rate, incorrect_byte_rate = bsc.countErrors(bsc.readFromFile('start.txt'), bsc.readFromFile('wynik.txt'))
    print("Procent prawidlowo przeslanych pikseli (ciag 8 bitów): %.3f%%" %incorrect_byte_rate)
    print("Procent prawidlowo przeslanych bitów: %.3f%%" %incorrect_bits_rate)

    # xbytes = bsc.bitsToBytes(bits_errors)
    if (operation_check == 2):
        bits_errors = bsc.decodeTrestle(bits_errors)
    xbytes = bsc.bitsToBytes(bits_errors)
    bsc.bytesToImg(xbytes, 'wynik.png')

main()