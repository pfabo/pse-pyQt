# -*- coding: utf-8 -*-
from numpy import zeros, floor, ndarray

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Fmodulo(Component):
    '''
    @if English

    @endif

    @if Slovak

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'fmodulo.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Amplitude', 1, False, QPointF(40, 0), Color.black, True)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        u = self.terminal[1].value

        m = self.parameter['Amplitude'].value

        if type(u) == ndarray:
            out = zeros(len(u))
            for i in range(len(u)):
                out[i] = u[i] - 0.5 * m - m * \
                    floor((u[i] - 0.5 * m) / m) - 0.5 * m
        else:
            out = u - 0.5 * m - m * floor((u - 0.5 * m) / m) - 0.5 * m

        self.terminal[2].value = out


class FmoduloB(Component):
    '''
    @if English

    @endif

    @if Slovak

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'fmodulob.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Amplitude', 1, False, QPointF(40, 0), Color.black, True)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        u = self.terminal[1].value

        m = self.parameter['Amplitude'].value

        if type(u) == ndarray:
            out = zeros(len(u))
            for i in range(len(u)):
                out[i] = u[i] - m * floor(u[i] / m)
        else:
            out = u - m * floor(u / m)

        self.terminal[2].value = out


class FmoduloC(Component):
    '''
    @if English

    @endif

    @if Slovak

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'fmoduloc.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Amplitude', 1, False, QPointF(40, 70), Color.black, True)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        u = self.terminal[1].value

        m = self.parameter['Amplitude'].value

        if type(u) == ndarray:
            out = zeros(len(u))
            for i in range(len(u)):
                out[i] = u[i] - m * int(u[i] / m)
        else:
            out = u - m * int(u / m)

        self.terminal[2].value = out
