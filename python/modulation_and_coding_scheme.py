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
#
from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio import digital
from gnuradio import fec
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import numpy
import numpy as np
import specest


class modulation_and_coding_scheme(gr.top_block):
    def __init__(self,
                 Np,
                 P,
                 modulation,
                 code_rate,
                 code_type="convolutional"
                 ):
        gr.top_block.__init__(self, "Modulation and Coding Scheme")

        ##################################################
        # Variables
        ##################################################
        self.Np = Np
        self.P = P
        self.samp_rate = 100000
        self.puncpat = '11'
        self.snr_db = 10
        self.enc_cc = enc_cc = fec.cc_encoder_make(2048, 7, 2, ([79, 109]), 0, fec.CC_STREAMING, False)
        self.const = digital.constellation_bpsk().base()
        self.get_constellation_from_string(modulation)
        self.get_puncpat_from_string(code_rate)


        ##################################################
        # Blocks
        ##################################################
        self.specest_cyclo_fam_0 = specest.cyclo_fam(self.Np, self.P, self.Np/4)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(4, (firdes.low_pass_2(1, 1, 1/8.0, 1/16.0, 80)))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fec_extended_encoder_0 = fec.extended_encoder(encoder_obj_list=enc_cc, threading='capillary', puncpat='11')
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc((self.const.points()), 1)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=10.0**(-self.snr_db/20.0),
            frequency_offset=0.0,
            epsilon=1.0,
            taps=(1.0, ),
            noise_seed=0,
            block_tags=False
        )
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, int(np.log2(self.const.arity())), "", False, gr.GR_LSB_FIRST)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*2*self.Np)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(self.samp_rate, analog.GR_COS_WAVE, self.samp_rate/4, 1, 0)
        self.analog_random_source_x_0 = blocks.vector_source_b(map(int, numpy.random.randint(0, 256, 10000)), True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.fec_extended_encoder_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.specest_cyclo_fam_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.fec_extended_encoder_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.specest_cyclo_fam_0, 0), (self.blocks_null_sink_0, 0))

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
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_frequency(self.samp_rate/4)

    def get_num_samples(self):
        return self.num_samples

    def set_num_samples(self, num_samples):
        self.num_samples = num_samples

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
            '1/2': '11',
            '2/3': '1101',
            '3/4': '110110',
            '5/6': '1101100110'
        }.get(code_rate_string, '11')
