from scipy.misc import imread
import bsc_functions as bsc
import numpy as np
import cv2

def main():
    print ("Podaj prawdopodobienstwo bledu (0-100): ")
    fault_prob = float(input())

    img = cv2.imread("zdjecie.png", 0)
    bits = bsc.imageToBitArray(img)         # konwersja na tablicę bitów

    result = bsc.hamminging(bits)           #generowanie kodu hamminga
    bits_errors = bsc.generateErrors(result, fault_prob, 30)    #zapis błędów

    result2 = bsc.rehamminging(bits_errors) #odczytywanie kodu z wykrywaniem błędów i usuwaniem bitów parzystości

    #wyliczanie statystyk:
    incorrect_bits_rate, incorrect_byte_rate = bsc.countErrors(bits, result2)

    print("Procent prawidlowo przeslanych pikseli (ciag 8 bitów): %.5f%%" %incorrect_byte_rate)
    print("Procent prawidlowo przeslanych bitów: %.5f%%" %incorrect_bits_rate)
    xbytes = bsc.bitsToBytes(result2)
    bsc.bytesToImg(xbytes, 'wynik.png')

main()