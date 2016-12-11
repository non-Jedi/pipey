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

from .context import pipey
import pipey.utils as utils
import unittest
from pipey import ureg

class FrictionFactorTests(unittest.TestCase):
    '''Runs unit tests on all functions related to friction factors.'''
    def test_colebrook(self):
        '''Tests colebrook function versus Moody diagram.'''
        self.assertAlmostEqual(utils.colebrook(0.020, 2e5), 0.0488,
                               delta = 0.0006)
        self.assertAlmostEqual(utils.colebrook(0.070, 3e4), 0.0850,
                               delta = 0.0006)
        self.assertAlmostEqual(utils.colebrook(0.004, 6e3), 0.0400,
                               delta = 0.0006)
        self.assertAlmostEqual(utils.colebrook(0.001, 1e6), 0.0199,
                               delta = 0.0006)
        self.assertAlmostEqual(utils.colebrook(1e-05, 8e8), 0.0082,
                               delta = 0.0006)

    def test_laminar_ff(self):
        '''Tests laminar_ff function versus hand calculated values.'''
        self.assertAlmostEqual(utils.laminar_ff(1500), 23.4375, places = 5)
        self.assertAlmostEqual(utils.laminar_ff(64), 1, places = 5)
        self.assertAlmostEqual(utils.laminar_ff(1999), 31.234375, places = 5)

    def test_friction_factor(self):
        '''Tests friction_factor function for both laminar and turbulent.'''
        self.assertAlmostEqual(utils.friction_factor(0.020, 2e5), 0.0488,
                               delta = 0.0006)
        self.assertAlmostEqual(utils.friction_factor(0.070, 3e4), 0.0850,
                               delta = 0.0006)
        self.assertAlmostEqual(utils.friction_factor(0.004, 6e3), 0.0400,
                               delta = 0.0006)
        self.assertAlmostEqual(utils.friction_factor(0.001, 1e6), 0.0199,
                               delta = 0.0006)
        self.assertAlmostEqual(utils.friction_factor(1500), 23.4375,
                               delta = 0.0006)
        self.assertAlmostEqual(utils.friction_factor(64), 1,
                               delta = 0.0006)
        self.assertAlmostEqual(utils.friction_factor(1999), 31.234375,
                               delta = 0.0006)

ff_suite = unittest.TestLoader().loadTestsFromTestCase(FrictionFactorTests)

suite = unittest.TestSuite()
suite.addTests((ff_suite,))

