from scipy.misc import imread
import bsc_functions as bsc
import numpy as np
import cv2

print ("Podaj prawdopodobienstwo bledu (0-100): ")
fault_prob = float(input())

img = cv2.imread("../zdjecie.png", 0)
bits = bsc.imageToBitArray(img)
bits_trestled = bsc.imageToBitArrayTrestle(bits)
bits_errors = bsc.generateErrors(bits_trestled, fault_prob, 30)
bits_detrestled = bsc.decodeTrestle(bits_errors)

sum_bits = 0
sum_bytes = 0

for x in range(0, 100):
    incorrect_bits_rate, incorrect_byte_rate = bsc.countErrors(bits, bits_detrestled)
    sum_bits += incorrect_bits_rate
    sum_bytes += incorrect_byte_rate

sum_bits = sum_bits / 100
sum_bytes = sum_bytes / 100

print("Procent prawidlowo przeslanych pikseli (ciag 8 bitów): %d / 59200" %sum_bytes)
print("Procent prawidlowo przeslanych bitów: %d / 473600" %sum_bits)