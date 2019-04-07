# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class GenTime(Component):
    """!
    @if English

    @endif

    @if Slovak

    Zdroj aktuálnej hodnoty času simulácie.

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -15, 60, 30)
        self.shapeColor = Color.black
        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -10, 0, 20)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.green)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -10, 50, 20, 5, 5)

        self.font = QFont('Decorative', 10)
        fm = QFontMetrics(self.font)
                             # urcenie rozmerov textu a centrovanie vzhladom
        # tw = fm.width(s)	  # k zadanej polohe referencneho bodu
        th = fm.height()

        qr = QRectF(-25, -th / 2, 50, th)
        gc.drawText(qr, Qt.AlignCenter, 'Time')

    def sim(self, flag, value, time, step):
        self.terminal[1].value = time


class GenStep(Component):
    """!
    @if English

    @endif

    @if Slovak

    Aktuálny krok simulácie.

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -15, 60, 30)
        self.shapeColor = Color.black
        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        self.value = 0

    def drawShape(self, gc):
        grad = QLinearGradient(0, -10, 0, 20)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.green)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -10, 50, 20, 5, 5)

        self.font = QFont('Decorative', 10)
        fm = QFontMetrics(self.font)
                             # urcenie rozmerov textu a centrovanie vzhladom
        # tw = fm.width(s)	  # k zadanej polohe referencneho bodu
        th = fm.height()

        qr = QRectF(-25, -th / 2, 50, th)
        gc.drawText(qr, Qt.AlignCenter, 'Step')

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.value = 0
            self.terminal[1].value = self.value
        elif flag == SIM_UPDATE:
            self.value = self.value + 1
            self.terminal[1].value = self.value
