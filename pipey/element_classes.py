import csv

class Element:
    '''General class for pipe elements to inherit from'''

    units = 0
    diameter = 1

class Pipe(Element):
    '''Total of all piping runs in segment'''

    def __init__(self, attributes):
        self.length = attributes[0]
        self.diameter = calculate_diameter(attributes[1:3])

    def calculate_loss(self, flow):
        '''calculates the head loss for a given flowrate'''
        
    def calculate_diameter(self, sched, nom_diam):
        '''Calculates internal diameter of pipe for a given nominal diameter'''

        f = open('
