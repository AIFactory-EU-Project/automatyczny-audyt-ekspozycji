import sys


class Logger:

    def __init__(self, f):
        self.out = sys.stdout
        self.logFile = open(f, 'w')

    def write(self, s):
        self.logFile.write(s)
        self.out.write(s)

    def flush(self):
        self.logFile.flush()
        self.out.flush()

    def __del__(self):
        sys.stdout = self.out
