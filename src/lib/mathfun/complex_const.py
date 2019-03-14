# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class ConstComplex(Component):
    """!
    @if English

    @endif

    @if Slovak

    Zdroj konštantnej hodnoty typu COMPLEX.

    @endif
    """
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -15, 60, 30)
        self.shapeColor = Color.black
        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Value', '1.0+1.0j')
        self.value = 0

    def updateShape(self):
        super(ConstComplex, self).updateShape()
        # inicializacia hodnoty parametra po vytvoreni komponentu
        # pri ulozeni do suboru (JSON) sa hodnota sa uklada ako retazec, konverzia z retazca

        s = self.parameter['Value'].value
        s = s.strip()
        s = s.replace(" ", "")

        # TODO - graficke osetrenie chyby pri chybnom formate komplexneho cisla - cervena vypln a pod.
        try:
            self.value = complex(s)
        except:
            self.value = 1 + 1j

        self.parameter['Value'].value = str(self.value)

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
        gc.drawText(qr, Qt.AlignCenter, str(self.value))

    def sim(self, flag, value, time, step):
        self.terminal[1].value = self.value
