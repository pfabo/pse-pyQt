from .func_base import FunctionBase


class Pow2(FunctionBase):

    def __init__(self, name, pos):
        FunctionBase.__init__(self, name, pos)
        self.shapeImage = 'pow2.svg'

    def sim(self, flag, value, time, step):
        inp = self.terminal[1].value
        self.terminal[2].value = inp * inp
