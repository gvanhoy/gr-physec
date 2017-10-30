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
from physec.vsrm_demod import vsrm_demod
from physec.vsrm_mod import vsrm_mod
import numpy as np


class vsrm_ber_test(gr.top_block):
    def __init__(self,
                 spread_seq=(1, -1),
                 esno_db=20,
                 modulation='BPSK',
                 code_rate='1'
                 ):
        gr.top_block.__init__(self, "Variable Symbol Rate Modulation BER Test")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = 10000000
        self.spread_seq = spread_seq
        self.esno_db = esno_db
        self.puncpat = '11'
        if code_rate == '1':
            self.enc = fec.dummy_encoder_make(2048)
            self.dec = fec.dummy_decoder.make(2048)
        else:
            self.enc = fec.cc_encoder_make(2048, 7, 2, ([79, 109]), 0, fec.CC_STREAMING, False)
            self.dec = fec.cc_decoder.make(2048, 7, 2, ([79, 109]), 0, -1, fec.CC_STREAMING, False)

        self.const = digital.constellation_bpsk().base()
        self.get_constellation_from_string(modulation)
        self.get_puncpat_from_string(code_rate)

        ##################################################
        # Blocks
        ##################################################
        self.vsrm_mod_0 = vsrm_mod(
            spread_seq=self.spread_seq,
        )
        self.vsrm_demod_0 = vsrm_demod(
            delay=0,
            spread_seq=self.spread_seq,
        )
        self.fec_extended_encoder_0 = fec.extended_encoder(encoder_obj_list=self.enc, threading='capillary', puncpat=self.puncpat)
        self.fec_extended_decoder_0 = fec.extended_decoder(decoder_obj_list=self.dec, threading='capillary', ann=None, puncpat=self.puncpat, integration_period=10000)
        self.fec_ber_bf_0 = fec.ber_bf(True, 100, -7.0)
        self.digital_constellation_soft_decoder_cf_0 = digital.constellation_soft_decoder_cf(self.const)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, self.samp_rate, True)
        self.blocks_repack_bits_bb_0_0_0_0 = blocks.repack_bits_bb(int(np.log2(self.const.arity())), 8, "", False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0_0_0 = blocks.repack_bits_bb(int(np.log2(self.const.arity())), 8, "", False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, int(np.log2(self.const.arity())), "", False, gr.GR_LSB_FIRST)
        self.blocks_probe_signal_x_0 = blocks.probe_signal_f()
        self.blocks_delay_0 = blocks.delay(gr.sizeof_char*1, 0)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, np.random.randint(0, self.const.arity(), 10000000)), True)
        self.analog_fastnoise_source_x_0 = analog.fastnoise_source_c(analog.GR_GAUSSIAN, 10.0**(-esno_db/20.0), 0, 2**16)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_fastnoise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.fec_extended_encoder_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.vsrm_demod_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_repack_bits_bb_0_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_0, 0), (self.fec_ber_bf_0, 1))
        self.connect((self.blocks_repack_bits_bb_0_0_0_0, 0), (self.fec_ber_bf_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.vsrm_mod_0, 0))
        self.connect((self.digital_constellation_soft_decoder_cf_0, 0), (self.fec_extended_decoder_0, 0))
        self.connect((self.fec_ber_bf_0, 0), (self.blocks_probe_signal_x_0, 0))
        self.connect((self.fec_extended_decoder_0, 0), (self.blocks_repack_bits_bb_0_0_0_0, 0))
        self.connect((self.fec_extended_encoder_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.vsrm_demod_0, 0), (self.digital_constellation_soft_decoder_cf_0, 0))
        self.connect((self.vsrm_mod_0, 0), (self.blocks_throttle_0, 0))

    def get_spread_seq(self):
        return self.spread_seq

    def set_spread_seq(self, spread_seq):
        self.spread_seq = spread_seq
        self.vr_modulator_0.set_spread_seq(self.spread_seq)
        self.vr_demodulator_0.set_spread_seq(self.spread_seq)

    def get_esno_db(self):
        return self.esno_db

    def set_esno_db(self, esno_db):
        self.esno_db = esno_db
        self.analog_fastnoise_source_x_0.set_amplitude(10.0**(-self.esno_db/20.0)/np.sqrt(2))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_const(self):
        return self.const

    def set_const(self, const):
        self.const = const

    def get_constellation_from_string(self, const_string):
        self.const = {
            'bpsk': digital.constellation_bpsk().base(),
            'qpsk': digital.constellation_qpsk().base(),
            '8psk': digital.constellation_8psk().base(),
            '16qam': digital.constellation_16qam().base()
        }.get(const_string, digital.constellation_bpsk().base())

    def get_puncpat_from_string(self, code_rate_string):
        '''
            The puncpat comes from the "puncturing matrix" that is
            shown for convolutional codes on wikipedia:
            https://en.wikipedia.org/wiki/Convolutional_code
            Where a matrix: 1 0 1
                            1 1 0
            becomes puncpat: '110110'
        '''
        self.puncpat = {
            '1':   '11',
            '1/2': '11',
            '2/3': '1101',
            '3/4': '110110',
            '5/6': '1101100110'
        }.get(code_rate_string, '11')
