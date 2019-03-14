# -*- coding: utf-8 -*-

from numpy import ndarray

from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImportimport numpy
from terminal import TERM


class LedBig(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(-10, -10, 60, 60)

        self.addTerminal('IN', 1, TERM.IN, QPointF(-10, 20),
                         TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)

        self.value = False

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, 0, 0, 20)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.khaki)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-5, -5, 50, 50, 5, 5)

        path = QPainterPath()
        if self.value > 0:
            gc.setBrush(QBrush(Color.limeGreen))
        else:
            gc.setBrush(QBrush(Color.red))

        path.addEllipse(0, 0, 40, 40)
        gc.drawPath(path)

    def sim(self, flag, value, time, step):
        if flag == SIM_UPDATE:
            inp = self.terminal[1].value
            if type(inp) == ndarray:
                self.value = inp[0]
            else:
                self.value = inp
