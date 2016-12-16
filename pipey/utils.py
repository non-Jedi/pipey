#!/usr/bin/env python3

# Copyright 2016 Adam Beckmeyer
# 
# This file is part of Pipey.
# 
# Pipey is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Pipey is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.
# 
# You should have received a copy of the GNU General Public License along
# with Pipey.  If not, see <http://www.gnu.org/licenses/>.

from math import sqrt, log
from scipy import optimize
import pint
from . import ureg

def check_formatting(list_input):

    pass

def colebrook(relative_roughness, reynolds):
    '''Returns colebrook approximation of friction factor'''
    colebrook_zero = lambda f: 1 / sqrt(abs(f[0])) +
                               2.0 * log(relative_roughness / 3.7 +
                                         2.51 / reynolds / sqrt(abs(f[0])), 10)

    f_result = optimize.root(colebrook_zero, [0.040], tol = 0.00001)
    if f_result.success:
        return abs(f_result.x[0])
    else:
        raise optimize.OptimizeWarning(f_result.message)

def reynolds(rho, d, v, mu):
    reynolds = rho * d * v / mu
    if reynolds.to_base_units().u == ureg.dimensionless:
        return reynolds.to_base_units()
    else:
        raise pint.errors.DimensionalityError("Dimensions don't cancel")

