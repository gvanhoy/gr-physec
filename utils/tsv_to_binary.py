import numpy as np

FILE_NAME = 'bpsk2qam16'

with open("../apps/sources/" + FILE_NAME + ".txt", "r") as input_file:
    output_file_1 = open("../apps/sources/" + FILE_NAME + "_first_half.bin", "w")
    output_file_2 = open("../apps/sources/" + FILE_NAME + "_second_half.bin", "w")
    lines = input_file.readlines()
    num_lines = len(lines)
    complex_array_1 = []
    complex_array_2 = []
    complex_symbol = complex(0, 0)
    for index, line in enumerate(lines):
        iq_data = line.split("\t")
        complex_symbol = float(iq_data[0]) + 1j*float(iq_data[1])
        if index < num_lines/2:
            complex_array_1.append(complex_symbol)
        else:
            complex_array_2.append(complex_symbol)
    output_file_1.write(np.asarray(complex_array_1, dtype=np.complex64).tobytes())
    output_file_2.write(np.asarray(complex_array_1, dtype=np.complex64).tobytes())

