#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Random Fec Fam
# Generated: Mon Sep 18 03:30:59 2017
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fec
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import numpy
import numpy as np
import specest


class random_fec_fam(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Random Fec Fam")

        ##################################################
        # Variables
        ##################################################
        self.rate = rate = 2
        self.polys = polys = [109, 79]
        self.k = k = 7
        self.frame_size = frame_size = 500
        self.Np = Np = 32
        self.snr_db = snr_db = 10
        self.samp_rate = samp_rate = 100000
        self.puncpat = puncpat = '11'


        self.enc_cc = enc_cc = fec.cc_encoder_make(frame_size*8, k, rate, (polys), 0, fec.CC_TERMINATED, False)


        self.const = const = digital.constellation_16qam().base()

        self.P = P = 256
        self.L = L = Np/4

        ##################################################
        # Blocks
        ##################################################
        self.specest_cyclo_fam_0 = specest.cyclo_fam(Np, P, Np/4)
        self.random = blocks.vector_source_b(map(int, numpy.random.randint(0, 256, 10000)), True)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(4, (firdes.low_pass_2(1, 1, 1/8.0, 1/16.0, 80)))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fec_extended_encoder_0_0_0 = fec.extended_encoder(encoder_obj_list=enc_cc, threading= None, puncpat=puncpat)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((const.points()), 1)
        self.channels_channel_model_0 = channels.channel_model(
        	noise_voltage=10.0**(-snr_db/20.0),
        	frequency_offset=0.0,
        	epsilon=1.0,
        	taps=(1.0, ),
        	noise_seed=0,
        	block_tags=False
        )
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, int(np.log2(const.arity())), "", False, gr.GR_MSB_FIRST)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*2*Np)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, samp_rate/4, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.specest_cyclo_fam_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.fec_extended_encoder_0_0_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.random, 0), (self.fec_extended_encoder_0_0_0, 0))
        self.connect((self.specest_cyclo_fam_0, 0), (self.blocks_null_sink_0, 0))

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate

    def get_polys(self):
        return self.polys

    def set_polys(self, polys):
        self.polys = polys

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_frame_size(self):
        return self.frame_size

    def set_frame_size(self, frame_size):
        self.frame_size = frame_size

    def get_Np(self):
        return self.Np

    def set_Np(self, Np):
        self.Np = Np
        self.set_L(self.Np/4)

    def get_snr_db(self):
        return self.snr_db

    def set_snr_db(self, snr_db):
        self.snr_db = snr_db
        self.channels_channel_model_0.set_noise_voltage(10.0**(-self.snr_db/20.0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_frequency(self.samp_rate/4)

    def get_puncpat(self):
        return self.puncpat

    def set_puncpat(self, puncpat):
        self.puncpat = puncpat

    def get_enc_cc(self):
        return self.enc_cc

    def set_enc_cc(self, enc_cc):
        self.enc_cc = enc_cc

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_P(self):
        return self.P

    def set_P(self, P):
        self.P = P

    def get_L(self):
        return self.L

    def set_L(self, L):
        self.L = L


def main(top_block_cls=random_fec_fam, options=None):

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
