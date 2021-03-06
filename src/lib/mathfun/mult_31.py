# -*- coding: utf-8 -*-
from numpy import array

from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Mult31(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(0, -20, 60, 40)

        self.addTerminal('IN1', 1, TERM.IN, QPointF(0, -20))
        self.addTerminal('IN2', 2, TERM.IN, QPointF(0, 0))
        self.addTerminal('IN3', 3, TERM.IN, QPointF(0, 20))
        self.addTerminal('OUT', 4, TERM.OUT, QPointF(60, 0))

        self.addParameter('Ref', 'A')

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.addEllipse(15, -15, 30, 30)

        path.moveTo(0, -20)
        path.lineTo(10, -20)
        path.lineTo(19, -11)

        # sipka
        path.moveTo(17, -18)
        path.lineTo(19, -11)
        path.lineTo(13, -13)

        path.moveTo(0, 20)
        path.lineTo(10, 20)
        path.lineTo(19, 11)

        # sipka
        path.moveTo(17, 18)
        path.lineTo(19, 11)
        path.lineTo(13, 13)

        # terminal stredny
        path.moveTo(0, 0)
        path.lineTo(15, 0)

        # sipka stredna
        path.moveTo(8, -3)
        path.lineTo(15, 0)
        path.lineTo(8, 3)

        # terminal vystupny
        path.moveTo(45, 0)
        path.lineTo(60, 0)

        # sipka
        path.moveTo(53, 3)
        path.lineTo(60, 0)
        path.lineTo(53, -3)

        # x znak
        path.moveTo(22, -8)
        path.lineTo(38, 8)

        path.moveTo(22, 8)
        path.lineTo(38, -8)

        gc.drawPath(path)

    def sim(self, flag, value, time, step):

        in1 = array(self.terminal[1].value)
        in2 = array(self.terminal[2].value)
        in3 = array(self.terminal[3].value)

        self.terminal[4].value = in1 * in2 * in3
