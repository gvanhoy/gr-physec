from physec import vsrm_ber_test


class VariableSymbolRateBER:
    def __init__(self):
        self.vsrm_ber_test = vsrm_ber_test(esno_db=3)
        self.vsrm_ber_test.run()
        self.vsrm_ber_test.wait()
        print self.vsrm_ber_test.blocks_probe_signal_x_0.level()
        self.vsrm_ber_test.stop()

if __name__ == '__main__':
    main_class = VariableSymbolRateBER()
