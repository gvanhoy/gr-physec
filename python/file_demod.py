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
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(const)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_b(1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, samp_rate,True)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(const.bits_per_symbol(), 1, "", False, gr.GR_LSB_FIRST)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/gvanhoy/gr-physec/apps/sources/bpsk2qam16.bin', False)
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
            '16qam': digital.constellation_16qam().base()
        }.get(const_string, digital.constellation_bpsk().base())


def main(top_block_cls=file_demod, options=None):
    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()
