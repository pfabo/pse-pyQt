# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class RS(Component):
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.box = QRectF(0, 0, 70, 50)
        self.value = 0

        self.addTerminal('S', 1, TERM.IN, QPointF(0, 10))
        self.addTerminal('R', 2, TERM.IN, QPointF(0, 40))
        self.addTerminal('QP', 3, TERM.OUT, QPointF(70, 10))
        self.addTerminal('QN', 4, TERM.OUT, QPointF(70, 40))

        self.val_QP = 0
        self.val_QN = 1

    def drawShape(self, gc):

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.addRect(20, 0, 30, 50)
        path.addEllipse(10, 5, 10, 10)
        path.addEllipse(10, 35, 10, 10)
        path.addEllipse(50, 35, 10, 10)

        # R
        path.moveTo(0, 10)
        path.lineTo(10, 10)

        # S
        path.moveTo(0, 40)
        path.lineTo(10, 40)

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

        s = 'S'
        w = fm.width(s)
        qr = QRectF(22, 10 - h / 2, w, h)
        gc.drawText(qr, Qt.AlignVCenter, s)

        s = 'R'
        w = fm.width(s)
        qr = QRectF(22, 40 - h / 2, w, h)
        gc.drawText(qr, Qt.AlignVCenter, s)

    def sim(self, flag, value, time, step):

        s = self.terminal[1].value
        r = self.terminal[2].value

        self.terminal[3].value = self.val_QP
        self.terminal[4].value = self.val_QN

        if s == 0:
            self.val_QP = 1
            self.val_QN = 0

        if r == 0:
            self.val_QP = 0
            self.val_QN = 1
