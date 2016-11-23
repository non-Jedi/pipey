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
from . import dummy_classes
import pipey.core as core
import unittest

class NetworkTestCase(unittest.TestCase):

    def setUp(self):
        self.network = core.Network()

    def tearDown(self):
        del self.network

    def test_init(self):
        empty_dict = dict()
        self.assertDictEqual(self.network.segments, empty_dict)
        self.assertDictEqual(self.network.nodes, empty_dict)

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

    def test_add_seg(self):
        focus = self.network.add_seg(['segment', 'A'])
        self.assertIs(self.network.segments['A'], focus)
        self.assertIsInstance(focus, core.PipeSegment)

    def test_add_node(self):
        focus = self.network.add_node(['node', 'A'])
        self.assertIs(self.network.nodes['A'], focus)
        self.assertIsInstance(focus, core.Node)

    def test_add_details_seg_start_new(self):
        focus = core.PipeSegment()
        # Check that nodes dict is empty before function runs
        self.assertDictEqual(self.network.nodes, dict())

        self.network.add_details(focus, ['start', 'A'])

        self.assertIsInstance(self.network.nodes['A'], core.Node)
        self.assertIs(self.network.nodes['A'], focus.start)
        self.assertIs(self.network.nodes['A'].outputs[0], focus)

    def test_add_details_seg_start_old(self):
        focus = core.PipeSegment()
        # Use nd to make sure that node 'A' doesn't change
        nd = self.network.nodes['A'] = core.Node()

        self.network.add_details(focus, ['start', 'A'])

        self.assertIs(nd, focus.start)
        self.assertIs(nd, self.network.nodes['A'])
        self.assertIs(nd.outputs[0], focus)

    def test_add_details_seg_end_new(self):
        focus = core.PipeSegment()
        # Check that nodes dict is empty before function runs
        self.assertDictEqual(self.network.nodes, dict())

        self.network.add_details(focus, ['end', 'A'])

        self.assertIsInstance(self.network.nodes['A'], core.Node)
        self.assertIs(self.network.nodes['A'], focus.end)
        self.assertIs(self.network.nodes['A'].inputs[0], focus)

    def test_add_details_seg_end_old(self):
        focus = core.PipeSegment()
        # Use nd to make sure that node 'A' doesn't change
        nd = self.network.nodes['A'] = core.Node()

        self.network.add_details(focus, ['end', 'A'])

        self.assertIs(nd, focus.end)
        self.assertIs(nd, self.network.nodes['A'])
        self.assertIs(nd.inputs[0], focus)
        
    def test_add_details_seg_ele(self):
        focus = dummy_classes.PipeSegmentTest()
        input_list = ['element', 'param1', 'param2']

        self.network.add_details(focus, input_list)

        # Test that add_ele was called on focus
        self.assertIs(focus.add_ele_val, input_list)

    def test_add_details_node(self):
        focus = dummy_classes.NodeTest()
        input_list = ['head', '10', 'feet']

        self.network.add_details(focus, input_list)

        self.assertIs(focus.add_details_val, input_list)

suite = unittest.TestLoader().loadTestsFromTestCase(NetworkTestCase)
