/* -*- c++ -*- */
/*
 * Copyright 2018 <+YOU OR YOUR COMPANY+>.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "vrds_demod_cc_impl.h"
#include <vector>
#include <iostream>

namespace gr {
  namespace physec {

    vrds_demod_cc::sptr
    vrds_demod_cc::make()
    {
      return gnuradio::get_initial_sptr
        (new vrds_demod_cc_impl());
    }

    /*
     * The private constructor
     */
    vrds_demod_cc_impl::vrds_demod_cc_impl()
      : gr::sync_block("vrds_demod_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
        set_output_multiple(2);
    }

    /*
     * Our virtual destructor.
     */
    vrds_demod_cc_impl::~vrds_demod_cc_impl()
    {
    }

    int
    vrds_demod_cc_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];

      std::vector<tag_t> tags;
      uint64_t idx = 0;

      get_tags_in_window(tags,
                         0,
                         0,
                         noutput_items,
                         pmt::mp("s"));

      for(unsigned int i = 0; i < tags.size(); i++){
        idx = tags[i].offset - nitems_read(0);
        std::cout << "Num symbols: " << pmt::to_long(tags[i].value) << std::endl;

        if(pmt::to_long(tags[i].value) == 2){
            out[idx] = in[idx] + in[idx + 1];
            out[idx + 1] = in[idx] - in[idx + 1];
        }
        else{
            out[idx] =      in[idx] + in[idx + 1] + in[idx + 2] + in[idx + 3];

            out[idx + 1] = -in[idx] + in[idx + 1] + in[idx + 2] - in[idx + 3];

            out[idx + 2] =  in[idx] + in[idx + 1] - in[idx + 2] - in[idx + 3];

            out[idx + 3] =  in[idx] - in[idx + 1] + in[idx + 2] - in[idx + 3];
        }
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace physec */
} /* namespace gr */

