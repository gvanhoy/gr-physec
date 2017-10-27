import numpy as np

FILE_NAME = 'qam16'

with open("sources/" + FILE_NAME + ".bin", "w") as output_file:
    with open("sources/" + FILE_NAME + ".txt", "r") as input_file:
        complex_array = []
        complex_symbol = complex(0, 0)
        for line in input_file.readlines():
            iq_data = line.split("\t")
            complex_symbol = float(iq_data[0]) + 1j*float(iq_data[1])
            complex_array.append(complex_symbol)

        output_file.write(np.asarray(complex_array, dtype=np.complex64).tobytes())
