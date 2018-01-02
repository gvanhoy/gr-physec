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
#include <cstdio>
#include <ctime>
#include "vrds_mod_cc_impl.h"

namespace gr {
  namespace physec {

    vrds_mod_cc::sptr
    vrds_mod_cc::make()
    {
      return gnuradio::get_initial_sptr
        (new vrds_mod_cc_impl());
    }

    /*
     * The private constructor
     */
    vrds_mod_cc_impl::vrds_mod_cc_impl()
      : gr::sync_block("vrds_mod_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
        srand(time(NULL));
        set_output_multiple(2);
    }

    /*
     * Our virtual destructor.
     */
    vrds_mod_cc_impl::~vrds_mod_cc_impl()
    {

    }

    int
    vrds_mod_cc_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      gr_complex *out = (gr_complex *) output_items[0];
      unsigned int num_items = 0;

      while(num_items < noutput_items){
            if(rand() % 2 == 0 && num_items + 4 < noutput_items){
                out[num_items] = in[num_items] +
                                  in[num_items + 1] +
                                  in[num_items + 2] +
                                  in[num_items + 3];
                out[num_items + 1] = -in[num_items] +
                                      in[num_items + 1] +
                                      in[num_items + 2] -
                                      in[num_items + 3];
                out[num_items + 2] = in[num_items] +
                                      in[num_items + 1] -
                                      in[num_items + 2] -
                                      in[num_items + 3];
                out[num_items + 3] = in[num_items] -
                                      in[num_items + 1] +
                                      in[num_items + 2] -
                                      in[num_items + 3];
                for(unsigned int i = 0; i < 4; i++){
                    out[num_items + i].real() /= 4.0;
                    out[num_items + i].imag() /= 4.0;
                }
                num_items += 4;
            }
            else{
                out[num_items] = in[num_items] + in[num_items + 1];
                out[num_items + 1] = in[num_items] - in[num_items + 1];
                for(unsigned int i = 0; i < 2; i++){
                    out[num_items + i].real() /= 2.0;
                    out[num_items + i].imag() /= 2.0;
                }
                num_items += 2;
            }
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace physec */
} /* namespace gr */

