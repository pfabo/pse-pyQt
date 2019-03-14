# -*- coding: utf-8 -*-
from numpy import ndarray

from component import Component, Color
from componenttypes import *  # @UnusedWildImport
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Led4(Component):
    '''Led indicator 4x'''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(-10, 0, 30, 80)

        self.addTerminal('IN1', 1, TERM.IN, QPointF(-10, 10), TERM.DIR_EAST)
        self.addTerminal('IN2', 2, TERM.IN, QPointF(-10, 30), TERM.DIR_EAST)
        self.addTerminal('IN3', 3, TERM.IN, QPointF(-10, 50), TERM.DIR_EAST)
        self.addTerminal('IN4', 4, TERM.IN, QPointF(-10, 70), TERM.DIR_EAST)

        self.numLed = 4
        self.value = [0, 0, 0, 0]

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor, 0.6))

        for i in range(self.numLed):
            grad = QLinearGradient(0, 0 + i * 20, 0, 20 + i * 20)
            grad.setColorAt(0, Color.white)
            grad.setColorAt(1, Color.khaki)
            gc.setBrush(QBrush(grad))

            gc.drawRoundedRect(0, 0 + i * 20, 20, 20, 5, 5)

            path = QPainterPath()
            gc.setPen(QPen(self.shapeColor))
            path.moveTo(-10, 10 + i * 20)
            path.lineTo(0, 10 + i * 20)
            gc.drawPath(path)

        for i in range(self.numLed):
            path = QPainterPath()
            if self.value[i] is True:
                gc.setBrush(QBrush(Color.limeGreen))
            else:
                gc.setBrush(QBrush(Color.red))
            path.addEllipse(4, 4 + 20 * i, 12, 12)
            gc.drawPath(path)

    def sim(self, flag, value, time, step):
        if flag == SIM_UPDATE:
            inp = self.terminal[1].value
            if type(inp) == ndarray:
                self.value[0] = inp[0]
            else:
                self.value[0] = inp

            inp = self.terminal[2].value
            if type(inp) == ndarray:
                self.value[1] = inp[0]
            else:
                self.value[1] = inp

            inp = self.terminal[3].value
            if type(inp) == ndarray:
                self.value[2] = inp[0]
            else:
                self.value[2] = inp

            inp = self.terminal[4].value
            if type(inp) == ndarray:
                self.value[3] = inp[0]
            else:
                self.value[3] = inp

            # zobrazujeme hodnotu prveho prvku vektora
            # self.value[0] = self.terminal[1].value #[0]
            # self.value[1] = self.terminal[2].value #[0]
            # self.value[2] = self.terminal[3].value #[0]
            # self.value[3] = self.terminal[4].value #[0]
