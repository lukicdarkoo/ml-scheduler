class Task(object):
    def __init__(self, processor=0, time=1):
        self.__length = []
        self.__name = ''
        self.set_length(processor, time)

    def get_length(self, processor):
        return self.__length[processor]

    def set_length(self, processor, time):
        self.__length.insert(processor, time)

    def set_name(self, name):
        self.__name = name

    def __str__(self):
        return self.__name
