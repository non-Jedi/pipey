from . import element_classes

class Network:
    '''The entire network of pipes'''

    def __init__(self):
        self.segments = list() #this will hold all PipeSegments in the Network
        self.nodes = list() #this will hold all Nodes in the Network

    def load(self, filename):
        '''Creates a list of PipeSegments and Nodes from information in filename'''

        with f as open(filename, 'r'):
            for line in f:
                list_line = line.split() #much easier to work list for this
                if list_line: #Check to make sure not empty line
                    #For every line with the 'segment' or 'node' label create a new
                    #object and set as the object currently being modified
                    if list_line[0] == 'segment':
                        self.segments.append(PipeSegment(list_line[1]))
                        current = self.segments[-1]
                    elif list_line[0] == 'node':
                        self.nodes.append(Node(list_line[1]))
                        current = self.nodes[-1]
                    elif list_line[0] in ('start', 'stop'):
                        #Check if the given start/stop node has already been instantiated
                        try:
                            current_node = self.nodes[[node.name for node in self.nodes].index(list_line[1])]
                        except ValueError:
                            self.nodes.append(Node(list_line[1]))
                            current_node = self.nodes[-1]
                        #make node aware of segment and segment aware of node
                        setattr(current, list_line[0], current_node)
                        if list_line[0] == 'start':
                            current_node.outputs.append(current)
                        elif list_line[0] == 'stop':
                            current_node.inputs.append(current)
                    else:
                        #add element to segment or node
                        current.add(list_line)

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

    def __init__(self, name):
        self.name = name
        self.elements = list() #holds all elements of the segment

    def add(self, attributes):
    '''General method for instantiating element objects in the segment'''

        self.elements.append(getattr(element_classes, attributes[0])(attributes[1:]))

    def calculate_loss(self, flow):
    '''Calculates the total head loss across the segment for a given flowrate'''

        return sum([element.calculate_loss(flow) for element in elements])


class Node:
    '''The point at which PipeSegments connect'''

    def __init__(self, name):
        self.name = name
        self.inputs = list() #holds all segments that flow into Node
        self.outputs = list() #holds all segments that flow out of Node

    def add(self, attributes):
    '''General method for adding attributes of the node'''

        if attributes[0] == 'head':
            self.head = attributes[1]
        elif attributes[0] == 'outflow'
            self.outflow = attributes[1]
        elif attributes[0] == 'inflow'
            self.outflow = -attributes[1]
