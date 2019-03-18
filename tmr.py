from scipy.misc import imread
import numpy as np
import random

def countErrors(toCompare):
    result = []

    testFile = open('wynik.txt', 'r')
    while True:
        threeBits = testFile.read(3)

        if not threeBits:
            break

        countOne = 0
        for x in range(0, 3):
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
            
    print ("Procent prawidlowo przeslanych bitow: %.2f%%" %(counter_3/len(bits)*100))

    return (counter_2 / (len(bits)/8))*100

# MAIN

img = imread("zdjecie.png", True, 'L')

bits = []

print ("Podaj prawdopodobienstwo bledu: ")
answer = int(input())

for x in range(0, len(img)):
    for y in range(0,len(img[x])):
        element = str(bin(int(img[x][y])))[2:].zfill(8)
        for z in range(0, len(element)):
            bits.append(int(element[z]))

startFile = open('start.txt', 'w')
for x in range(0, len(bits)):
    startFile.write(str(bits[x]))

random.seed(30)
endFile = open('wynik.txt', 'w')
for x in range(0, len(bits)):
    for y in range(0, 3):
        r = random.randint(0, 100)
        if (r < answer):
            if (bits[x] == 1):
                endFile.write('0')
            else:
                endFile.write('1')
        else:
            endFile.write(str(bits[x]))

endFile.close()

print("Procent prawidlowo przeslanych pikseli (ciag 8 bitow): %.2f%%" %countErrors(bits))