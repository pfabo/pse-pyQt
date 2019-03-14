# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Logistic(Component):
    '''
    @if English

    2D bifurcation of the logistic map

    @endif

    @if Slovak

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'logistic.svg'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN1', 1, TERM.IN, QPointF(-30, -10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('IN2', 2, TERM.IN, QPointF(-30, 10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 3, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

    def drawShape(self, gc):

        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[3].value = 0.7

        elif flag == SIM_UPDATE:
            in1 = self.terminal[1].value
            in2 = self.terminal[2].value
            self.terminal[3].value = 4 * in1 * in2 * (1 - in2)
