from random import random, randint, uniform
import datetime


class RandomUseCase(object):
    @staticmethod
    def time_diff(start, end):
        diff = end - start
        millis = diff.days * 24 * 60 * 60 * 1000
        millis += diff.seconds * 1000
        millis += diff.microseconds / 1000
        return millis

    @staticmethod
    def run():
        print("Running: " + RandomUseCase.__name__)
        print("-----------------------------------------")

        start = datetime.datetime.now()
        for i in range(0, 10000):
            a = randint(0, i)
            b = random()
            c = uniform(0, i)
        end = datetime.datetime.now()

        print(RandomUseCase.time_diff(start, end))



