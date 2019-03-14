# -*- coding: utf-8 -*-
from numpy import ndarray

from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Led(Component):
    '''
    Jednoducha logicka sonda.
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(-15, 0, 35, 20)

        self.addTerminal('IN', 1, TERM.IN, QPointF(-10, 10), TERM.DIR_EAST)

        self.value = 0

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, 0, 0, 20)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.khaki)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(0, 0, 20, 20, 5, 5)

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))
        path.moveTo(-10, 10)
        path.lineTo(0, 10)
        gc.drawPath(path)

        path = QPainterPath()
        if self.value > 0:
            gc.setBrush(QBrush(Color.limeGreen))
        else:
            gc.setBrush(QBrush(Color.red))

        path.addEllipse(4, 4, 12, 12)
        gc.drawPath(path)

    def sim(self, flag, value, time, step):
        if flag == SIM_UPDATE:
            inp = self.terminal[1].value
            if type(inp) == ndarray:
                self.value = inp[0]
            else:
                self.value = inp
