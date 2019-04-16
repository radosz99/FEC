from scipy.misc import imread
from matplotlib import pyplot as plt, cm
import numpy as np
import random
    four_bits = [0,1,1,0]

    G = np.array([                  #Macierz generująca
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