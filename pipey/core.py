'''Main code defining classes and methods of calculating pipe network'''

class Network:
    '''The entire network of pipes'''

    def __init__(self):
        self.segments = dict() #this will hold all PipeSegments in the Network
        self.nodes = dict() #this will hold all Nodes in the Network

    def load(self, filename):
        '''Creates a list of PipeSegments and Nodes from information in filename'''

        with f as open(filename, 'r'):
            for line in f:
                list_line = line.split() #much easier to work list for this
                if list_line: #Check to make sure not empty line
                    #For every line with the 'segment' or 'node' label create a new
                    #object and set as the object currently being modified
                    if list_line[0] == 'segment':
                        self.segments[list_line[-1]] = PipeSegment(list_line[-1])
                        current = self.segments[list_line[-1]]
                    elif list_line[0] == 'node':
                        self.nodes[list_line[-1]] = Node(list_line[-1])
                        current = self.nodes[list_line[-1]]
                    else:
                        #add element to segment or node
                        current.add(list_line)


class PipeSegment:
    '''A piping segment running between nodes'''

    def __init__(self, name):
        self.name = name
        self.element


class Node:
    '''The point at which PipeSegments connect'''

    def __init__(self, name):
        self.name = name
