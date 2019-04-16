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
        for y in range(0, 7):
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
    for x in range(0, len(bit_array), 7):
        eigth_bits = rehammingEightBits(bit_array[x : x + 7])      #odczytywanie każdego bajtu koloru
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

    for x in range(0, 7):
        eight_bits[0][x] = bits[x]

    syndrome = np.dot(H, eight_bits.T) % 2
    if(syndrome[3][0] == 1):
        err=0
        for x in range(0, 3):
            err+=(2**(x))*int(syndrome[x][0])

        err -= 1
        eight_bits[0][err] = int(not (eight_bits[0][err]))
   
    return eight_bits