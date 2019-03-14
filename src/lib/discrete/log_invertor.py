# -*- coding: utf-8 -*-

from numpy import logical_not

from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_INIT, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Invertor(Component):
    '''
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.box = QRectF(0, 0, 60, 40)
        self.value = 1

        self.addTerminal('A', 1, TERM.IN, QPointF(0, 20))
        self.addTerminal('Y', 2, TERM.OUT, QPointF(60, 20))

    def drawShape(self, gc):

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.moveTo(0, 20)
        path.lineTo(10, 20)
        path.moveTo(55, 20)
        path.lineTo(60, 20)
        gc.drawPath(path)

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.moveTo(10, 0)
        path.lineTo(45, 20)
        path.lineTo(10, 40)
        path.lineTo(10, 0)
        path.addEllipse(45, 15, 10, 10)
        gc.drawPath(path)

    def sim(self, flag, value, time, step):
        if (flag == SIM_INIT) or (flag == SIM_UPDATE):
            inp = self.terminal[1].value
            self.terminal[2].value = logical_not(inp)
