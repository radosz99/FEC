from scipy.misc import imread
from matplotlib import pyplot as plt, cm
import numpy as np
import random

#konwertowanie bajtów obrazu do RGB i zapis do pliku wynikowego
def bytesToImg(bytes_array, file_name):
    new_array = np.ndarray(shape=(400, 148, 3), dtype=int)

    i = 0

    for x in range(0, 400):
        for y in range(0, 148):
            for z in range(0, 3):
                new_array[x][y][z] = bytes_array[i]
            i += 1

    plt.imsave(file_name, new_array)

#generowanie kodu hamminga
def hamminging(bit_array):
    result = []

    G = np.array([                  #Maciesz generująca
        [1, 1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 0, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 1, 0, 1, 0, 0, 1, 0]
    ])

    for x in range(0, len(bit_array), 4):
        four_bits = np.array([[0, 0, 0, 0]])
        for y in range(0, 4):                       #konwertowanie tablicy do 'NumPy array'
            four_bits[0][y] = bit_array[x + y]

        data_vector = np.dot(four_bits, G) % 2      #mnożenie przez macierz generującą kod hamminga
        for y in range(0, 8):
            result.append(data_vector[0][y])        #konwersja do tablicy bitów
    return result

#dekodowanie kodu hamminga
def rehamminging(bit_array):
    result = []

    R = np.array([
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0]
    ])
    for x in range(0, len(bit_array), 8):
        eigth_bits = rehammingEightBits(bit_array[x : x + 8])      #odczytywanie każdego bajtu koloru
        output_data = np.dot(R, eigth_bits.T)                      #dekodowanie bitów parzystości
        
        for y in range(0, 4):
            result.append(int(output_data[y]))                      #konwersja do tablicy bitów

    return result

#funkcja konwertująca 8 elementów tablicy bitów w 'NumPy array'
def rehammingEightBits(bits):
    H = np.array([                          #macierz parzystości
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 1, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ])



    eight_bits = np.array([[0, 0, 0, 0, 0, 0, 0, 0]])

    for x in range(0, 8):
        eight_bits[0][x] = bits[x]

    syndrome = np.dot(H, eight_bits.T) % 2
    if(syndrome[3][0] == 1):
        err=0
        for x in range(0, 3):
            err+=(2**(x))*int(syndrome[x][0])

        err -= 1
        eight_bits[0][err] = int(not (eight_bits[0][err]))
   
    return eight_bits

#funkcja konwertująca kolejne 8 bitów koloru na decymalną liczbę 
def bitsToBytes(bit_array):
    result = []

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
            
    a = counter_3# / len (bit_array1) * 100        #stosunek prawidlowo przeslanych bitow do wszystkich
    b = counter_2# / (len(bit_array1) / 8) * 100   #stosunek prawidlowo przeslanych pikseli do wszystkich

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
def generateErrors(bit_array, fault_prob):
    bit_error_array = []


    for x in range(0, len(bit_array)):
 
        r = random.random() * 100
        if (r <= fault_prob):
            bit_error_array.append(int(not bit_array[x]))   # jeśli r <= prawdopodobieństwo - zapisz negację bitu
        else:
            bit_error_array.append(bit_array[x])            # w przeciwnym wypadku zapisz prawidłowy bit

    return bit_error_array

#funckja tworząca przeplot dla podanej tablicy bitów
def imageToBitArrayTrestle(bits):
    bit_array = []
    
    for x in range (0, 8):
        for y in range (x, len(bits),8):
            bit_array.append(bits[y])
            
    return bit_array

#funkcja dekodująca przeplot dla danej tablicy bitów
def decodeTrestle(bits):
    bit_array = []
    tmp = int(len(bits)/8)

    for x in range (0, tmp):
        for y in range(0,len(bits),tmp):
            bit_array.append(bits[x + y])
            
    return bit_array