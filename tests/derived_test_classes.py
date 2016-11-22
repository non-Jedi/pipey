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

class PipeSegmentTest(core.PipeSegment):
    def __init__(self):
        self.set_val_val = None
        self.add_ele_val = None
        self.calculate_loss_val = None
    def set_val(self, input_val):
        self.set_val_val = input_val
    def add_ele(self, input_val):
        self.add_ele_val = input_val
    def calculate_loss(self):
        self.calculate_loss_val = True

class NodeTest(core.Node):
    def __init__(self):
        self.set_val_val = None
        self.add_details_val = None
    def set_val(self, input_val):
        self.set_val_val = input_val
    def add_details(self, input_val):
        self.add_details_val = input_val
