# -*- coding: utf-8 -*-
from numpy import *  # global import due to eval @UnusedWildImport

from color import Color
from lib.mathfun.func_base import FunctionBase


class FuncEval(FunctionBase):
    """!
    @if English

    @endif

    @if Slovak

    Nastavenie výstupu podľa hodnoty výrazu.

    Výraz musí byť syntakticky správny podľa pravidiel jazyku python. Vstupná hodnota
    môže byť skalárna alebo vektorová.

    @endif
    """

    def __init__(self, name, pos):
        FunctionBase.__init__(self, name, pos)

        self.shapeImage = 'func.svg'
        self.addParameter('f(x)', '4*sin(x)+x', visibleName=True)

    def sim(self, flag, value, time, step):
        try:
            x = self.terminal[1].value
            out = eval(self.parameter['f(x)'].value)
            self.terminal[2].value = out
        except Exception as err:
            self.shapeFillColor = Color.red
            self.terminal[2].value = 0
            print('>>> Error in FuncEval, Ref =', self.parameter['Ref'].value)
            print('    Error in the evaluation of expressions, x =', x)
            print('    Exception:', err)
