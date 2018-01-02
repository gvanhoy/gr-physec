from physec import file_demod
from collections import Counter
import logging
import numpy as np
import matplotlib.pyplot as plt

CONSTRAINT_LEN = 4
OFFSET = 3


class Classifier:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.demod = file_demod("sources/bpsk2qam16.bin", "bpsk")
        self.bit_string = []
        self.get_bitstring()
        self.sequences = []
        self.hist_sequences()
        print np.multiply(Counter(self.sequences).values(), float(CONSTRAINT_LEN)/len(self.bit_string))
        plt.hist(np.multiply(Counter(self.sequences).values(), float(CONSTRAINT_LEN)/len(self.bit_string)))
        plt.show()

    def get_bitstring(self):
        self.demod.run()
        self.demod.wait()
        self.demod.stop()
        self.bit_string = np.asarray(self.demod.blocks_vector_sink_x_0.data(), dtype=np.bool)

    def hist_sequences(self):
        for x in range(OFFSET, len(self.bit_string) - CONSTRAINT_LEN - OFFSET, CONSTRAINT_LEN):
            self.sequences.append(tuple(self.bit_string[x:x + CONSTRAINT_LEN]))


if __name__ == '__main__':
    classifier = Classifier()
