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
    counter = 0
    for x in range(0, len(bits)):
        if (toCompare[x] != result[x]):
            counter += 1

    return (counter / len(bits))

# MAIN

img = imread("zdjecie.png", True, 'L')

bits = []

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
        if (r > 75):
            if (bits[x] == 1):
                endFile.write('0')
            else:
                endFile.write('1')
        else:
            endFile.write(str(bits[x]))

endFile.close()

print(countErrors(bits))