#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Random Source Fam
# Generated: Thu Sep 14 19:11:22 2017
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import numpy
import specest


class random_source_fam(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Random Source Fam")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 100000
        self.const = const = digital.constellation_16qam().base()
        self.P = P = 256
        self.Np = Np = 32
        self.L = L = 8

        ##################################################
        # Blocks
        ##################################################
        self.specest_cyclo_fam_0 = specest.cyclo_fam(Np, P, L)
        self.random = blocks.vector_source_b(map(int, numpy.random.randint(0, const.arity(), 10000)), True)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(4, (firdes.low_pass_2(1, 1, 1 / 8.0, 1 / 16.0, 80)))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((const.points()), 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex * 1, samp_rate, True)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float * 1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float * 2 * Np)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, samp_rate / 4, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.specest_cyclo_fam_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.random, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.specest_cyclo_fam_0, 0), (self.blocks_null_sink_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_frequency(self.samp_rate/4)

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_P(self):
        return self.P

    def set_P(self, P):
        self.P = P

    def get_Np(self):
        return self.Np

    def set_Np(self, Np):
        self.Np = Np

    def get_L(self):
        return self.L

    def set_L(self, L):
        self.L = L


def main(top_block_cls=random_source_fam, options=None):

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
