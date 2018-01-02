from physec import file_demod
import logging


class Classifier:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.demod = file_demod("sources/bpsk2qam16.bin", "qpsk")
        self.get_bitstring()

    def get_bitstring(self):
        self.demod.run()
        self.demod.wait()
        self.demod.stop()
        print len(self.demod.blocks_vector_sink_x_0.data())


if __name__ == '__main__':
    classifier = Classifier()
