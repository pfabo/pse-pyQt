# -*- coding: utf-8 -*-

from numpy import logical_not

from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class D(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.box = QRectF(0, 0, 70, 50)
        self.value = 0

        self.addTerminal('D', 1, TERM.IN, QPointF(0, 10))
        self.addTerminal('CLK', 2, TERM.IN, QPointF(0, 40))
        self.addTerminal('QP', 3, TERM.OUT, QPointF(70, 10))
        self.addTerminal('QN', 4, TERM.OUT, QPointF(70, 40))

        self.val_QP = 0
        self.val_QN = 1
        self.val_CLK = 0

    def drawShape(self, gc):

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.addRect(20, 0, 30, 50)
        path.addEllipse(50, 35, 10, 10)

        # D
        path.moveTo(0, 10)
        path.lineTo(20, 10)

        # CLK
        path.moveTo(0, 40)
        path.lineTo(20, 40)

        path.moveTo(20, 33)
        path.lineTo(27, 40)
        path.lineTo(20, 47)

        # QP
        path.moveTo(50, 10)
        path.lineTo(70, 10)

        # QN
        path.moveTo(60, 40)
        path.lineTo(70, 40)

        gc.drawPath(path)

        gc.setPen(QPen(Color.black))
        font = QFont('Decorative', 10)
        fm = QFontMetrics(font)
        h = fm.height()

        s = 'D'
        w = fm.width(s)
        qr = QRectF(22, 10 - h / 2, w, h)
        gc.drawText(qr, Qt.AlignVCenter, s)

    def sim(self, flag, value, time, step):

        d = self.terminal[1].value
        clk = self.terminal[2].value

        self.terminal[3].value = self.val_QP
        self.terminal[4].value = self.val_QN

        if clk == self.val_CLK:
            # ustaleny stav
            pass
        elif (clk == 1) and (self.val_CLK == 0):
            # nabezna hrana
            self.val_QP = d
            self.val_QN = logical_not(d)
            self.val_CLK = clk
        elif (clk == 0) and (self.val_CLK == 1):
            # odbezna hrana
            self.val_CLK = clk
