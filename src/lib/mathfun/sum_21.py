# -*- coding: utf-8 -*-
from numpy import array

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Sum21(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(10, -30, 50, 60)

        term_in1 = self.addTerminal('IN1', 1, TERM.IN, QPointF(30, -30))
        term_in1.termDiscColor = Color.black

        term_in2 = self.addTerminal('IN2', 2, TERM.IN, QPointF(30, 30))
        term_in2.termDiscColor = Color.black

        TERM.out = self.addTerminal('OUT', 3, TERM.OUT, QPointF(60, 0))
        TERM.out.termDiscColor = Color.black

        # Parametre bloku pre simulacie
        self.addParameter('Inputs', '++')

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

        # + znak
        path.moveTo(20, 0)
        path.lineTo(40, 0)

        path.moveTo(30, -10)
        path.lineTo(30, 10)

        self.drawPolarity(path, 1, self.parameter['Inputs'].value[0])
        self.drawPolarity(path, 2, self.parameter['Inputs'].value[1])

        gc.drawPath(path)

    def drawPolarity(self, path, termNum, sign):

        dx = self.terminal[termNum].position.x()
        dy = self.terminal[termNum].position.y()
        path.moveTo(dx - 15, dy)
        path.lineTo(dx - 5, dy)
        if sign == '+':
            path.moveTo(dx - 10, dy - 5)
            path.lineTo(dx - 10, dy + 5)

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
