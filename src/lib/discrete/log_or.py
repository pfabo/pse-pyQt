# -*- coding: utf-8 -*-
from numpy import logical_or

from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_INIT, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Or2(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.box = QRectF(0, 0, 70, 40)
        self.value = 0

        self.addTerminal('A', 1, TERM.IN, QPointF(0, 10))
        self.addTerminal('B', 2, TERM.IN, QPointF(0, 30))
        self.addTerminal('Y', 3, TERM.OUT, QPointF(70, 20))

    def drawShape(self, gc):
        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.moveTo(0, 10)
        path.lineTo(12, 10)
        path.moveTo(0, 30)
        path.lineTo(12, 30)

        path.moveTo(60, 20)
        path.lineTo(70, 20)
        gc.drawPath(path)

        path.moveTo(10, 0)
        path.lineTo(17, 0)
        path.arcTo(-7, 0, 70, 70, 90, -63)

        path.moveTo(10, 40)
        path.lineTo(17, 40)
        path.arcTo(-7, -30, 70, 70, -90, 63)

        path.moveTo(10, 0)
        path.arcTo(-65, -20, 80, 80, 30, -60)

        gc.drawPath(path)

    def sim(self, flag, value, time, step):
        if (flag == SIM_INIT) or (flag == SIM_UPDATE):
            a = self.terminal[1].value
            b = self.terminal[2].value
            self.terminal[3].value = logical_or(a, b)
