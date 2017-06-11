import unittest
from mlscheduler.misc.Task import Task


class TaskTest(unittest.TestCase):
    def setUp(self):
        self.task = Task()

    def testTimeToFinish(self):
        self.task.set_length(0, 10)
        self.assertEqual(self.task.get_length(0), 10)
