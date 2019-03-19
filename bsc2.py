from scipy.misc import imread
import bsc_functions as bsc

# glowna funkcja programu
def main():
    print ("Podaj prawdopodobienstwo bledu (0-100): ")
    fault_prob = int(input())

    img = imread("zdjecie.png", True, 'L')  # odczyt obrazu 
    bits = bsc.imageToBitArray(img)         # konwersja na tablicę bitów
    bsc.saveToFile(bits, 'start.txt')       # zapis do pliku

    bits_errors = bsc.generateErrors(bits, fault_prob, 30)  # generowanie błędów
    bsc.saveToFile(bits_errors, 'wynik.txt')                # zapis bitów z błędami do pliku

    # porównanie bitów bez błędów i tych z błędami
    incorrect_bits_rate, incorrect_byte_rate = bsc.countErrors(bsc.readFromFile('start.txt'), bsc.readFromFile('wynik.txt'))
    print("Procent prawidlowo przeslanych pikseli (ciag 8 bajtow): %.3f%%" %incorrect_bits_rate)
    print("Procent prawidlowo przeslanych bitów: %.3f%%" %incorrect_byte_rate)

main()