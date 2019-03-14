
from numpy import abs

from .func_base import FunctionBase


class Abs(FunctionBase):

    def __init__(self, name, pos):
        FunctionBase.__init__(self, name, pos)
        self.shapeImage = 'abs.svg'

    def sim(self, flag, value, time, step):
        inp = self.terminal[1].value
        self.terminal[2].value = abs(inp)
