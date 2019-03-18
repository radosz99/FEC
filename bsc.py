from scipy.misc import imread
import numpy as np
import random

def countErrors(toCompare):	#funkcja sprawdzająca stosunek błędów 
    result = []

    testFile = open('wynik.txt', 'r')	#odczyt z pliku tekstowego bitow odcieni pikseli
    while True:
        bit = testFile.read(1)
        if not bit:
            break
        result.append(int(bit))

    # counting errors
    counter = 0						
    for x in range(0, len(bits)):		#porownywanie btow wyniku z bitami źródłowymi
        if (toCompare[x] != result[x]):
            counter += 1

    return (counter / len(bits))		#zwrócenie stosunku ilości błędów do ilości wszystkich bitów

img = imread("zdjecie.png", True, 'L')	#odczyt obrazu 

bits = []

for x in range(0, len(img)):							#konwertowanie sczytanych danych do tablicy reprezętującej odcienie szarości
    for y in range(0,len(img[x])):
        element = str(bin(int(img[x][y])))[2:].zfill(8)	#konwertowanie danych do 8bitowej liczby w systemie dwójkowym
        for z in range(0, len(element)):
            bits.append(int(element[z]))				#zapis do tablicy

startFile = open('start.txt', 'w')		#zapis do pliku ciągu bitów źródłowych
for x in range(0, len(bits)):
    startFile.write(str(bits[x]))

random.seed(30)							#zapis do pliku bitów z prawdopodobiestwem błędu
endFile = open('wynik.txt', 'w')
for x in range(0, len(bits)):
    r = random.randint(0, 100)
    if (r > 75):						#prawdopodobieństwo wystąpienia błędu (25%)
        if (bits[x] == 1):
            endFile.write('0')
        else:
            endFile.write('1')
    else:
        endFile.write(str(bits[x]))

endFile.close()

print(countErrors(bits))			#wypisywanie stosunku wystąpienia błędu 