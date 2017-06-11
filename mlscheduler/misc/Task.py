class Task(object):
    def __init__(self):
        self.__length = []
        self.__index = None
        self.__processor = None

    def get_length(self, processor):
        return self.__length[processor]

    def set_length(self, processor, time):
        self.__length.insert(processor, time)

    def set_index(self, index):
        self.__index = index

    def set_processor(self, processor):
        self.__processor = processor

    def __str__(self):
        return str(self.__index) + '; ' + str(self.__processor)
