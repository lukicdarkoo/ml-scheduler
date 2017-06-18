class Processor(object):
    def __init__(self, capacity, index):
        self.tasks = []
        self.capacity = capacity
        self.index = index

    def clear(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def get_last_task(self):
        if len(self.tasks) > 0:
            return self.tasks[len(self.tasks) - 1]
        return None

    def __str__(self):
        return 'p' + str(self.index + 1)

