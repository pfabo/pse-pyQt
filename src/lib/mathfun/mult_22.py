# -*- coding: utf-8 -*-
from numpy import array, inf

from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Mult22(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(10, -30, 50, 60)

        self.addTerminal('IN1', 1, TERM.IN, QPointF(30, -30))
        self.addTerminal('IN2', 2, TERM.IN, QPointF(30, 30))
        self.addTerminal('OUT', 3, TERM.OUT, QPointF(60, 0))

        self.addParameter('Ref', 'A')

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.addEllipse(15, -15, 30, 30)

        # terminal hore
        path.moveTo(30, -30)
        path.lineTo(30, -15)

        # sipka
        path.moveTo(27, -22)
        path.lineTo(30, -15)
        path.lineTo(33, -22)

        # terminal dole
        path.moveTo(30, 30)
        path.lineTo(30, 15)

        # sipka
        path.moveTo(27, 22)
        path.lineTo(30, 15)
        path.lineTo(33, 22)

        # out
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
        if flag == SIM_INIT:
            self.terminal[1].value = 0
            self.terminal[2].value = 0
            self.terminal[3].value = 0
        else:
            in1 = array(self.terminal[1].value)
            in2 = array(self.terminal[2].value)

            self.terminal[3].value = in1 * in2


class Div22(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(10, -30, 50, 60)

        self.addTerminal('IN1', 1, TERM.IN, QPointF(30, -30))
        self.addTerminal('IN2', 2, TERM.IN, QPointF(30, 30))
        self.addTerminal('OUT', 3, TERM.OUT, QPointF(60, 0))

        self.addParameter('Ref', 'A')

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.addEllipse(15, -15, 30, 30)

        # terminal hore
        path.moveTo(30, -30)
        path.lineTo(30, -15)

        # sipka
        path.moveTo(27, -22)
        path.lineTo(30, -15)
        path.lineTo(33, -22)

        # terminal dole
        path.moveTo(30, 30)
        path.lineTo(30, 15)

        # sipka
        path.moveTo(27, 22)
        path.lineTo(30, 15)
        path.lineTo(33, 22)

        # out
        path.moveTo(45, 0)
        path.lineTo(60, 0)

        # sipka
        path.moveTo(53, 3)
        path.lineTo(60, 0)
        path.lineTo(53, -3)

        # x znak
        path.moveTo(22, 0)
        path.lineTo(38, 0)

        path.addEllipse(29, -7, 2, 2)
        path.addEllipse(29, 5, 2, 2)
        gc.drawPath(path)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[1].value = 0
            self.terminal[2].value = 1
            self.terminal[3].value = 0
        else:
            in1 = array(self.terminal[1].value)
            in2 = array(self.terminal[2].value)
            try:
                self.terminal[3].value = in1 / in2
            except:
                self.terminal[3].value = inf
