from scipy.misc import imread
import bsc_functions as bsc
import numpy as np
import cv2
import random

random.seed(30)

print ("Podaj prawdopodobienstwo bledu (0-100): ")
fault_prob = float(input())

sum_bits = 0
sum_bytes = 0

img = cv2.imread("../zdjecie.png", 0)

for x in range(0, 10):
    bits = bsc.imageToBitArray(img)
    bits_errors = bsc.generateErrors(bits, fault_prob)
    incorrect_bits_rate, incorrect_byte_rate = bsc.countErrors(bits, bits_errors)
    sum_bits += incorrect_bits_rate
    sum_bytes += incorrect_byte_rate

sum_bits = sum_bits / 10
sum_bytes = sum_bytes / 10

print("Procent prawidlowo przeslanych pikseli (ciag 8 bitów): %d / 59200" %sum_bytes)
print("Procent prawidlowo przeslanych bitów: %d / 473600" %sum_bits)