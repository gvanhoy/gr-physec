from gnuradio import blocks
import logging


class Classifier:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.filename = "sources/bpsk2qam16.bin"