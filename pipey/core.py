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
from . import ureg # pint.UnitRegistry shared with rest of package
from scipy import optimize

class Network:
    '''The entire network of pipes'''

    def __init__(self):
        self.segments = dict() #this will hold all PipeSegments in the Network
        self.nodes = dict() #this will hold all Nodes in the Network
        self.fluid = Fluid()

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
            elif line_args[0] == 'fluid':
                current_focus = self.fluid
            else:
                # Can't have the add_details method on focus method
                # because adding start and end nodes to PipeSegments
                # requires referencing Network.nodes
                self.add_details(current_focus, line_args)

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

        else: # Both Nodes and Fluids have add_details method
            focus.add_details(line_args)

    def solve(self):
        '''Solves flows and heads for network of PipeSegments and Nodes.
        Method doesn't return anything but sets all PipeSegment.flow
        values and Node.head values to their correct value.'''

        sol = optimize.root(self._attempt_solution, [0]*len(self.unknowns), 
                            method = 'hybr')
        if sol.success:
            self._set_unknowns(sol.x)
        else:
            raise Warning

    def _find_unknowns(self):
        '''Iterates through both self.segments and self.nodes and
        creates a list of all values that are currently set as None
        type.
        
        This method should only be called once for a given Network
        object. If called a second time, self.unknowns will be set to
        an empty list and Network will be unable to be solved.'''

        self.unknowns = list()

        for seg_name in self.segments:
            if self.segments[seg_name].flow is None:
                self.unknowns.append(self.segments[seg_name].set_val)

        for node_name in self.nodes:
            if self.nodes[node_name].head is None:
                self.unknowns.append(self.nodes[node_name].set_val)

    def _set_unknowns(self, new_vals):
        '''Iterates through the list of unknowns and sets each one to
        the value specified in new_vals'''

        for method, val in zip(self.unknowns, new_vals):
            method(val)

    def get_errors(self):
        '''Returns a list-like object with all errors in pressure drop
        equations and continuity equations (in that order)'''
        # Error for a segment is the difference between the node head
        # difference and its own pressure drop
        seg_errors = [self.segments[i].end.head 
                      + self.segments[i].calculate_loss() 
                      - self.segments[i].start.head 
                      for i in self.segments]

        # Error for a node is the difference between the node's inputs
        # and outputs (including inflows and outflows)
        node_errors = [0]*len(self.nodes)
        for i,n in enumerate(self.nodes):
            n = self.nodes[n]
            inputs = sum((pipe.flow for pipe in n.inputs))
            outputs = sum((pipe.flow for pipe in n.outputs))
            node_errors[i] = inputs - outputs - n.outflow

        return seg_errors + node_errors

    def _attempt_solution(self, new_vals):
        '''Helper method that sets unknown values to new_vals and
        returns the error terms for the object.'''

        self._set_unknowns(new_vals)
        return self.get_errors()

class PipeSegment:
    '''A piping segment running between nodes'''

    def __init__(self):
        self.elements = list() #holds all elements of the segment
        self.start = None
        self.end = None
        self.flow = None

    # This method exists so that PipeSegment and Node can be treated the
    # same way by Network._find_unknowns and Network._set_unknowns
    def set_val(self, new_flow):
        '''Sets flow attribute to new_flow'''
        self.flow = new_flow * ureg.gallons / ureg.minutes

    def add_ele(self, attributes):
        '''General method for instantiating element objects in the
        segment. `attributes` is a list-like object containing [0] the
        name of the element and [1+] parameters for the given
        element.'''

        self.elements.append(getattr(element_classes, attributes[0])(attributes[1:]))

    def calculate_loss(self):
        '''Calculates the total head loss across the segment for a given
        flowrate'''

        return sum([element.calculate_loss(self.flow) 
                    for element in self.elements])


class Node:
    '''The point at which PipeSegments connect'''

    def __init__(self):
        self.inputs = list() #holds all segments that flow into Node
        self.outputs = list() #holds all segments that flow out of Node
        self.head = None
        self.outflow = 0 * ureg.gallons / ureg.minutes

    # This method exists so that PipeSegment and Node can be treated the
    # same way by Network._find_unknowns and Network._set_unknowns
    def set_val(self, new_head):
        '''Sets head attribute to new_head'''
        self.head = new_head * ureg.feet

    def add_details(self, attributes):
        '''General method for adding attributes of the node'''

        if attributes[0] == 'head':
            self.head = float(attributes[1]) * ureg.parse_expression(attributes[2])
        elif attributes[0] == 'outflow':
            self.outflow = float(attributes[1]) * ureg.parse_expression(attributes[2])
        elif attributes[0] == 'inflow':
            self.outflow = -float(attributes[1]) * ureg.parse_expression(attributes[2])

class Fluid:
    '''Fluid class contains the properties of the fluid such as density
    and viscosity. The fluid may return different properties given
    different base states'''

    def __init__(self):
        self.density = None
        self.viscosity = None

    def add_details(self, args):
        '''Given a properly formatted list-like object, changes
        attributes of fluid to match the given args.'''

        pass
