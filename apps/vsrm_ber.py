from physec import vsrm_ber_test
from matplotlib import pyplot as plt
import numpy as np
import time

ESNO_RANGE = np.arange(-2, 3, 1)
SPREAD_SEQ_RANGE = {
    0: (1,),
    1: (1, -1),
    2: (1, -1, 1),
    3: (1, -1, 1, -1)
}
COLORS = ['red', 'green', 'blue', 'black']
LINE_STYLES = ['--', '-.', '-', ':']
FIGURE_FILENAME = '../results/seq_len_v_ber_{0}'.format(time.strftime("%Y%m%d-%H%M%S"))


class VariableSymbolRateBER:
    def __init__(self):
        self.vsrm_ber_test = vsrm_ber_test()
        self.ber = np.zeros((len(ESNO_RANGE), len(SPREAD_SEQ_RANGE)))
        self.gen_ber_data()
        self.plot_ber_data()

    def gen_ber_data(self):
        for seq_index in range(len(SPREAD_SEQ_RANGE)):
            for esno_index, esno in enumerate(ESNO_RANGE):
                self.vsrm_ber_test = vsrm_ber_test(
                    esno_db=esno,
                    spread_seq=SPREAD_SEQ_RANGE[seq_index],
                    code_rate='1',
                    modulation='qpsk'
                )
                self.vsrm_ber_test.run()
                self.vsrm_ber_test.wait()
                self.ber[esno_index, seq_index] = self.vsrm_ber_test.blocks_probe_signal_x_0.level()
                self.vsrm_ber_test.stop()

    def plot_ber_data(self):
        print self.ber
        plt.figure(1)
        for x in range(len(SPREAD_SEQ_RANGE)):
            plt.plot(ESNO_RANGE,
                     self.ber[:, x],
                     color=COLORS[x],
                     linewidth=3.0,
                     linestyle=LINE_STYLES[x],
                     label="Len=" + str(x + 1))
        self.save_figure(1, 'Sequence Length vs BER', FIGURE_FILENAME)

    def save_figure(self, figure_number, figure_title, file_name):
        plt.figure(figure_number)
        plt.xlabel('E_s/N_0 (dB)', fontsize=18)
        plt.ylabel('log_10(BER)', fontsize=16)
        plt.xlim(min(ESNO_RANGE), max(ESNO_RANGE))
        plt.ylim(np.amin(self.ber), 0)
        plt.legend(loc='lower left')
        plt.title(figure_title)
        plt.grid(True)
        plt.show()
        plt.savefig(file_name + '.eps', format='eps', dpi=1000)
        plt.savefig(file_name + '.png', format='png', dpi=300)


if __name__ == '__main__':
    main_class = VariableSymbolRateBER()
