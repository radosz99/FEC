from scipy.misc import imread
import numpy as np
import random

def countErrors(toCompare):	#funkcja sprawdzająca stosunek błędów 
    result = []

    testFile = open('wynik.txt', 'r')	#sczytywanie z pliku tekstowego bitow odcieni pikseli
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
    counter = 0
    for x in range(0, len(bits)):		#obliczanie ilości błędów
        if (toCompare[x] != result[x]):
            counter += 1

    return (counter / len(bits))		#zwrócenie stosunku ilości błędów do ilości wszystkich bitów

# MAIN

img = imread("zdjecie.png", True, 'L')

bits = []

for x in range(0, len(img)):							#konwertowanie sczytanych danych do tablicy reprezętującej odcienie szarości
    for y in range(0,len(img[x])):
        element = str(bin(int(img[x][y])))[2:].zfill(8)	#konwertowanie danych do 8bitowej liczby w systemie dwójkowym
        for z in range(0, len(element)):
            bits.append(int(element[z]))				#zapis do tablicy

startFile = open('start.txt', 'w')		#zapis do pliku ciągu bitów źródłowych
for x in range(0, len(bits)):
    startFile.write(str(bits[x]))

random.seed(30)							#potrójna redundancja modularna i zapis do pliku bitów z prawdopodobiestwem błędu
endFile = open('wynik.txt', 'w')
for x in range(0, len(bits)):
    for y in range(0, 3):				#pędla odpowiadająca za potrajanie każdego bitu
        r = random.randint(0, 100)
        if (r > 75):					#prawdopodobieństwo wystąpienia błędu (25%)
            if (bits[x] == 1):
                endFile.write('0')
            else:
                endFile.write('1')
        else:
            endFile.write(str(bits[x]))

endFile.close()

print(countErrors(bits))		#wypisywanie stosunku wystąpienia błędu 