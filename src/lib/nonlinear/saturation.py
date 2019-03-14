# -*- coding: utf-8 -*-
from numpy import zeros, ndarray

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Saturation(Component):
    '''Blok saturacie s nastavitelnymi limitnymi hodnotami.'''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'saturation.svg'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Upper limit', 1.0, False, QPointF(0, 30), Color.black, True)
        self.addParameter('Lower limit', -1.0, False, QPointF(0, 45), Color.black, True)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        '''
        Vypocet vystupnej veliciny
        '''
        inp = self.terminal[1].value

        limUpp = self.parameter['Upper limit'].value
        limLow = self.parameter['Lower limit'].value

        if type(inp) == ndarray:
            out = zeros(len(inp))
            for i in range(len(inp)):
                if inp[i] >= limUpp:
                    out[i] = limUpp
                elif inp[i] <= limLow:
                    out[i] = limLow
                else:
                    out[i] = inp[i]
        else:
            out = 0.0
            if inp >= limUpp:
                out = limUpp
            elif inp <= limLow:
                out = limLow
            else:
                out = inp

        self.terminal[2].value = out
