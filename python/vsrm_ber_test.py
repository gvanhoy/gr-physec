#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
from vr_demodulator import vr_demodulator  # grc-generated hier_block
from vr_modulator import vr_modulator  # grc-generated hier_block
import numpy
import numpy as np


class vsrm_ber_test(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self, "Variable Symbol Rate Modulation BER Test")

        ##################################################
        # Variables
        ##################################################
        self.interp = interp = 2
        self.spread_seq = spread_seq = 1, -1
        self.snr_db = snr_db = 20
        self.samp_rate = samp_rate = 1000000

        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(np.sqrt(interp), 1, 1/float(interp), 0.35, interp*20)



        self.enc_cc = enc_cc = fec.cc_encoder_make(60*8, 7, 2, ([79, 109]), 0, fec.CC_STREAMING, False)



        self.dummy_enc = dummy_enc = fec.dummy_encoder_make(2048)



        self.dummy_dec = dummy_dec = fec.dummy_decoder.make(2048)



        self.dec_cc = dec_cc = fec.cc_decoder.make(60*8, 7, 2, ([79, 109]), 0, -1, fec.CC_STREAMING, False)


        self.const = const = digital.constellation_bpsk().base()


        ##################################################
        # Blocks
        ##################################################
        self.vr_modulator_0 = vr_modulator(
            spread_seq=spread_seq,
        )
        self.vr_demodulator_0 = vr_demodulator(
            delay=0,
            spread_seq=spread_seq,
        )
        self.fec_extended_encoder_0 = fec.extended_encoder(encoder_obj_list=dummy_enc, threading='capillary', puncpat='11')
        self.fec_extended_decoder_0 = fec.extended_decoder(decoder_obj_list=dummy_dec, threading='capillary', ann=None, puncpat='11', integration_period=10000)
        self.fec_ber_bf_0 = fec.ber_bf(False, 100, -7.0)
        self.digital_constellation_soft_decoder_cf_0 = digital.constellation_soft_decoder_cf(const)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((const.points()), 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_repack_bits_bb_0_0_0_0 = blocks.repack_bits_bb(int(np.log2(const.arity())), 8, "", False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0_0_0 = blocks.repack_bits_bb(int(np.log2(const.arity())), 8, "", False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, int(np.log2(const.arity())), "", False, gr.GR_LSB_FIRST)
        self.blocks_probe_signal_x_0 = blocks.probe_signal_f()
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, 0)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, const.arity(), 60*8*20)), True)
        self.analog_fastnoise_source_x_0 = analog.fastnoise_source_c(analog.GR_GAUSSIAN, 10.0**(-snr_db/20.0)/np.sqrt(2), 0, 8192)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fastnoise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.fec_extended_encoder_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.vr_demodulator_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_repack_bits_bb_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_0, 0), (self.fec_ber_bf_0, 1))
        self.connect((self.blocks_repack_bits_bb_0_0_0_0, 0), (self.fec_ber_bf_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.vr_modulator_0, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_0, 0), (self.fec_extended_decoder_0, 0))
        self.connect((self.fec_ber_bf_0, 0), (self.blocks_probe_signal_x_0, 0))
        self.connect((self.fec_extended_decoder_0, 0), (self.blocks_repack_bits_bb_0_0_0_0, 0))
        self.connect((self.fec_extended_encoder_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.vr_demodulator_0, 0), (self.digital_constellation_soft_decoder_cf_0, 0))
        self.connect((self.vr_modulator_0, 0), (self.blocks_throttle_0, 0))

    def get_interp(self):
        return self.interp

    def set_interp(self, interp):
        self.interp = interp

    def get_spread_seq(self):
        return self.spread_seq

    def set_spread_seq(self, spread_seq):
        self.spread_seq = spread_seq
        self.vr_modulator_0.set_spread_seq(self.spread_seq)
        self.vr_demodulator_0.set_spread_seq(self.spread_seq)

    def get_snr_db(self):
        return self.snr_db

    def set_snr_db(self, snr_db):
        self.snr_db = snr_db
        self.analog_fastnoise_source_x_0.set_amplitude(10.0**(-self.snr_db/20.0)/np.sqrt(2))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_enc_cc(self):
        return self.enc_cc

    def set_enc_cc(self, enc_cc):
        self.enc_cc = enc_cc

    def get_dummy_enc(self):
        return self.dummy_enc

    def set_dummy_enc(self, dummy_enc):
        self.dummy_enc = dummy_enc

    def get_dummy_dec(self):
        return self.dummy_dec

    def set_dummy_dec(self, dummy_dec):
        self.dummy_dec = dummy_dec

    def get_dec_cc(self):
        return self.dec_cc

    def set_dec_cc(self, dec_cc):
        self.dec_cc = dec_cc

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const