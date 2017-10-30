from physec import vsrm_ber_test
import numpy as np
from matplotlib import pyplot as plt

ESNO_RANGE = np.arange(4, 10, 1)
SPREAD_SEQ_RANGE = {
    0: (1,),
    1: (1, -1),
    2: (1, -1, 1),
    3: (1, -1, 1, -1)
}


class VariableSymbolRateBER:
    def __init__(self):
        self.vsrm_ber_test = vsrm_ber_test()
        self.ber = np.zeros((len(ESNO_RANGE), len(SPREAD_SEQ_RANGE)))
        self.gen_ber_data()
        self.plot_ber_data()

    def gen_ber_data(self):
        for seq_index in range(len(SPREAD_SEQ_RANGE)):
            for esno_index, esno in enumerate(ESNO_RANGE):
                self.vsrm_ber_test = vsrm_ber_test(esno_db=esno, spread_seq=SPREAD_SEQ_RANGE[seq_index])
                self.vsrm_ber_test.run()
                self.vsrm_ber_test.wait()
                self.ber[esno_index, seq_index] = self.vsrm_ber_test.blocks_probe_signal_x_0.level()
                self.vsrm_ber_test.stop()

    def plot_ber_data(self):
        print self.ber
        plt.plot(ESNO_RANGE,
                 self.ber,
                 color=['red', 'green', 'blue', 'black'],
                 linewidth=3.0,
                 linestyle=['--', '-.', '-', ':']
                 )
        plt.show()

if __name__ == '__main__':
    main_class = VariableSymbolRateBER()
