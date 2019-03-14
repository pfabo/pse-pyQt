# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from numpy import logical_and, logical_not

from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Nand_N(Component):
    """!
    @if English

    General NAND gate with N inputs.

    @endif

    @if Slovak

    Všeobecné hradlo NAND s N vstupmi.

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -20, 70, 40)
        self.value = 0

        self.addParameter('Inputs', 2)

        self.addTerminal('Y', 100, TERM.OUT, QPointF(40, 0))

    def drawShape(self, gc):

        n = self.parameter['Inputs'].value

        # vertikalna ciara pri vstupoch
        if n > 3:
            if (n % 2) == 0:  # kontrola parne/neparne cislo
                y = (n // 2) * 20 - 10
            else:
                y = (n // 2) * 20

            path = QPainterPath()
            gc.setPen(QPen(self.shapeColor))
            path.moveTo(-20, -y - 10)
            path.lineTo(-20, y + 10)
            gc.drawPath(path)

            self.box = QRectF(-30, -y - 10, 70, 2 * y + 20)

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))
        # vystupny terminal
        path.moveTo(30, 0)
        path.lineTo(40, 0)
        path.addEllipse(20, -5, 10, 10)
        gc.drawPath(path)

        path.moveTo(0, -20)
        path.lineTo(-20, -20)
        path.lineTo(-20, 20)
        path.lineTo(0, 20)
        path.arcTo(-20, -20, 40, 40, -90, 180)

        gc.drawPath(path)

    def updateShape(self):
        n = self.parameter['Inputs'].value
        if n < 2:
            self.parameter['Inputs'].value = 2
            print ('>>> WARNING <<<')
            print ('    Component And_N: Number of inputs must be >=2')
            return
        else:
            t = self.terminal
            # kontrola pripojenych terminalov
            for k in t:
                if self.terminal[k].connect != []:
                    print ('>>> WARNING <<<')
                    print ('    Component And_N: Connected terminal(s) (docasne neimplementovane)')
                    return

            # zamazanie povodnych terminalov
            tempArr = []
            for k in t:
                if k != 100:
                    tempArr.append(k)
            for q in tempArr:
                del self.terminal[q]

            # generovanie noveho poctu terminalov
            y = 0
            if (n % 2) == 0:  # kontrola - parne/neparne cislo
                y = -(n // 2) * 20 + 10
            else:
                y = -(n // 2) * 20

            for i in range(n):
                term = self.addTerminal('IN' + str(i + 1), (i + 1), TERM.IN, QPointF(-30, y))
                term.length = 10
                term.termColor = self.shapeColor
                y = y + 20

    def sim(self, flag, value, time, step):
        self.terminal[100].value = self.value
        self.value = True
        for t in self.terminal:
            if t != 100:
                self.value = logical_and(self.value, self.terminal[t].value)
        self.value = logical_not(self.value)


class Nand3(Nand_N):

    def __init__(self, name, pos):
        Nand_N.__init__(self, name, pos)
        self.parameter['Inputs'].value = 3


class Nand2(Nand_N):

    def __init__(self, name, pos):
        Nand_N.__init__(self, name, pos)
        self.parameter['Inputs'].value = 2
