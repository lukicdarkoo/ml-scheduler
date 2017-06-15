class Task(object):
    def __init__(self, length, index=None):
        self.length = length
        self.index = index

        # Temporary values
        self.st = None         # Start execution time
        self.ft = None         # Finish execution time
        self.processor = None  # Processor
        self.processed = False

    def __str__(self):
        return 'v' + str(self.index + 1) + '; ' + str(self.length)
