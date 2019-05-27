from scipy.misc import imread
import bsc_functions as bsc
import random

def gilbert_model(bit_array):
    correct_prob = 9
    injure_prob = 10 - correct_prob
    
    state = 1 # 1 = correct, 0 = error

    bit_error_array = []

    for x in range(0, len(bit_array)):
        #losowanie czy następuje zmiana stanu
        r = random.random()
        if (state == 1):
            if (r*100 <= injure_prob):
                state = 0
        else:
            if (r*100 <= correct_prob):
                state = 1
        #zapisywanie w zależności od aktualnego stanu
        if (state == 0):
            bit_error_array.append(int(not bit_array[x]))   # jeśli r <= prawdopodobieństwo - zapisz negację bitu
        else:
            bit_error_array.append(bit_array[x])    

    return bit_error_array

# potrójna redundancja modularna - funkcja potrajająca każdy bit
def codeTMR(bit_array):
    result = []
    for x in range (0, len(bit_array)):
        for y in range(0, 3):
            result.append(bit_array[x])

    return result

# dekodowanie TMR
def decodeTMR(bit_array):
    result = []

    for x in range(0, len(bit_array), 3):
        three_bits = bit_array[x : x + 3]

        count_one = 0
        for y in range(0, 3):
            if (int(three_bits[y]) == 1):
                count_one += 1
        
        if (count_one >= 2):
            result.append(1)
        else:
            result.append(0)

    return result


# glowna funkcja programu
def main():
    random.seed(30)
    sum_bits = 0
    sum_bytes = 0

    img = imread("../zdjecie.png", True, 'L')  # odczyt obrazu 

    for x in range(0, 10):
        bits = bsc.imageToBitArray(img)         # obraz na tablicę bitów
        bits_TMR = codeTMR(bits)                                        # kodowanie TMR
        bits_trestled = bsc.bitArrayTrestle(bits_TMR)
        bits_TMR_errors = gilbert_model(bits_trestled)
        bits_detrestled = bsc.decodeTrestle(bits_TMR_errors)
        decoded_bits = decodeTMR(bits_detrestled)         # odczyt i dekodowanie potrojonych bitów z błędami
        incorrect_bits_rate, incorrect_bytes_rate = bsc.countErrors(bits, decoded_bits)
        sum_bits += incorrect_bits_rate
        sum_bytes += incorrect_bytes_rate

    sum_bits = sum_bits / 10
    sum_bytes = sum_bytes / 10

    print("Procent prawidlowo przeslanych pikseli (ciag 8 bitów): %d / 59200" %sum_bytes)
    print("Procent prawidlowo przeslanych bitów: %d / 473600" %sum_bits)

main()