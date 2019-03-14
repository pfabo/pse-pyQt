from numpy import cos

from .func_base import FunctionBase


class Cos(FunctionBase):

    def __init__(self, name, pos):
        FunctionBase.__init__(self, name, pos)
        self.shapeImage = 'cos.svg'

    def sim(self, flag, value, time, step):
        inp = self.terminal[1].value
        self.terminal[2].value = cos(inp)
