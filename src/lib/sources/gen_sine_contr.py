# -*- coding: utf-8 -*-
from numpy import sin, pi

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class GenSineContr(Component):
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'gensine.svg'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.addTerminal('AMP', 2, TERM.IN, QPointF(-30, -10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('FRQ', 3, TERM.IN, QPointF(-30, 10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

    def drawShape(self, gc):

        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.green)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        ampl = self.terminal[2].value
        f = self.terminal[3].value
        self.terminal[1].value = ampl * sin(2 * pi * f * time)
