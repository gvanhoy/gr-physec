#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# This application is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This application is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio PHYSEC module. Place your Python package
description here (python/__init__.py).
'''

# import swig generated symbols into the physec namespace
try:
	# this might fail if the module is python-only
	from physec_swig import *
except ImportError:
	pass

# import any pure python here
from modulation_and_coding_scheme_fam import modulation_and_coding_scheme_fam
from file_based_fam import file_based_fam
from random_fec_fam import random_fec_fam
from vsrm_ber_test import vsrm_ber_test
from vsrm_mod import vsrm_mod
from vsrm_demod import vsrm_demod
from file_demod import file_demod


#
