# -*- coding: utf-8 -*-

from numpy import array

from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Sum22(Component):
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(0, -20, 60, 40)

        self.addTerminal('IN1', 1, TERM.IN, QPointF(0, -20))
        self.addTerminal('IN2', 2, TERM.IN, QPointF(0, 20))
        self.addTerminal('OUT', 3, TERM.OUT, QPointF(60, 0))

        # Parametre bloku pre simulacie
        self.addParameter('Inputs', '++')

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.addEllipse(15, -15, 30, 30)

        # terminal hore
        path.moveTo(0, -20)
        path.lineTo(10, -20)
        path.lineTo(19, -11)

        # sipka
        path.moveTo(17, -18)
        path.lineTo(19, -11)
        path.lineTo(13, -13)

        # terminal dole
        path.moveTo(0, 20)
        path.lineTo(10, 20)
        path.lineTo(19, 11)

        # sipka
        path.moveTo(17, 18)
        path.lineTo(19, 11)
        path.lineTo(13, 13)

        # out
        path.moveTo(45, 0)
        path.lineTo(60, 0)

        # sipka
        path.moveTo(53, 3)
        path.lineTo(60, 0)
        path.lineTo(53, -3)

        path.moveTo(20, 0)
        path.lineTo(40, 0)

        # znacenie komponentu
        ch0 = self.parameter['Inputs'].value[0]
        ch1 = self.parameter['Inputs'].value[1]

        path.moveTo(30, -10)
        path.lineTo(30, 10)

        self.drawPolarity(path, 1, ch0)
        self.drawPolarity(path, 2, ch1)

        gc.drawPath(path)

    def drawPolarity(self, path, termNum, sign):

        dx = self.terminal[termNum].position.x()
        dy = self.terminal[termNum].position.y()
        path.moveTo(dx - 5, dy - 10)
        path.lineTo(dx + 5, dy - 10)
        if sign == '+':
            path.moveTo(dx, dy - 15)
            path.lineTo(dx, dy - 5)

    def sim(self, flag, value, time, step):

        in1 = array(self.terminal[1].value)
        in2 = array(self.terminal[2].value)

        if self.parameter['Inputs'].value[0] != '+':
            in1 = -in1

        if self.parameter['Inputs'].value[1] != '+':
            in2 = -in2

        self.terminal[3].value = in1 + in2
