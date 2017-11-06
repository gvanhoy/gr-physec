from physec import vsrm_ber_test
from matplotlib import pyplot as plt
import numpy as np
import time

ESNO_RANGE = np.arange(0, 7, 1)
EXPERIMENT_DESC = {
    0: ('bpsk', '1', (1,)),
    1: ('bpsk', '1/2', (1,)),
    2: ('bpsk', '1', (1, -1)),
    3: ('bpsk', '1/2', (1, -1)),
    4: ('qpsk', '1', (1,)),
    5: ('qpsk', '1/2', (1,)),
    6: ('qpsk', '1', (1, -1)),
    7: ('qpsk', '1/2', (1, -1))
}
COLORS = ['red', 'green', 'blue', 'black', 'red', 'green', 'blue', 'black']
LINE_STYLES = ['--', '-.', '-', ':', '--', '-.', '-', ':']
MARKERS = ['s', 's', 's', 's', 'o', 'o', 'o', 'o']
FIGURE_FILENAME = '../results/esno_v_ber_{0}'.format(time.strftime("%Y%m%d-%H%M%S"))


class VariableSymbolRateBER:
    def __init__(self):
        self.vsrm_ber_test = vsrm_ber_test()
        self.ber = np.zeros((len(ESNO_RANGE), len(EXPERIMENT_DESC)))
        self.gen_ber_data()
        self.plot_ber_data()

    def gen_ber_data(self):
        for exp_index in range(len(EXPERIMENT_DESC)):
            for esno_index, esno in enumerate(ESNO_RANGE):
                print "Testing SNR: {0}, Seq: {1}".format(esno, EXPERIMENT_DESC[exp_index][2])
                self.vsrm_ber_test = vsrm_ber_test(
                    esno_db=esno,
                    spread_seq=EXPERIMENT_DESC[exp_index][2],
                    code_rate=EXPERIMENT_DESC[exp_index][1],
                    modulation=EXPERIMENT_DESC[exp_index][0]
                )
                self.vsrm_ber_test.run()
                self.vsrm_ber_test.wait()
                self.ber[esno_index, exp_index] = self.vsrm_ber_test.blocks_probe_signal_x_0.level()
                self.vsrm_ber_test.stop()

    def plot_ber_data(self):
        print self.ber
        plt.figure(1)
        for x in range(len(EXPERIMENT_DESC)):
            description_string = str(EXPERIMENT_DESC[x][0]) + ", R=" + str(EXPERIMENT_DESC[x][1]) + ", Len=" + str(len(EXPERIMENT_DESC[x][2]))
            plt.plot(ESNO_RANGE,
                     self.ber[:, x],
                     color=COLORS[x],
                     linewidth=3.0,
                     linestyle=LINE_STYLES[x],
                     marker=MARKERS[x],
                     markersize=10,
                     label=description_string)
        self.save_figure(1, "Bit Error Rate", FIGURE_FILENAME)

    def save_figure(self, figure_number, figure_title, file_name):
        plt.figure(figure_number)
        plt.xlabel('E_s/N_0 (dB)', fontsize=18)
        plt.ylabel('log_10(BER)', fontsize=18)
        plt.xlim(min(ESNO_RANGE), max(ESNO_RANGE))
        plt.ylim(np.amin(self.ber), 0)
        plt.legend(loc='lower left')
        plt.title(figure_title, fontsize=18)
        plt.grid(True)
        # plt.show()
        plt.savefig(file_name + '.eps', format='eps', dpi=1000)
        plt.savefig(file_name + '.png', format='png', dpi=300)


if __name__ == '__main__':
    main_class = VariableSymbolRateBER()
