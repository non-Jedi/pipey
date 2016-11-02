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

from . import element_classes
from . import utils
from pint import UnitRegistry

class Network:
    '''The entire network of pipes'''

    def __init__(self):
        self.segments = dict() #this will hold all PipeSegments in the Network
        self.nodes = dict() #this will hold all Nodes in the Network

    def load(self, filename):
        '''Reads in the contents of filename and converts them into a
        list-like object'''

        with open(filename, 'r') as f:
            file_list = [i.strip().split(sep=' ') for i in f]

        #This script checks that the input is formatted according to the rules.
        utils.check_formatting(file_list)

        self.parse(file_list)

    def parse(self, input_list):
        '''Given a list-like object generated by the load method, parse
        attempts to populate self.segments and self.nodes with the
        parameters specified in the input file.
        
        The results of this parsing will be appended to self.segments
        and self.nodes.'''

        # Iterate through entire list to make sure all file contents
        # added to object.
        for line_args in input_list:

            # Since the input was already validated, we don't need to
            # worry about invalid input here.
            if not line_args[0]: # Checks for empty line in input
                current_focus = None
            elif line_args[0] == 'segment':
                current_focus = self.add_seg(line_args)
            elif line_args[0] == 'node':
                current_focus = self.add_node(line_args)
            else:
                self.add_details(line_args)

    def add_seg(self, args):
        '''Adds piping segment to Network object as specified by
        arguments contained in args.'''

        self.segments[args[1]] = PipeSegment()
        return self.segments[args[1]]

    def add_node(self, args):
        '''Adds node between pipe intersections as specified by
        arguments contained in args.'''

        self.nodes[args[1]] = Node()
        return self.nodes[args[1]]

    def add_details(self, focus, line_args):
        '''When passed a PipeSegment object or Node object and a
        list-like object describing some aspect of the segment or node,
        this method modifies the node or segment.'''

        if isinstance(focus, PipeSegment):
            # The 'start' and 'end' keywords are special and must be
            # handled outside of the PipeSegment class
            if line_args[0] == 'start':
                # Instantiate Node object if not yet created
                if line_args[1] not in self.nodes:
                    self.nodes[line_args[1]] = Node()
                focus.start = self.nodes[line_args[1]]
                # Must keep node inputs and outputs separate so that the
                # dimensionality of flow has meaning
                self.nodes[line_args[1]].outputs.append(focus)

            elif line_args[0] == 'end':
                # Instantiate Node object if not yet created
                if line_args[1] not in self.nodes:
                    self.nodes[line_args[1]] = Node()
                focus.end = self.nodes[line_args[1]]
                # Must keep node inputs and outputs separate so that the
                # dimensionality of flow has meaning
                self.nodes[line_args[1]].inputs.append(focus)
            else:
                focus.add_ele(line_args)

        elif isinstance(focus, Node):
            focus.add_details(line_args)

    def get_error(self, values):
        '''Returns the error present in each equation for the given values

        the length of values corresponds to the sum of PipeSegments and Nodes in
        the Network. The first len(Network.segments) values are flows through
        the corresponding segments. The rest are heads at the corresponding nodes.'''

        for i, value in enumerate(values):
            (self.segments+self.nodes)[i].temp_val = value

        segment_errors = [segment.start.head-segment.calculate_loss(segment.temp_val)-segment.stop.head for segment in self.segments]
        node_errors = [node.outflow + sum(node.outputs) - sum(node.inputs) for node in self.nodes]

        return segment_errors+node_errors


class PipeSegment:
    '''A piping segment running between nodes'''

    def __init__(self):
        self.elements = list() #holds all elements of the segment
        self.start = None
        self.end = None

    def add_ele(self, attributes):
        '''General method for instantiating element objects in the segment'''

        self.elements.append(getattr(element_classes, attributes[0])(attributes[1:]))

    def calculate_loss(self, flow):
        '''Calculates the total head loss across the segment for a given flowrate'''

        return sum([element.calculate_loss(flow) for element in elements])


class Node:
    '''The point at which PipeSegments connect'''

    def __init__(self):
        self.inputs = list() #holds all segments that flow into Node
        self.outputs = list() #holds all segments that flow out of Node

    def add_details(self, attributes):
        '''General method for adding attributes of the node'''

        if attributes[0] == 'head':
            self.head = attributes[1]
        elif attributes[0] == 'outflow':
            self.outflow = attributes[1]
        elif attributes[0] == 'inflow':
            self.outflow = -attributes[1]
