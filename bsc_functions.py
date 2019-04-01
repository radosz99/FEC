from scipy.misc import imread
from matplotlib import pyplot as plt, cm
import numpy as np
import random

def bytesToImg(bytes_array, file_name):
    new_array = np.ndarray(shape=(400, 148, 3), dtype=int)

    i = 0

    for x in range(0, 400):
        for y in range(0, 148):
            for z in range(0, 3):
                new_array[x][y][z] = bytes_array[i]
            i += 1

    plt.imsave(file_name, new_array)

def bitsToBytes(bit_array):
    result = []
    # tmp_array = 

    for x in range(0, len(bit_array), 8):
        byte = ""
        for y in range(0, 8):
            byte += str(bit_array[x + y])

        result.append(int(byte, 2))

    return result

# funkcja sprawdzająca stosunek błędów 
def countErrors(bit_array1, bit_array2):             
    counter_1 = 0 # zlicza prawidlowy przesyl w obrebie kazdych 8 bitow
    counter_2 = 0 # zlicza prawidlowo przeslane piksele (ciag 8 bitow)
    counter_3 = 0 # zlicza prawidlowo przeslane bity

    for x in range(0, len(bit_array1)):           
        if (bit_array1[x] == bit_array2[x]):     #jezeli bit z pozycji x z pliku wynikowego zgadza sie 
            counter_1 += 1                    #z bitem z pozycji x z pliku startowego to inkrementuje
            counter_3 +=1                   #sie licznik przesylu w obrebie 8 bitow i samych bitow
        if ((x+1)%8 == 0 and counter_1 == 8): #jezeli wszystkie poczawszy od bitu z pozycji x az do 
            counter_2 += 1                  #bitu z pozycji x+7 zostaly przeslane prawidlowo 
        if ((x+1)%8 == 0):                  #to inkrementujemy licznik przeslanych pikseli
            counter_1 = 0                     #po kazdej 8-ce bitow zerujemy licznik przesylu counter
            
    a = counter_3 / len (bit_array1) * 100        #stosunek prawidlowo przeslanych bitow do wszystkich
    b = counter_2 / (len(bit_array1) / 8) * 100   #stosunek prawidlowo przeslanych pikseli do wszystkich

    return a, b

# funkcja konwertująca obraz na tablicę jedynek i zer
def imageToBitArray(img):
    bit_array = []

    for x in range(0, len(img)):                            #konwertowanie sczytanych danych do tablicy reprezentującej odcienie szarości
        for y in range(0,len(img[x])):
            element = str(bin(int(img[x][y])))[2:].zfill(8) #konwertowanie danych do 8-bitowej liczby w systemie dwójkowym
            for z in range(0, len(element)):
                bit_array.append(int(element[z]))                #zapis do tablicy

    return bit_array

# funkcja zapisująca podaną tablicę do pliku tekstowego
def saveToFile(bit_array, file_name):
    file = open(file_name, 'w')      #zapis do pliku ciągu bitów źródłowych

    for x in range(0, len(bit_array)):
        file.write(str(bit_array[x]))

# funkcja odczytująca z pliku tekstowego
def readFromFile(file_name):
    result = []

    file = open(file_name, 'r') # odczyt z pliku tekstowego bitow odcieni pikseli

    while True:
        bit = file.read(1)
        if not bit:
            break
        result.append(int(bit))

    return result

# funkcja generująca błędy w podanej tablicy z podanym prawdopodobieństwem
def generateErrors(bit_array, fault_prob, seed):
    bit_error_array = []
    random.seed(seed)

    for x in range(0, len(bit_array)):
        r = random.randint(0, 100)
        if (r < fault_prob):
            bit_error_array.append(int(not bit_array[x]))   # jeśli r < prawdopodobieństwo - zapisz negację bitu
        else:
            bit_error_array.append(bit_array[x])            # w przeciwnym wypadku zapisz prawidłowy bit

    return bit_error_array