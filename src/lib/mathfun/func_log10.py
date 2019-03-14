from numpy import log10

from .func_base import FunctionBase


class Log10(FunctionBase):

    def __init__(self, name, pos):
        FunctionBase.__init__(self, name, pos)
        self.shapeImage = 'log.svg'

    def sim(self, flag, value, time, step):
        # ToDo - kontrola hodnoty, chybove hlasenie
        inp = self.terminal[1].value

        out = log10(inp)
        self.terminal[2].value = out
