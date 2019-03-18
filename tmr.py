from scipy.misc import imread
import numpy as np
import random

def countErrors(toCompare):             #funkcja zwracajaca procent poprawnie przeslanych danych 
    result = []

    testFile = open('wynik.txt', 'r')	#odczyt z pliku tekstowego bitow odcieni pikseli
    while True:
        threeBits = testFile.read(3)    #odczyt 3 kolejnych znakow z pliku

        if not threeBits:
            break

        countOne = 0
        for x in range(0, 3):           #dekodowanie potrójnej redundancji modularnej
            if (threeBits[x] == '1'):
                countOne += 1           #zliczamy wystepowanie jedynek w podciagu trzyznakowym 
                                        #jesli wystapily 2 lub 3 jedynki to przeslana jest jedynka
        if (countOne >= 2):             #jesli wystapila 1 lub 0 jedynek to przeslane jest zero
            result.append(1)            
        else:
            result.append(0)

    counter = 0     # zlicza prawidlowy przesyl w obrebie kazdych 8 bitow
    counter_2 = 0   # zlicza prawidlowo przeslane piksele (ciag 8 bitow)
    counter_3 = 0   # zlicza prawidlowo przeslane bity

    for x in range(0, len(bits)):           
        if (toCompare[x] == result[x]):     #jezeli bit z pozycji x z pliku wynikowego zgadza sie 
            counter += 1                    #z bitem z pozycji x z pliku startowego to inkrementuje
            counter_3 +=1                   #sie licznik przesylu w obrebie 8 bitow i samych bitow
        if ((x+1)%8 == 0 and counter == 8): #jezeli wszystkie poczawszy od bitu z pozycji x az do 
            counter_2 += 1                  #bitu z pozycji x+7 zostaly przeslane prawidlowo 
        if ((x+1)%8 == 0):                  #to inkrementujemy licznik przeslanych pikseli
            counter = 0                     #po kazdej 8-ce bitow zerujemy licznik przesylu counter
            
    a = counter_3 / len (bits) * 100        #stosunek prawidlowo przeslanych bitow do wszystkich
    b = counter_2 / (len(bits) / 8) * 100   #stosunek prawidlowo przeslanych pikseli do wszystkich

    return a, b

# MAIN

img = imread("zdjecie.png", True, 'L')      #wczytanie zdjecia do img

bits = []                                   #zainicjalizowanie tablicy w ktorej beda dane

print ("Podaj prawdopodobienstwo bledu (0-100): ")
fault_prob = int(input())

for x in range(0, len(img)):
    for y in range(0,len(img[x])):
        element = str(bin(int(img[x][y])))[2:].zfill(8)	#konwertowanie danych do 8bitowej liczby w systemie dwójkowym
        for z in range(0, len(element)):                #ucinajac prefix 0b i z uzupelnieniem np. 10111 -> 00010111
            bits.append(int(element[z]))                #zapis do tablicy kazdego bitu

startFile = open('start.txt', 'w')                      #zapis do pliku ciągu bitów źródłowych
for x in range(0, len(bits)):
    startFile.write(str(bits[x]))

random.seed(30)							#potrójna redundancja modularna i zapis do pliku bitów z prawdopodobienstwem błędu
endFile = open('wynik.txt', 'w')
for x in range(0, len(bits)):
    for y in range(0, 3):               #pętla odpowiadająca za potrajanie każdego bitu
        r = random.randint(0, 100)
        if (r < fault_prob):            #jesli wylosowane pseudo-losowo r jest mniejsze od 
            if (bits[x] == 1):          #prawdopodobienstwa bledu to wystepuje blad
                endFile.write('0')      #w przeciwnym razie prawidlowy przesyl
            else:
                endFile.write('1')
        else:
            endFile.write(str(bits[x]))

endFile.close()

result_bytes, result_pixels = countErrors(bits)

print("Procent prawidlowo przeslanych pikseli (ciag 8 bajtow): %.3f%%" %result_pixels)
print("Procent prawidlowo przeslanych bajtów: %.3f%%" %result_bytes)
