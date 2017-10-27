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
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import pmt
import specest


class file_based_fam(gr.top_block):

    def __init__(self, filename=""):
        gr.top_block.__init__(self, "File Based Fam")

        ##################################################
        # Variables
        ##################################################
        self.snr_db = snr_db = 10
        self.samp_rate = samp_rate = 100000
        self.P = P = 256
        self.Np = Np = 16
        self.L = L = self.Np/4
        print "Approximate amount of points for SCD: {0}".format(self.P*self.Np/4)
        self.filename = filename

        ##################################################
        # Blocks
        ##################################################
        self.specest_cyclo_fam_0 = specest.cyclo_fam(Np, P, L)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccc(4, (firdes.low_pass_2(1, 1, 1/8.0, 1/16.0, 80)))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=10.0**(-snr_db/20.0),
            frequency_offset=0.0,
            epsilon=1.0,
            taps=(1.0, ),
            noise_seed=0,
            block_tags=False
        )
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate, True)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*2*Np)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_file_source_0_0 = blocks.file_source(gr.sizeof_gr_complex*1, self.filename, True)
        self.blocks_file_source_0_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, samp_rate/4, 1, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_file_source_0_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.specest_cyclo_fam_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.specest_cyclo_fam_0, 0), (self.blocks_null_sink_0, 0))

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
