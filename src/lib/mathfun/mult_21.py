# -*- coding: utf-8 -*-
from numpy import array

from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Mult21(Component):
    '''
    Sucin dvoch signalov
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(0, -20, 60, 40)

        self.addTerminal('IN1', 1, TERM.IN, QPointF(0, -20))
        self.addTerminal('IN2', 2, TERM.IN, QPointF(0, 20))
        self.addTerminal('OUT', 3, TERM.OUT, QPointF(60, 0))

        self.addParameter('Ref', 'A')

    def drawShape(self, gc):
        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        # terminal hore
        path.addEllipse(15, -15, 30, 30)
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
