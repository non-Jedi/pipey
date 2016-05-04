'''Main code defining classes and methods of calculating pipe network'''

class Network:
    '''The entire network of pipes'''

    def __init__(self):
        self.segments = dict()
        self.nodes = dict()

    def load(self, filename):
        '''Creates a list of PipeSegments and Nodes from information in filename'''

        with f as open(filename, 'r'):
            for line in f:
                if line: #Check to make sure not empty line
                    #For every line with the 'segment' or 'node' label create a new
                    #object and set as the object currently being modified
                    if line.split()[0] == 'segment':
                        self.segments[line.split()[-1]] = PipeSegment(line.split()[-1])
                        current = self.segments[line.split()[-1]]
                    elif line.split()[0] == 'node':
                        self.nodes[line.split()[-1]] = Node(line.split()[-1])
                        current = self.nodes[line.split()[-1]]
                    else:
                        #add element to segment or node
                        current.add(line.split())


class PipeSegment:
    '''A piping segment running between nodes'''

    def __init__(self, name):
        self.name = name
        self.element


class Node:
    '''The point at which PipeSegments connect'''

    def __init__(self, name):
        self.name = name
