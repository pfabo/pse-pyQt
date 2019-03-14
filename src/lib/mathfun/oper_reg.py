# -*- coding: utf-8 -*-

"""!
@if English

@endif

@if Slovak

Symboly pre matematické operácie v regulačných systémoch.

@endif
"""

from numpy import array

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class RegSum2A(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -30, 60, 60)

        self.addTerminal('IN1', 1, TERM.IN, QPointF(-30, 0))
        self.addTerminal('IN2', 2, TERM.IN, QPointF(0, 30))
        self.addTerminal('OUT', 3, TERM.OUT, QPointF(30, 0))

        # Parametre bloku pre simulacie
        self.addParameter('Inputs', '+-')

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        gc.setBrush(Qt.NoBrush)
        path = QPainterPath()

        # terminal IN1
        path.moveTo(-30, 0)
        path.lineTo(-15, 0)

        # terminal IN2
        path.moveTo(0, 30)
        path.lineTo(0, 15)

        # terminal OUT
        path.moveTo(30, 0)
        path.lineTo(15, 0)

        # prazdny obluk
        path.moveTo(-10, -10)
        path.arcTo(-15, -15, 30, 30, 135, -90)
        path.moveTo(-10, -10)
        path.lineTo(0, 0)
        path.lineTo(10, -10)

        gc.drawPath(path)

        # vypln pre IN1
        if self.parameter['Inputs'].value[0] != '+':
            gc.setBrush(QBrush(Color.red))
        else:
            gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(-10, -10)
        path.arcTo(-15, -15, 30, 30, 135, 90)
        path.lineTo(0, 0)
        path.lineTo(-10, -10)
        gc.drawPath(path)

        # vypln pre IN2
        if self.parameter['Inputs'].value[1] != '+':
            gc.setBrush(QBrush(Color.red))
        else:
            gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(-10, 10)
        path.arcTo(-15, -15, 30, 30, 225, 90)
        path.lineTo(0, 0)
        path.lineTo(-10, 10)
        gc.drawPath(path)

        # vypln pre OUT
        gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(10, 10)
        path.arcTo(-15, -15, 30, 30, 315, 90)
        path.lineTo(0, 0)
        path.lineTo(10, 10)
        # sipka
        path.moveTo(23, 3)
        path.lineTo(30, 0)
        path.lineTo(23, -3)
        gc.drawPath(path)

        self.drawPolarity(gc, -25, -10, self.parameter['Inputs'].value[0])
        self.drawPolarity(gc, -10, 25, self.parameter['Inputs'].value[1])

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[1].value = 0
            self.terminal[2].value = 0
            self.terminal[3].value = 0
        else:
            in1 = array(self.terminal[1].value)
            in2 = array(self.terminal[2].value)

            if self.parameter['Inputs'].value[0] != '+':
                in1 = -in1

            if self.parameter['Inputs'].value[1] != '+':
                in2 = -in2

            self.terminal[3].value = in1 + in2

    def drawPolarity(self, gc, dx, dy, sign):

        gc.setBrush(QBrush(Color.red))
        gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(dx - 5, dy)
        path.lineTo(dx + 5, dy)
        if sign == '+':
            path.moveTo(dx, dy - 5)
            path.lineTo(dx, dy + 5)
        gc.drawPath(path)


class RegSum2B(Component):
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -30, 60, 60)

        self.addTerminal('IN1', 1, TERM.IN, QPointF(0, -30))
        self.addTerminal('IN2', 2, TERM.IN, QPointF(0, 30))
        self.addTerminal('OUT', 3, TERM.OUT, QPointF(30, 0))

        # Parametre bloku pre simulacie
        self.addParameter('Inputs', '+-')

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor))
        gc.setBrush(Qt.NoBrush)
        path = QPainterPath()

        # terminal IN1
        path.moveTo(0, -30)
        path.lineTo(0, -15)

        # terminal IN2
        path.moveTo(0, 30)
        path.lineTo(0, 15)

        # terminal OUT
        path.moveTo(30, 0)
        path.lineTo(15, 0)

        # vypln pre IN1
        if self.parameter['Inputs'].value[0] != '+':
            gc.setBrush(QBrush(Color.red))
        else:
            gc.setBrush(Qt.NoBrush)
        path.moveTo(-10, -10)
        path.arcTo(-15, -15, 30, 30, 135, -90)
        path.lineTo(0, 0)
        path.lineTo(-10, -10)

        gc.drawPath(path)

        # prazdny obluk
        gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(-10, -10)
        path.arcTo(-15, -15, 30, 30, 135, 90)
        path.lineTo(0, 0)
        path.lineTo(-10, -10)
        gc.drawPath(path)

        # vypln pre IN2
        if self.parameter['Inputs'].value[1] != '+':
            gc.setBrush(QBrush(Color.red))
        else:
            gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(-10, 10)
        path.arcTo(-15, -15, 30, 30, 225, 90)
        path.lineTo(0, 0)
        path.lineTo(-10, 10)
        gc.drawPath(path)

        # vypln pre OUT
        gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(10, 10)
        path.arcTo(-15, -15, 30, 30, 315, 90)
        path.lineTo(0, 0)
        path.lineTo(10, 10)
        # sipka
        path.moveTo(23, 3)
        path.lineTo(30, 0)
        path.lineTo(23, -3)
        gc.drawPath(path)

        self.drawPolarity(gc, 10, -25, self.parameter['Inputs'].value[0])
        self.drawPolarity(gc, -10, 25, self.parameter['Inputs'].value[1])

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[1].value = 0
            self.terminal[2].value = 0
            self.terminal[3].value = 0
        else:
            in1 = array(self.terminal[1].value)
            in2 = array(self.terminal[2].value)

            if self.parameter['Inputs'].value[0] != '+':
                in1 = -in1

            if self.parameter['Inputs'].value[1] != '+':
                in2 = -in2

            self.terminal[3].value = in1 + in2

    def drawPolarity(self, gc, dx, dy, sign):

        gc.setBrush(QBrush(Color.red))
        gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(dx - 5, dy)
        path.lineTo(dx + 5, dy)
        if sign == '+':
            path.moveTo(dx, dy - 5)
            path.lineTo(dx, dy + 5)
        gc.drawPath(path)


class RegSum3(Component):
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -30, 60, 60)

        self.addTerminal('IN1', 2, TERM.IN, QPointF(-30, 0))
        self.addTerminal('IN2', 3, TERM.IN, QPointF(0, 30))
        self.addTerminal('IN3', 1, TERM.IN, QPointF(0, -30))
        self.addTerminal('OUT', 4, TERM.OUT, QPointF(30, 0))

        # Parametre bloku pre simulacie
        self.addParameter('Inputs', '+-+')

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        gc.setBrush(Qt.NoBrush)
        path = QPainterPath()

        # terminal IN1
        path.moveTo(-30, 0)
        path.lineTo(-15, 0)

        # terminal IN2
        path.moveTo(0, 30)
        path.lineTo(0, 15)

        # terminal IN3
        path.moveTo(0, -30)
        path.lineTo(0, -15)

        # terminal OUT
        path.moveTo(30, 0)
        path.lineTo(15, 0)
        gc.drawPath(path)

        # vypln pre IN3
        if self.parameter['Inputs'].value[0] != '+':
            gc.setBrush(QBrush(Color.red))
        else:
            gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(-10, -10)
        path.arcTo(-15, -15, 30, 30, 135, -90)
        path.lineTo(0, 0)
        path.lineTo(-10, -10)
        gc.drawPath(path)

        # vypln pre IN1
        if self.parameter['Inputs'].value[1] != '+':
            gc.setBrush(QBrush(Color.red))
        else:
            gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(-10, -10)
        path.arcTo(-15, -15, 30, 30, 135, 90)
        path.lineTo(0, 0)
        path.lineTo(-10, -10)
        gc.drawPath(path)

        # vypln pre IN2
        if self.parameter['Inputs'].value[2] != '+':
            gc.setBrush(QBrush(Color.red))
        else:
            gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(-10, 10)
        path.arcTo(-15, -15, 30, 30, 225, 90)
        path.lineTo(0, 0)
        path.lineTo(-10, 10)
        gc.drawPath(path)

        # vypln pre OUT
        gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(10, 10)
        path.arcTo(-15, -15, 30, 30, 315, 90)
        path.lineTo(0, 0)
        path.lineTo(10, 10)
        # sipka
        path.moveTo(23, 3)
        path.lineTo(30, 0)
        path.lineTo(23, -3)
        gc.drawPath(path)

        self.drawPolarity(gc, 10, -25, self.parameter['Inputs'].value[0])
        self.drawPolarity(gc, -25, -10, self.parameter['Inputs'].value[1])
        self.drawPolarity(gc, -10, 25, self.parameter['Inputs'].value[2])

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[1].value = 0
            self.terminal[2].value = 0
            self.terminal[3].value = 0
            self.terminal[4].value = 0
        else:
            in1 = array(self.terminal[1].value)
            in2 = array(self.terminal[2].value)
            in3 = array(self.terminal[3].value)

            if self.parameter['Inputs'].value[0] != '+':
                in1 = -in1

            if self.parameter['Inputs'].value[1] != '+':
                in2 = -in2

            if self.parameter['Inputs'].value[2] != '+':
                in3 = -in3

            self.terminal[4].value = in1 + in2 + in3

    def drawPolarity(self, gc, dx, dy, sign):

        gc.setBrush(QBrush(Color.red))
        gc.setBrush(Qt.NoBrush)
        path = QPainterPath()
        path.moveTo(dx - 5, dy)
        path.lineTo(dx + 5, dy)
        if sign == '+':
            path.moveTo(dx, dy - 5)
            path.lineTo(dx, dy + 5)
        gc.drawPath(path)
