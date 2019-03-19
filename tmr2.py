from scipy.misc import imread
import bsc_functions as bsc

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
    print ("Podaj prawdopodobienstwo bledu (0-100): ")
    fault_prob = int(input())

    img = imread("zdjecie.png", True, 'L')  # odczyt obrazu 
    bits = bsc.imageToBitArray(img)         # obraz na tablicę bitów
    bsc.saveToFile(bits, 'start.txt')       # zapis do pliku

    bits_TMR = codeTMR(bits)                                        # kodowanie TMR
    bits_TMR_errors = bsc.generateErrors(bits_TMR, fault_prob, 30)  # generowanie błędów na potrojonych bitach
    bsc.saveToFile(bits_TMR_errors, 'wynik.txt')                    # zapis potrojonych bitów z błędami do pliku

    start_bits = bsc.readFromFile('start.txt')                      # odczyt prawidłowych bitów z pliku
    decoded_bits = decodeTMR(bsc.readFromFile('wynik.txt'))         # odczyt i dekodowanie potrojonych bitów z błędami

    incorrect_bits_rate, incorrect_bytes_rate = bsc.countErrors(start_bits, decoded_bits)
    print("Procent prawidlowo przeslanych pikseli (ciag 8 bajtow): %.3f%%" %incorrect_bytes_rate)
    print("Procent prawidlowo przeslanych bitów: %.3f%%" %incorrect_bits_rate)

main()