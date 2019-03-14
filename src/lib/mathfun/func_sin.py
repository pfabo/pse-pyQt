# from component import *
# from terminal import *
from numpy import sin

from .func_base import FunctionBase


class Sin(FunctionBase):

    def __init__(self, name, pos):
        FunctionBase.__init__(self, name, pos)
        self.shapeImage = 'sin.svg'

    def sim(self, flag, value, time, step):
        inp = self.terminal[1].value
        self.terminal[2].value = sin(inp)
