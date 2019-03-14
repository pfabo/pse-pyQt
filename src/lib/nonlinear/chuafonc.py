# -*- coding: utf-8 -*-
from numpy import ndarray, zeros

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Chuafonc(Component):
    '''
    @if English

    Chua's nonlinear function block

    @endif

    @if Slovak

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'chuafonc.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('m0', -1.1428571, False, QPointF(40, 70), Color.black, True)
        self.addParameter('m1', -0.7142857, False, QPointF(40, 85), Color.black, True)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        inp = self.terminal[1].value

        m0 = self.parameter['m0'].value
        m1 = self.parameter['m1'].value

        if type(inp) == ndarray:
            out = zeros(len(inp))
            for i in range(len(inp)):
                out[i] = m1 * inp[i] + 0.5 * (
                    m0 - m1) * (abs(inp[i] + 1) - abs(inp[i] - 1))
        else:
            out = m1 * inp + 0.5 * (m0 - m1) * (abs(inp + 1) - abs(inp - 1))

        self.terminal[2].value = out
