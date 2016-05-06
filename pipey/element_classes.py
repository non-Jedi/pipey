
class Element:
'''General class for pipe elements to inherit from'''

    units = 0
    diameter = 1

class Pipe(Element):
'''Total of all piping runs in segment'''

    def __init__(self, attributes):
        self.units = attributes[0]
        try:
            self.diameter = attributes[attributes.index('diameter')+1]
        except ValueError:
            pass

    def calculate_loss(self, flow):
    '''calculates the head loss for a given flowrate'''
        
        return 5
