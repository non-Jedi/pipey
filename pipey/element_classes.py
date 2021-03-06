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

import csv
import math
from . import ureg

class Element:
    '''General class for pipe elements to inherit from'''

    units = 0
    diameter = 1

class Null_Element(Element):
    '''Special class that puts all input into stuff attribute.

    This class is useful for testing purposes but should not be called
    at any point in the package's actual codebase.
    '''
    def __init__(self, attributes):
        self.stuff = attributes

class Pipe(Element):
    '''Total of all piping runs in segment'''

    def __init__(self, attributes):
        self.length = attributes[0]
        self.diameter = calculate_diameter(attributes[1:3])

    #need to review code to see how information about density and viscosity best passed
    def calculate_loss(self, flow, density, viscosity):
        '''calculates the head loss for a given flowrate'''
        #flow in gpm, diameter in inches output in ft/sec
        velocity = 60*0.13368*flow/((self.diameter/24)**2*math.pi())
        #diameter in inches, velocity in ft/sec, density in lb/ft3, viscosity in cP
        #validate the unit conversions in this formula!
        reynolds = (self.diameter*velocity*density/viscosity)/12/6.8948/144
        
    def calculate_diameter(self, sched, nom_diam):
        '''Calculates internal diameter of pipe for a given nominal diameter'''

        sizes = dict()
        with open(os.path.join(os.path.abspath(__file__), 'data/pipe_size.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                if csv_reader.line_num == 1: #first line is just the labels
                    index = [str(i) for i in line] #make sure index has correct type
                else: #Each column is wall thickness at a specific schedule
                    sizes[line[0]] = dict(zip(index[1:], line[1:]))

        return float(sizes[nom_diam][sched])
