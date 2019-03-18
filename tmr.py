from scipy.misc import imread
import numpy as np
import random

def countErrors(toCompare):	#funkcja sprawdzająca stosunek błędów 
    result = []

    testFile = open('wynik.txt', 'r')	#odczyt z pliku tekstowego bitow odcieni pikseli
    while True:
        threeBits = testFile.read(3)

        if not threeBits:
            break

        countOne = 0
        for x in range(0, 3):			#dekodowanie potrójnej reduntancji modularnej
            if (threeBits[x] == '1'):
                countOne += 1

        if (countOne >= 2):
            result.append(1)
        else:
            result.append(0)

    # counting errors
    counter = 0     # zlicza prawidlowy przesyl w obrebie kazdych 8 bitow
    counter_2 = 0   # zlicza prawidlowo przeslane piksele (ciag 8 bitow)
    counter_3 = 0   # zlicza prawidlowo przeslane bity

    for x in range(0, len(bits)):
        if (toCompare[x] == result[x]):
            counter += 1
            counter_3 +=1
        if ((x+1)%8 == 0 and counter == 8):
            counter_2 += 1
        if ((x+1)%8 == 0):
            counter = 0
            
    a = counter_3 / len (bits) * 100
    b = counter_2 / (len(bits) / 8) * 100
    return a, b

# MAIN

img = imread("zdjecie.png", True, 'L')      #wczytanie zdjecia do img

bits = []   

print ("Podaj prawdopodobienstwo bledu (0-100): ")
fault_prob = int(input())

for x in range(0, len(img)):
    for y in range(0,len(img[x])):
        element = str(bin(int(img[x][y])))[2:].zfill(8)	#konwertowanie danych do 8bitowej liczby w systemie dwójkowym, ucinajac prexix 0b i z uwaga 10111 -> 00010111
        for z in range(0, len(element)):
            bits.append(int(element[z]))				#zapis do tablicy

startFile = open('start.txt', 'w')		#zapis do pliku ciągu bitów źródłowych
for x in range(0, len(bits)):
    startFile.write(str(bits[x]))

random.seed(30)							#potrójna redundancja modularna i zapis do pliku bitów z prawdopodobiestwem błędu
endFile = open('wynik.txt', 'w')
for x in range(0, len(bits)):
    for y in range(0, 3):				#pętla odpowiadająca za potrajanie każdego bitu
        r = random.randint(0, 100)
        if (r < fault_prob):
            if (bits[x] == 1):
                endFile.write('0')
            else:
                endFile.write('1')
        else:
            endFile.write(str(bits[x]))

endFile.close()

result_bytes, result_pixels = countErrors(bits)

print("Procent prawidlowo przeslanych pikseli (ciag 8 bajtow): %.3f%%" %result_pixels)
print("Procent prawidlowo przeslanych bajtów: %.3f%%" %result_bytes)
