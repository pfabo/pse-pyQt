from numpy import log

from .func_base import FunctionBase


class Ln(FunctionBase):

    def __init__(self, name, pos):
        FunctionBase.__init__(self, name, pos)
        self.shapeImage = 'ln.svg'

    def sim(self, flag, value, time, step):
        # ToDo kontrola hodnoty, chybove hlasenie
        inp = self.terminal[1].value
        self.terminal[2].value = log(inp)
