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
from gnuradio import blocks
from gnuradio import gr


class vsrm_mod(gr.hier_block2):

    def __init__(self,
                 spread_seq=(-1, 1)
                 ):
        gr.hier_block2.__init__(
            self, "Variable Symbol Rate Modulation Modulator",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.spread_seq = spread_seq

        ##################################################
        # Variables
        ##################################################

        ##################################################
        # Blocks
        ##################################################
        self.blocks_vector_to_stream_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, len(spread_seq))
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, len(spread_seq))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_gr_complex*1, len(spread_seq))
        self.blocks_patterned_interleaver_0 = blocks.patterned_interleaver(gr.sizeof_gr_complex*1, ([0] + [1]*len(spread_seq)))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((spread_seq))
        self.blocks_deinterleave_0 = blocks.deinterleave(gr.sizeof_gr_complex*1, 1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_deinterleave_0, 0), (self.blocks_patterned_interleaver_0, 0))
        self.connect((self.blocks_deinterleave_0, 1), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_vector_to_stream_0, 0))
        self.connect((self.blocks_patterned_interleaver_0, 0), (self, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_vector_to_stream_0, 0), (self.blocks_patterned_interleaver_0, 1))
        self.connect((self, 0), (self.blocks_deinterleave_0, 0))

    def get_spread_seq(self):
        return self.spread_seq

    def set_spread_seq(self, spread_seq):
        self.spread_seq = spread_seq
        self.blocks_repeat_0.set_interpolation(len(self.spread_seq))
        self.blocks_multiply_const_vxx_0.set_k((self.spread_seq))
