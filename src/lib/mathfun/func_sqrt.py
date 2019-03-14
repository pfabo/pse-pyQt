from numpy import sqrt

from .func_base import FunctionBase


class Sqrt(FunctionBase):

    def __init__(self, name, pos):
        FunctionBase.__init__(self, name, pos)
        self.shapeImage = 'sqrt.svg'

    def sim(self, flag, value, time, step):
        inp = self.terminal[1].value
        self.terminal[2].value = sqrt(inp)
