/* -*- c++ -*- */

#define PHYSEC_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "physec_swig_doc.i"

%{
#include "physec/vrds_mod_cc.h"
%}


%include "physec/vrds_mod_cc.h"
GR_SWIG_BLOCK_MAGIC2(physec, vrds_mod_cc);
