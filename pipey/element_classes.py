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

        sizes = dict()
        with open(os.path.join(os.path.abspath(__file__), 'data/pipe_size.csv'), 'r') as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                if csv_reader.line_num == 1: #first line is just the labels
                    index = [str(i) for i in line] #make sure index has correct type
                else: #Each column is wall thickness at a specific schedule
                    sizes[line[0]] = dict(zip(index[1:], line[1:]))

        return float(sizes[nom_diam][sched])
