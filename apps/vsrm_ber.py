from physec import vsrm_ber_test
import numpy as np
from matplotlib import pyplot as plt

ESNO_RANGE = np.arange(4, 6, .25)


class VariableSymbolRateBER:
    def __init__(self):
        self.vsrm_ber_test = vsrm_ber_test()
        self.ber = np.zeros((len(ESNO_RANGE)))
        self.gen_ber_data()
        self.plot_ber_data()

    def gen_ber_data(self):
        for index, esno in enumerate(ESNO_RANGE):
            self.vsrm_ber_test = vsrm_ber_test(esno_db=esno)
            self.vsrm_ber_test.run()
            self.vsrm_ber_test.wait()
            self.ber[index] = self.vsrm_ber_test.blocks_probe_signal_x_0.level()
            self.vsrm_ber_test.stop()

    def plot_ber_data(self):
        plt.plot(ESNO_RANGE, self.ber)
        plt.show()

if __name__ == '__main__':
    main_class = VariableSymbolRateBER()
