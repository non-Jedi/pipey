<!---

Copyright 2016 Adam Beckmeyer

This file is part of Pipey.

Pipey is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your
option) any later version.

Pipey is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License along
with Pipey.  If not, see <http://www.gnu.org/licenses/>.  

--> 

# Pipey

Simple python package for calculating pressure drop through pipes and
fittings.

## Status

Unmaintained, unfinished and unusable. I hope to return to this package again at
a later time, but it is not a priority for me right now.

## Input format

Pipey reads text files (which may have the filename extension .pipey).
The first token (tokens are separated by a single space) on the first
line of a text block denotes the object the text block describes
(segment or node). The second token (may be only a character) denotes
the name of the object. For simple cases, a convention of a single
number for segments and single capital letter for nodes should be
used.

The rest of a object's text block follows a convention where the first
token in a line calls a property of the object by name and the
remainder of the line describes values of that property.

The convention is that capitalized property names indicate some
element of a pipe segment through which fluid may flow (such as
"Pipe", "Orifice", or "Elbow")

### Segment Properties

#### Non-element properties

##### start

The "start" property of a segment is a node to which the segment is
connected. Any directionally specified properties shall be assumed to
be moving from "start".

##### end

The "end" property of a segment is the other node to which a segment
is connected. Any directionally specified properties shall be assumed
to be moving to "end".

#### Element properties

At this time, the only available element properties are those included
with the pipey package. A planned feature of the project's
architecture is to allow allow custom piping elements, but it has not
yet been implemented.

##### Pipe

Pipe describes a straight length of pipe or tubing. 

* The tag "-s" indicates that the next token will be the pipe
	element's numerical schedule (schedule 40, schedule 80, etc.).
* The tag "-l" indicates that the next two tokens will be interpreted
	as the pipe element's numerical length followed by the units used
	(feet, in, m, meters, etc.).
* The tag "-d" indicates that the next two tokens will be interpreted
	as the element's nominal diameter followed by the unit used.
* The tag "-D" indicates that the next two tokens will be interpreted
	as the element's inner diameter followed by the unit used.
	
### Node Properties

#### head

The head property of a node indicates the pressure head available at
the node. If this is not specified it will be assumed to be unknown.
The two tokens immediately after head should be the quantity and units
of head (eg. "head 40 feet").

### outflow

The outflow property of a node indicates the amount of fluid flowing
out of the system from the node. The first token after outflow should
be the quantity and the second token should be the units.

If this quantity is unknown please see the _unknown_ property.

### inflow

The inflow property of a node indicates the amount of fluid flowing
into the system at a node. The first token after outflow should be the
quantity and the second token should be the units.

If this quantity is unknown please see the _unknown_ property.

### unknown

#### outflow

If the first token after unknown is outflow pipey will assume that a
node's outflow is equal to its input flows minus its output flows.
This is useful if there is a tank accumulating fluid at a node.
