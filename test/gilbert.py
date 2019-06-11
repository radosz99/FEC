import random

def gilbert_model(bit_array):
    p_dz = 0.01 # prawdopodobienstwo przejscia z dobrego na zly
    p_zd = 0.95 # prawdopodobienstwo przejscia ze zlego na dobry
    
    state = 1 # 1 = correct, 0 = error

    bit_error_array = []

    for x in range(0, len(bit_array)):
        #losowanie czy następuje zmiana stanu
        r = random.random()
        if (state == 1):
            if (r <= p_dz):
                state = 0
        else:
            if (r <= p_zd):
                state = 1
        #zapisywanie w zależności od aktualnego stanu
        r2 = random.random()
        if (state == 0):
            if (r2 <= 0.1):     # prawdopodobienstwo wystapienia bledu w stanie zlym = 1 lub 0.5 lub 0.1
                bit_error_array.append(int(not bit_array[x]))
            else:               # prawdopodobienstwo wystapienia bledu w stanie dobrym = 0
                bit_error_array.append(bit_array[x])
        else:
            bit_error_array.append(bit_array[x])    

    return bit_error_array