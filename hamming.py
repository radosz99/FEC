from scipy.misc import imread
import bsc_functions as bsc
import numpy as np

# glowna funkcja programu
def main():
    print ("Podaj prawdopodobienstwo bledu (0-100): ")
    fault_prob = float(input())

    img = imread("zdjecie.png", True, 'L')  # odczyt obrazu 
    bits = bsc.imageToBitArray(img)         # konwersja na tablicę bitów

<<<<<<< HEAD
    result = bsc.hamminging(bits)
    bits_errors = bsc.generateErrors(result, fault_prob, 30)
    result2 = bsc.rehamminging(bits_errors)
=======
    result = bsc.hamminging(bits)           #generowanie kodu hamminga
    bits_errors = bsc.generateErrors(result, fault_prob, 30)    #zapis błędów

    result2 = bsc.rehamminging(bits_errors) #odczytywanie kodu z wykrywaniem błędów i usuwaniem bitów parzystości
>>>>>>> 76c4f4e67ba4dd2756b1d267d3650e6de58f860c

    #wyliczanie statystyk:
    incorrect_bits_rate, incorrect_byte_rate = bsc.countErrors(bits, result2)

    print("Procent prawidlowo przeslanych pikseli (ciag 8 bitów): %.3f%%" %incorrect_byte_rate)
    print("Procent prawidlowo przeslanych bitów: %.3f%%" %incorrect_bits_rate)
    xbytes = bsc.bitsToBytes(result2)
    bsc.bytesToImg(xbytes, 'wynik.png')

main()