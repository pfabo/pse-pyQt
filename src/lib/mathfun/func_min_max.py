# -*- coding: utf-8 -*-
from numpy import inf, ndarray

from color import Color
from componenttypes import SIM_INIT
from lib.pseqt import *  # @UnusedWildImport

from .func_base import FunctionBase


class Min(FunctionBase):
    '''!
    @if English

    @endif

    @if Slovak

    Minimalna hodnota vstupnej hodnoty. Ak je vstupná hodnota vektor,
    berie sa minimálna hodnota z položiek vektora.

    @endif
    '''
    def __init__(self, name, pos):
        FunctionBase.__init__(self, name, pos)
        self.shapeImage = 'min.png'

        self.minValue = 1e38

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.yellow)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -10)

    def sim(self, flag, value, time, step):

        inp = self.terminal[1].value

        if flag == SIM_INIT:
            self.minValue = 1e38
        else:
            if (type(inp) == ndarray) or (type(inp) == list):
                value = min(inp)
            else:
                value = inp

            if value < self.minValue:
                self.minValue = value

            self.terminal[2].value = self.minValue


class Max(FunctionBase):
    '''!
    @if English

    @endif

    @if Slovak

    Maximalna hodnota vstupnej hodnoty.

    @endif
    '''
    def __init__(self, name, pos):
        FunctionBase.__init__(self, name, pos)
        self.shapeImage = 'max.png'

        self.maxValue = -1e38

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.yellow)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -25, -10)

    def sim(self, flag, value, time, step):
        inp = self.terminal[1].value

        if flag == SIM_INIT:
            self.maxValue = -1e38
        else:
            if (type(inp) == ndarray) or (type(inp) == list):
                value = max(inp)
            else:
                value = inp

            if value > self.maxValue:
                self.maxValue = value

            self.terminal[2].value = self.maxValue


class Ratio(FunctionBase):
    '''!
    @if English

    @endif

    @if Slovak

    Prevrátená hosnota vstupnej hodnoty, f(x)=1/x.

    V prípade nulovej vstupnej hodnoty je výstupom +/- inf.

    @endif
    '''
    def __init__(self, name, pos):
        FunctionBase.__init__(self, name, pos)
        self.shapeImage = 'ratio.png'

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.yellow)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -10)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[2].value = 0.0
        else:
            #if (type(inp) == numpy.ndarray) or (type(inp) == list):
            #    value = max(inp)
            #else:
            try:
                inp = self.terminal[1].value
                self.terminal[2].value = 1.0 / inp
            except:
                self.terminal[2].value = inf
