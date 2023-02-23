import time


class Stopwatch:
    def __init__(self):
        self.start = time.time() * 1000
        self.end = self.start

    def time(self):
        self.end = time.time() * 1000
        return self.end - self.start

    def reset(self):
        self.end = time.time() * 1000
        self.start = self.end
