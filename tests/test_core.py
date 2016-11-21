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

    def test_parses_segment(self):
        self.network.parse([['segment', '1']])
        self.assertIsInstance(self.network.segments['1'], core.PipeSegment)

    def test_parses_node(self):
        self.network.parse([['node', '1']])
        self.assertIsInstance(self.network.nodes['1'], core.Node)

suite = unittest.TestLoader().loadTestsFromTestCase(NetworkTestCase)
