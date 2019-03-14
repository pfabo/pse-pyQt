# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Equ(Component):
    '''!
    @if English

    @endif

    @if Slovak

    Porovnanie vstupnych hodnot na zhodu, vysledkom je hodnota True alebo False.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -30, 60, 60)

        term_in1 = self.addTerminal('INA', 1, TERM.IN, QPointF(-30, 0))
        term_in1.termDiscColor = Color.black

        term_in2 = self.addTerminal('INB', 2, TERM.IN, QPointF(30, 0))
        term_in2.termDiscColor = Color.black

        TERM.out = self.addTerminal('OUT', 3, TERM.OUT, QPointF(0, 30))
        TERM.out.termDiscColor = Color.black

        self.addParameter('Round', 3)

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.addEllipse(-15, -15, 30, 30)

        # terminal dole
        path.moveTo(0, 30)
        path.lineTo(0, 15)
        # sipka
        path.moveTo(-3, 22)
        path.lineTo(0, 30)
        path.lineTo(3, 22)

        # terminal vlavo
        path.moveTo(-30, 0)
        path.lineTo(-15, 0)
        # sipka
        path.moveTo(-22, 3)
        path.lineTo(-15, 0)
        path.lineTo(-22, -3)

        # terminal vpravo
        path.moveTo(30, 0)
        path.lineTo(15, 0)
        # sipka
        path.moveTo(22, 3)
        path.lineTo(15, 0)
        path.lineTo(22, -3)

        # znak =
        path.moveTo(-10, -3)
        path.lineTo(10, -3)
        path.moveTo(-10, 3)
        path.lineTo(10, 3)

        gc.drawPath(path)

    def sim(self, flag, value, time, step):
        roundDigit = self.parameter['Round'].value

        try:
            inA = round(self.terminal[1].value, roundDigit)
            inB = round(self.terminal[2].value, roundDigit)

            if inA == inB:
                self.terminal[3].value = True
            else:
                self.terminal[3].value = False
        except Exception as err:
            self.terminal[3].value = False
            print('>>> Error in Equ, Ref =', self.parameter['Ref'].value)
            print('    Error during comparison of input values ', inA, inB)
            print('    Exception:', err)


class Lss(Component):
    '''!
    @if English

    @endif

    @if Slovak

    Porovnanie vstupnych hodnot, vysledkom je hodnota True alebo False.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -30, 60, 60)

        term_in1 = self.addTerminal('INA', 1, TERM.IN, QPointF(-30, 0))
        term_in1.termDiscColor = Color.black

        term_in2 = self.addTerminal('INB', 2, TERM.IN, QPointF(30, 0))
        term_in2.termDiscColor = Color.black

        TERM.out = self.addTerminal('OUT', 3, TERM.OUT, QPointF(0, 30))
        TERM.out.termDiscColor = Color.black

        self.addParameter('Round', 3)

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.addEllipse(-15, -15, 30, 30)

        # terminal dole
        path.moveTo(0, 30)
        path.lineTo(0, 15)
        # sipka
        path.moveTo(-3, 22)
        path.lineTo(0, 30)
        path.lineTo(3, 22)

        # terminal vlavo
        path.moveTo(-30, 0)
        path.lineTo(-15, 0)
        # sipka
        path.moveTo(-22, 3)
        path.lineTo(-15, 0)
        path.lineTo(-22, -3)

        # terminal vpravo
        path.moveTo(30, 0)
        path.lineTo(15, 0)
        # sipka
        path.moveTo(22, 3)
        path.lineTo(15, 0)
        path.lineTo(22, -3)

        # znak >
        path.moveTo(-8, -6)
        path.lineTo(10, 0)
        path.lineTo(-8, 6)

        gc.drawPath(path)

    def sim(self, flag, value, time, step):
        roundDigit = self.parameter['Round'].value

        try:
            inA = round(self.terminal[1].value, roundDigit)
            inB = round(self.terminal[2].value, roundDigit)

            if inA > inB:
                self.terminal[3].value = True
            else:
                self.terminal[3].value = False
        except Exception as err:
            self.terminal[3].value = False
            print('>>> Error in Lss, Ref =', self.parameter['Ref'].value)
            print('    Error during comparison of input values ', inA, inB)
            print('    Exception:', err)


class Leq(Component):
    '''!
    @if English

    @endif

    @if Slovak

    Porovnanie vstupnych hodnot, vysledkom je hodnota True alebo False.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -30, 60, 60)

        term_in1 = self.addTerminal('INA', 1, TERM.IN, QPointF(-30, 0))
        term_in1.termDiscColor = Color.black

        term_in2 = self.addTerminal('INB', 2, TERM.IN, QPointF(30, 0))
        term_in2.termDiscColor = Color.black

        TERM.out = self.addTerminal('OUT', 3, TERM.OUT, QPointF(0, 30))
        TERM.out.termDiscColor = Color.black

        self.addParameter('Round', 3)

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.addEllipse(-15, -15, 30, 30)

        # terminal dole
        path.moveTo(0, 30)
        path.lineTo(0, 15)
        # sipka
        path.moveTo(-3, 22)
        path.lineTo(0, 30)
        path.lineTo(3, 22)

        # terminal vlavo
        path.moveTo(-30, 0)
        path.lineTo(-15, 0)
        # sipka
        path.moveTo(-22, 3)
        path.lineTo(-15, 0)
        path.lineTo(-22, -3)

        # terminal vpravo
        path.moveTo(30, 0)
        path.lineTo(15, 0)
        # sipka
        path.moveTo(22, 3)
        path.lineTo(15, 0)
        path.lineTo(22, -3)

        # znak >=
        path.moveTo(-8, -6)
        path.lineTo(10, 0)
        path.lineTo(-8, 6)

        path.moveTo(-8, 9)
        path.lineTo(10, 3)

        gc.drawPath(path)

    def sim(self, flag, value, time, step):
        roundDigit = self.parameter['Round'].value

        try:
            inA = round(self.terminal[1].value, roundDigit)
            inB = round(self.terminal[2].value, roundDigit)

            if inA > inB:
                self.terminal[3].value = True
            else:
                self.terminal[3].value = False
        except Exception as err:
            self.terminal[3].value = False
            print('>>> Error in Lss, Ref =', self.parameter['Ref'].value)
            print('    Error during comparison of input values ', inA, inB)
            print('    Exception:', err)
