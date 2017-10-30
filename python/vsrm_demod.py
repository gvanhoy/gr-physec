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


class vsrm_demod(gr.hier_block2):

    def __init__(self,
                 delay=1,
                 spread_seq=(1, -1)
                 ):
        gr.hier_block2.__init__(
            self, "Variable Symbol Rate Modulation Demodulator",
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
            gr.io_signature(1, 1, gr.sizeof_gr_complex*1),
        )

        ##################################################
        # Parameters
        ##################################################
        self.delay = delay
        self.spread_seq = spread_seq

        ##################################################
        # Blocks
        ##################################################
        self.blocks_vector_to_stream_0_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, len(spread_seq) + 1)
        self.blocks_vector_to_stream_0_0 = blocks.vector_to_stream(gr.sizeof_gr_complex*1, len(spread_seq) + 1)
        self.blocks_stream_to_vector_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1 + len(spread_seq))
        self.blocks_multiply_const_vxx_0_0_0_0 = blocks.multiply_const_vcc((1/float(len(spread_seq)), ))
        self.blocks_multiply_const_vxx_0_0_0 = blocks.multiply_const_vcc(([1] + [0]*len(spread_seq)))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc(((0,) + spread_seq))
        self.blocks_interleave_0 = blocks.interleave(gr.sizeof_gr_complex*1, 1)
        self.blocks_integrate_xx_0_0 = blocks.integrate_cc(len(spread_seq) + 1, 1)
        self.blocks_integrate_xx_0 = blocks.integrate_cc(len(spread_seq) + 1, 1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, delay)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_delay_0, 0), (self.blocks_stream_to_vector_0_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_multiply_const_vxx_0_0_0_0, 0))
        self.connect((self.blocks_integrate_xx_0_0, 0), (self.blocks_interleave_0, 0))
        self.connect((self.blocks_interleave_0, 0), (self, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_vector_to_stream_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0, 0), (self.blocks_vector_to_stream_0_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0_0_0, 0), (self.blocks_interleave_0, 1))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_stream_to_vector_0_0, 0), (self.blocks_multiply_const_vxx_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_vector_to_stream_0_0_0, 0), (self.blocks_integrate_xx_0_0, 0))
        self.connect((self, 0), (self.blocks_delay_0, 0))

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self.blocks_delay_0.set_dly(self.delay)

    def get_spread_seq(self):
        return self.spread_seq

    def set_spread_seq(self, spread_seq):
        self.spread_seq = spread_seq
        self.blocks_multiply_const_vxx_0_0_0_0.set_k((1/float(len(self.spread_seq)), ))
        self.blocks_multiply_const_vxx_0_0_0.set_k(([1] + [0]*len(self.spread_seq)))
        self.blocks_multiply_const_vxx_0_0.set_k(((0,) + self.spread_seq))