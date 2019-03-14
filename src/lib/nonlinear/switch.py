# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Switch2(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'switch.svg'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN1', 1, TERM.IN, QPointF(-30, -10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('IN2', 2, TERM.IN, QPointF(-30, 10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)

        term = self.addTerminal('CNT', 100, TERM.IN, QPointF(0, 25), TERM.DIR_NORTH, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        term.termDiscColor = Color.blue
        term.termConnColor = Color.blue
        term.termConnFill = Color.blue

        self.addTerminal('OUT', 101, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Level', 0.0)

    def drawShape(self, gc):

        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        cnt = self.terminal[100].value

        if cnt > self.parameter['Level'].value:
            self.terminal[101].value = self.terminal[1].value
        else:
            self.terminal[101].value = self.terminal[2].value
