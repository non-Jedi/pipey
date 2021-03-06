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
from pipey import ureg

class NetworkTestCase(unittest.TestCase):
    '''Runs units tests on all methods of Network class.'''
    def setUp(self):
        '''Creates core.Network object to be tested'''
        self.network = core.Network()

    def tearDown(self):
        '''Destroys test object'''
        del self.network

    def test_init(self):
        '''Tests that test object initialized correctly'''
        empty_dict = dict()
        self.assertDictEqual(self.network.segments, empty_dict)
        self.assertDictEqual(self.network.nodes, empty_dict)

    def test_parses_segment_header(self):
        '''Tests parse method of core.Network with segment header'''
        self.network.parse([['segment', '1']])
        self.assertIsInstance(self.network.segments['1'], core.PipeSegment)

    def test_parses_node_header(self):
        '''Tests parse method of core.Network with node header'''
        self.network.parse([['node', '1']])
        self.assertIsInstance(self.network.nodes['1'], core.Node)

    def test_parses_empty_header(self):
        '''Tests parse method of core.Network with empty line'''
        self.network.parse([['',]])
        self.assertDictEqual(self.network.segments, dict())
        self.assertDictEqual(self.network.nodes, dict())

    def test_parse_current_focus(self):
        '''Tests that parse method of core.Network correctly switches focus'''
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
        '''Tests method of core.Network: add_seg'''
        focus = self.network.add_seg(['segment', 'A'])
        self.assertIs(self.network.segments['A'], focus)
        self.assertIsInstance(focus, core.PipeSegment)

    def test_add_node(self):
        '''Tests method of core.Network: add_node'''
        focus = self.network.add_node(['node', 'A'])
        self.assertIs(self.network.nodes['A'], focus)
        self.assertIsInstance(focus, core.Node)

    def test_add_details_seg_start_new(self):
        '''Tests method of core.Network: add_details.

        Tests that add_details method correctly handles the situation
        where the details reference a node that doesn't exist. This test
        is against adding a segment start.
        '''
        focus = core.PipeSegment()
        # Check that nodes dict is empty before function runs
        self.assertDictEqual(self.network.nodes, dict())

        self.network.add_details(focus, ['start', 'A'])

        self.assertIsInstance(self.network.nodes['A'], core.Node)
        self.assertIs(self.network.nodes['A'], focus.start)
        self.assertIs(self.network.nodes['A'].outputs[0], focus)

    def test_add_details_seg_start_old(self):
        '''Tests method of core.Network: add_details.

        Tests that add_details method correctly handles the situation
        where the details reference a node that already exists. This
        test is against adding a segment start.
        '''
        focus = core.PipeSegment()
        # Use nd to make sure that node 'A' doesn't change
        nd = self.network.nodes['A'] = core.Node()

        self.network.add_details(focus, ['start', 'A'])

        self.assertIs(nd, focus.start)
        self.assertIs(nd, self.network.nodes['A'])
        self.assertIs(nd.outputs[0], focus)

    def test_add_details_seg_end_new(self):
        '''Tests method of core.Network: add_details.

        Tests that add_details method correctly handles the situation
        where the details reference a node that does not exist. This
        test is against adding a segment end.
        '''
        focus = core.PipeSegment()
        # Check that nodes dict is empty before function runs
        self.assertDictEqual(self.network.nodes, dict())

        self.network.add_details(focus, ['end', 'A'])

        self.assertIsInstance(self.network.nodes['A'], core.Node)
        self.assertIs(self.network.nodes['A'], focus.end)
        self.assertIs(self.network.nodes['A'].inputs[0], focus)

    def test_add_details_seg_end_old(self):
        '''Tests method of core.Network: add_details.

        Tests that add_details method correctly handles the situation
        where the details reference a node that already exists. This
        test is against adding a segment end.
        '''
        focus = core.PipeSegment()
        # Use nd to make sure that node 'A' doesn't change
        nd = self.network.nodes['A'] = core.Node()

        self.network.add_details(focus, ['end', 'A'])

        self.assertIs(nd, focus.end)
        self.assertIs(nd, self.network.nodes['A'])
        self.assertIs(nd.inputs[0], focus)
        
    def test_add_details_seg_ele(self):
        '''Tests method of core.Network: add_details.

        Tests that add_details correctly handles adding a new element to
        a core.PipeSegment.
        '''
        focus = dummy_classes.PipeSegmentTest()
        input_list = ['element', 'param1', 'param2']

        self.network.add_details(focus, input_list)

        # Test that add_ele was called on focus
        self.assertIs(focus.add_ele_val, input_list)

    def test_add_details_node(self):
        '''Tests adding node with method of core.Network: add_details.'''
        focus = dummy_classes.NodeTest()
        input_list = ['head', '10', 'feet']

        self.network.add_details(focus, input_list)

        self.assertIs(focus.add_details_val, input_list)

    def test_solve(self):
        '''Tests method of core.Network: solve.'''
        self.solve_network = dummy_classes.DummyNetworkSolve()

        self.solve_network.solve()

        solve_solution = list(self.solve_network.segments) # See dummy class
        self.assertListEqual(solve_solution, [2, 1])

        del self.solve_network

    def test__find_unknowns(self):
        '''Tests method core.Network: _find_unknowns'''
        # Create network elements
        self.network.nodes['A'] = core.Node()
        self.network.segments['1'] = core.PipeSegment()
        self.network.nodes['B'] = core.Node()

        # Setup network connections
        self.network.nodes['A'].outputs.append(self.network.segments['1'])
        self.network.nodes['B'].inputs.append(self.network.segments['1'])
        self.network.segments['1'].start = self.network.nodes['A']
        self.network.segments['1'].end = self.network.nodes['B']

        # Set knowns
        self.network.nodes['A'].head = 10.0 * ureg.feet
        self.network.nodes['B'].head = 5.0 * ureg.feet

        # Run the method
        self.network._find_unknowns()

        self.assertEqual(len(self.network.unknowns), 1)
        self.assertEqual(self.network.unknowns[0],
                      self.network.segments['1'].set_val)

    def test__set_unknowns(self):
        '''Tests method of core.Network: _set_unknowns.'''
        test_list = list()
        self.network.unknowns = [test_list.append]

        self.network._set_unknowns([5.3])

        self.assertAlmostEqual(5.3, test_list[0], places = 3)

    def test_get_errors(self):
        '''Tests method of core.Network: get_errors.'''
        seg = self.network.segments['1'] = dummy_classes.PipeSegmentTest()
        node_A = self.network.nodes['A'] = core.Node()
        node_B = self.network.nodes['B'] = core.Node()

        seg.start = node_A
        seg.end = node_B
        node_A.outputs.append(seg)
        node_B.inputs.append(seg)

        # Have to use plain numbers without units with all of these to
        # avoid issues with incompatible UnitRegistrys.
        node_A.head = 100
        node_A.outflow = 0
        node_B.head = 50
        node_B.outflow = 0
        seg.flow = 10

        errors = self.network.get_errors()

        self.assertEqual(errors[0], -40)
        self.assertEqual(abs(errors[1]), 10)
        self.assertEqual(abs(errors[2]), 10)

    def test__attempt_solution(self):
        '''Tests method of core.Network: _attempt_solution

        This test will fail if _set_unknowns is functioning incorrectly.
        '''
        test_list = list()
        self.network.unknowns = [test_list.append]
        self.network.get_errors = lambda : 5

        test_errors = self.network._attempt_solution([6.3])

        self.assertAlmostEqual(6.3, test_list[0], places=3)
        self.assertEqual(test_errors, 5)

class PipeSegmentTestCase(unittest.TestCase):
    '''Runs unit tests on all methods of PipeSegment class'''
    def setUp(self):
        self.seg = core.PipeSegment()
    def tearDown(self):
        del self.seg

    def test___init__(self):
        '''Checks that PipeSegment objects are properly created'''
        self.assertListEqual(self.seg.elements, list())
        self.assertIs(self.seg.start, None)
        self.assertIs(self.seg.end, None)
        self.assertIs(self.seg.flow, None)

    def test_set_val(self):
        '''Tests method of PipeSegment: set_val'''
        self.seg.set_val(10)
        self.assertEqual(self.seg.flow.m, 10)

    def test_add_ele(self):
        '''Tests method of PipeSegment: add_ele.

        This test uses the special Null_Element class located in pipey.element_classes.
        '''
        self.seg.add_ele(['Null_Element', '1', '2', '3'])
        self.assertEqual(len(self.seg.elements), 1)
        self.assertIsInstance(self.seg.elements[0],
                              pipey.element_classes.Null_Element)
        self.assertListEqual(self.seg.elements[0].stuff, ['1','2','3'])

    def test_calculate_loss(self):
        '''Tests method of PipeSegment: calculate_loss.
        
        Since dummy_classes.DummyElement calculate_loss method returns
        its input, and PipeSegment.calculate_loss sums output of
        calculate_loss methods for PipeSegment.elements, the losses
        returned should be len(PipeSegment.elements) * PipeSegment.flow.
        '''
        self.seg.flow = 2 * ureg.gallons / ureg.minutes

        for elements_len in range(1,10):
            self.seg.elements = [dummy_classes.DummyElement()] * elements_len
            losses = self.seg.calculate_loss()
            self.assertEqual(losses, elements_len * self.seg.flow)

class NodeTestCase(unittest.TestCase):
    '''Runs unit tests for Node class.'''
    def setUp(self):
        self.node = core.Node()
    def tearDown(self):
        del self.node

    def test___init__(self):
        '''Tests initialization of Node object.'''
        self.assertListEqual(self.node.inputs, list())
        self.assertListEqual(self.node.outputs, list())
        self.assertIs(self.node.head, None)
        self.assertEqual(self.node.outflow.m, 0)

    def test_set_val(self):
        '''Tests set_val method of Node class.'''
        self.node.set_val(5)
        self.assertEqual(self.node.head.m, 5)
        self.assertEqual(self.node.head.u, ureg.feet)

    def test_add_details(self):
        '''Tests adding method add_details of Node class.'''
        self.node.add_details(['head', '2.5', 'meters'])
        self.assertAlmostEqual(self.node.head.m, 2.5, places = 5)
        self.assertEqual(self.node.head.u, ureg.meters)

        self.node.add_details(['outflow', '500', 'gpm'])
        self.assertAlmostEqual(self.node.outflow.m, 500, places = 5)
        self.assertEqual(self.node.outflow.to_base_units().u, ureg.m**3 / ureg.sec)

        self.node.add_details(['inflow', '50', 'gpm'])
        self.assertAlmostEqual(self.node.outflow.m, -50, places = 5)
        self.assertEqual(self.node.outflow.to_base_units().u, ureg.m**3 / ureg.sec)

network_suite = unittest.TestLoader().loadTestsFromTestCase(NetworkTestCase)
seg_suite = unittest.TestLoader().loadTestsFromTestCase(PipeSegmentTestCase)
node_suite = unittest.TestLoader().loadTestsFromTestCase(NodeTestCase)

# This is the test suite imported by __init__.py
suite = unittest.TestSuite()
suite.addTests((network_suite, seg_suite, node_suite,))

