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
import pipey.core as core
import unittest

class NetworkTestCase(unittest.TestCase):

    def setUp(self):
        self.network = core.Network()

    def tearDown(self):
        del self.network

    def test_parses_segment_header(self):
        self.network.parse([['segment', '1']])
        self.assertIsInstance(self.network.segments['1'], core.PipeSegment)

    def test_parses_node_header(self):
        self.network.parse([['node', '1']])
        self.assertIsInstance(self.network.nodes['1'], core.Node)

    def test_parses_empty_header(self):
        self.network.parse([['',]])
        self.assertDictEqual(self.network.segments, dict())
        self.assertDictEqual(self.network.nodes, dict())
        self.assertIsInstance(self.network.fluid, core.Fluid)

    def test_parse_current_focus(self):
        self.network.parse([['segment', '1'],
                            ['start', 'B'],
                            ['node', 'A'],
                            ['head', '5.67', 'feet'],
                            ['segment', '2'],
                            ['end', 'A'],])
        self.assertIs(self.network.segments['1'].start,
                      self.network.nodes['B'])
        self.assertAlmostEqual(self.network.nodes['A'].head.m, 
                               5.67, places = 2)
        self.assertIs(self.network.segments['2'].end,
                      self.network.nodes['A'])

suite = unittest.TestLoader().loadTestsFromTestCase(NetworkTestCase)
