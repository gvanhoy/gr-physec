#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
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
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
import numpy as np
import pmt


class file_demod(gr.top_block):
    def __init__(self,
                 file_name="",
                 modulation="bpsk"):
        gr.top_block.__init__(self, "File Demodulator")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 100000
        self.file_name = file_name
        self.const = const = digital.constellation_bpsk().base()
        self.const = digital.constellation_bpsk().base()
        self.get_constellation_from_string(modulation)


        ##################################################
        # Blocks
        ##################################################
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(self.const)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_b(1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, self.samp_rate, True)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(self.const.bits_per_symbol(), 1, "", False, gr.GR_LSB_FIRST)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, self.file_name, False)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_vector_sink_x_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.blocks_repack_bits_bb_0, 0))

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
            '16qam': self.constellation_16qam()
        }.get(const_string, digital.constellation_bpsk().base())

    def constellation_16qam(self):
        # points are separated as such
        real, imaginary = np.meshgrid(np.linspace(-3, 3, 4), np.linspace(-3, 3, 4))
        constellation_points = real + np.multiply(imaginary, 1j)
        gray_code = [
            2, 6, 14, 10,
            3, 7, 15, 11,
            1, 5, 13, 9,
            0, 4, 12, 8
        ]
        return digital.constellation_rect(
            constellation_points.flatten(),
            gray_code,
            4,  # rotational symmetry
            4,  # real sectors
            4,  # imaginary sectors
            2,  # real sector width
            2   # imaginary sector width
        ).base()


def main(top_block_cls=file_demod, options=None):
    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
