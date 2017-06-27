class Processor(object):
    def __init__(self, capacity, index):
        self.capacity = capacity
        self.index = index

    def __str__(self):
        return 'Processor[' + str(self.index + 1) + ']'

