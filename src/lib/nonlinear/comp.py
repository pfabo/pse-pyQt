# -*- coding: utf-8 -*-
from numpy import ones, array, ndarray, zeros

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class CompST(Component):
    '''
    @if English

    @endif

    @if Slovak

    Standardny komparator bez hysterezy. Klasické zobrazenie v tvare trojuholníka.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-40, -35, 80, 70)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN', 1, TERM.IN, QPointF(-40, 0))
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(40, 0))

        self.addParameter('Output H', 1.0, False, QPointF(0, 40), Color.black, True)
        self.addParameter('Output L', -1.0, False, QPointF(0, 45), Color.black, True)
        self.addParameter('Comp', 0.0, False, QPointF(0, 45), Color.black, True)

    def drawShape(self, gc):

        grad = QLinearGradient(0, -30, 0, 60)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor))

        path = QPainterPath()

        path.moveTo(-40, 0)
        path.lineTo(-30, 0)
        path.moveTo(40, 0)
        path.lineTo(30, 0)
        gc.drawPath(path)

        path.moveTo(-30, -30)
        path.lineTo(-25, -30)
        path.lineTo(-25, 30)
        path.lineTo(-30, 30)
        path.lineTo(-30, -30)
        gc.drawPath(path)

        path = QPainterPath()
        path.moveTo(-25, -30)
        path.lineTo(30, 0)
        path.lineTo(-25, 30)
        path.lineTo(-25, -30)
        gc.drawPath(path)

        gc.setPen(QPen(Color.black))
        path = QPainterPath()
        path.moveTo(-22, 15)
        path.lineTo(-15, 15)
        path.lineTo(-15, -15)
        path.lineTo(-8, -15)
        gc.drawPath(path)

    def sim(self, flag, value, time, step):

        inpValue = self.terminal[1].value
        outHigh = self.parameter['Output H'].value
        outLow = self.parameter['Output L'].value
        compVal = self.parameter['Comp'].value

        if type(inpValue) == ndarray:
            out = zeros(len(inpValue))
            for i in range(len(inpValue)):
                if inpValue[i] == compVal:
                    out[i] = (outHigh + outLow) / 2.0
                elif inpValue[i] > compVal:
                    out[i] = outHigh
                else:
                    out[i] = outLow
        else:
            out = 0
            if inpValue == compVal:
                out = (outHigh + outLow) / 2.0
            elif inpValue > compVal:
                out = outHigh
            else:
                out = outLow

        self.terminal[2].value = out


class CompBlock(Component):
    '''
    @if English

    @endif

    @if Slovak

    Štandardný komparátor bez hysterézy. Zobrazenie v tvare bloku.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'comp.svg'
        self.shapeColor = Color.steelBlue

        self.box = QRectF(-30, -30, 60, 60)

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Output H', 1.0, False, QPointF(-30, 40), Color.black, True)
        self.addParameter('Output L', -1.0, False, QPointF(-30, 50), Color.black, True)
        self.addParameter('Comp', 0.0, False, QPointF(-30, 60), Color.black, True)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):

        inpValue = self.terminal[1].value
        outHigh = self.parameter['Output H'].value
        outLow = self.parameter['Output L'].value
        compVal = self.parameter['Comp'].value

        if type(inpValue) == ndarray:
            out = zeros(len(inpValue))
            for i in range(len(inpValue)):
                if inpValue[i] == compVal:
                    out[i] = (outHigh + outLow) / 2.0
                elif inpValue[i] > compVal:
                    out[i] = outHigh
                else:
                    out[i] = outLow
        else:
            out = 0
            if inpValue == compVal:
                out = (outHigh + outLow) / 2.0
            elif inpValue > compVal:
                out = outHigh
            else:
                out = outLow

        self.terminal[2].value = out


class CompHS(Component):
    '''
    @if English

    @endif

    @if Slovak

    Komparator s hysterezou

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-40, -35, 80, 70)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN', 1, TERM.IN, QPointF(-40, 0))
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(40, 0))

        self.addParameter('Comp H', 1.0, False, QPointF(10, 75), Color.black, True)
        self.addParameter('Comp L', -1.0, False, QPointF(10, 60), Color.black, True)
        self.addParameter('Output H', 1.0, False, QPointF(10, 40), Color.black, True)
        self.addParameter('Output L', -1.0, False, QPointF(10, 55), Color.black, True)

    def drawShape(self, gc):

        grad = QLinearGradient(0, -30, 0, 60)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor))

        path = QPainterPath()

        path.moveTo(-40, 0)
        path.lineTo(-30, 0)
        path.moveTo(40, 0)
        path.lineTo(30, 0)
        gc.drawPath(path)

        path.moveTo(-30, -30)
        path.lineTo(-25, -30)
        path.lineTo(-25, 30)
        path.lineTo(-30, 30)
        path.lineTo(-30, -30)
        gc.drawPath(path)

        path = QPainterPath()
        path.moveTo(-25, -30)
        path.lineTo(30, 0)
        path.lineTo(-25, 30)
        path.lineTo(-25, -30)
        gc.drawPath(path)

        gc.setPen(QPen(Color.black))
        path = QPainterPath()
        path.moveTo(-22, 15)
        path.lineTo(-15, 15)
        path.lineTo(-15, -15)
        path.lineTo(-3, -15)

        path.moveTo(-15, 15)
        path.lineTo(-10, 15)
        path.lineTo(-10, -15)
        gc.drawPath(path)

    def sim(self, flag, value, time, step):
        inpValue = self.terminal[1].value

        outHigh = self.parameter['Output H'].value
        outLow = self.parameter['Output L'].value
        valH = self.parameter['Comp H'].value
        valL = self.parameter['Comp L'].value

        if flag == SIM_INIT:
            if type(inpValue) == ndarray:
                self.terminal[2].value = array(ones(len(inpValue))) * outHigh
            else:
                self.terminal[2].value = outHigh

        else:
            if type(inpValue) == ndarray:

                for i in range(len(inpValue)):
                    if inpValue[i] >= valH:
                        self.terminal[2].value[i] = outHigh

                    if inpValue[i] <= valL:
                        self.terminal[2].value[i] = outLow
            else:
                if inpValue >= valH:
                    self.terminal[2].value = outHigh
                if inpValue <= valL:
                    self.terminal[2].value = outLow


class CompLatch(Component):
    '''
    @if English

    @endif

    @if Slovak

    Standardny komparator so synchronizovanym vystupom (Latch).

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-40, -35, 80, 70)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN', 1, TERM.IN, QPointF(-40, 0))
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(40, 0))
        self.addTerminal('CLK', 3, TERM.IN, QPointF(10, -30))

        self.addParameter('Output H', 1.0, False, QPointF(40, 70), Color.black, True)
        self.addParameter('Output L', -1.0, False, QPointF(40, 85), Color.black, True)
        self.addParameter('Comp', 0.0, False, QPointF(40, 85), Color.black, True)

        self.val_CLK = 0  # predchadzajuca hodnota synchr. signalu

    def drawShape(self, gc):

        grad = QLinearGradient(0, -30, 0, 60)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor))

        path = QPainterPath()
        path.moveTo(-40, 0)
        path.lineTo(-30, 0)
        path.moveTo(40, 0)
        path.lineTo(30, 0)
        path.moveTo(10, -30)
        path.lineTo(10, -10)
        gc.drawPath(path)

        path.moveTo(-30, -30)
        path.lineTo(-25, -30)
        path.lineTo(-25, 30)
        path.lineTo(-30, 30)
        path.lineTo(-30, -30)
        gc.drawPath(path)

        path = QPainterPath()
        path.moveTo(-25, -30)
        path.lineTo(30, 0)
        path.lineTo(-25, 30)
        path.lineTo(-25, -30)
        gc.drawPath(path)

        gc.setPen(QPen(Color.black))
        path = QPainterPath()
        path.moveTo(-22, 15)
        path.lineTo(-15, 15)
        path.lineTo(-15, -15)
        path.lineTo(-8, -15)
        gc.drawPath(path)

        gc.setPen(QPen(self.shapeColor))
        #gc.setBrush(QBrush(Color.yellow))
        path = QPainterPath()
        path.moveTo(0, 16)  # vizualne oddelenie buffra
        path.lineTo(0, -16)
        path.lineTo(30, 0)
        path.lineTo(0, 16)
        gc.drawPath(path)

    def sim(self, flag, value, time, step):

        inpValue = self.terminal[1].value
        clk = self.terminal[3].value

        outHigh = self.parameter['Output H'].value
        outLow = self.parameter['Output L'].value
        compVal = self.parameter['Comp'].value

        if clk == self.val_CLK:
            # ustaleny stav
            pass
        elif (clk == 0) and (self.val_CLK == 1):
            # odbezna hrana
            self.val_CLK = clk
        elif (clk == 1) and (self.val_CLK == 0):
            # nabezna hrana - komparacia a zapis hodnoty
            self.val_CLK = clk

            if type(inpValue) == ndarray:
                out = zeros(len(inpValue))
                for i in range(len(inpValue)):
                    if inpValue[i] == compVal:
                        out[i] = (outHigh + outLow) / 2.0
                    elif inpValue[i] > compVal:
                        out[i] = outHigh
                    else:
                        out[i] = outLow
            else:
                out = 0
                if inpValue == compVal:
                    out = (outHigh + outLow) / 2.0
                elif inpValue > compVal:
                    out = outHigh
                else:
                    out = outLow

            self.terminal[2].value = out


class CompHSContr(Component):
    '''
    @if English

    @endif

    @if Slovak

    Komparator s hysterezou

    Parametre preklápania sú definované vstupmo H,L

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-40, -35, 80, 70)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN', 1, TERM.IN, QPointF(-40, 0))
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(40, 0))
        TERM.H = self.addTerminal('H', 3, TERM.IN, QPointF(-40, -20))
        TERM.H.termNameShow = True
        TERM.H.posName = QPoint(-3, -2)

        TERM.L = self.addTerminal('L', 4, TERM.IN, QPointF(-40, 20))
        TERM.L.termNameShow = True
        TERM.L.posName = QPoint(-3, -2)

        self.addParameter('Output H', 1.0, False, QPointF(10, 40), Color.black, True)
        self.addParameter('Output L', -1.0, False, QPointF(10, 55), Color.black, True)

    def drawShape(self, gc):

        grad = QLinearGradient(0, -30, 0, 60)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor))

        gc.setPen(QPen(Color.red))
        path = QPainterPath()
        path.moveTo(-40, 0)
        path.lineTo(-30, 0)
        path.moveTo(40, 0)
        path.lineTo(30, 0)
        path.moveTo(-40, -20)
        path.lineTo(-30, -20)
        path.moveTo(-40, 20)
        path.lineTo(-30, 20)
        gc.drawPath(path)

        gc.setPen(QPen(self.shapeColor))

        path = QPainterPath()
        path.moveTo(-30, -30)
        path.lineTo(-25, -30)
        path.lineTo(-25, 30)
        path.lineTo(-30, 30)
        path.lineTo(-30, -30)
        gc.drawPath(path)

        path = QPainterPath()
        path.moveTo(-25, -30)
        path.lineTo(30, 0)
        path.lineTo(-25, 30)
        path.lineTo(-25, -30)
        gc.drawPath(path)

        gc.setPen(QPen(Color.black))
        path = QPainterPath()
        path.moveTo(-22, 15)
        path.lineTo(-15, 15)
        path.lineTo(-15, -15)
        path.lineTo(-3, -15)

        path.moveTo(-15, 15)
        path.lineTo(-10, 15)
        path.lineTo(-10, -15)
        gc.drawPath(path)

    def sim(self, flag, value, time, step):

        inpValue = self.terminal[1].value

        outHigh = self.parameter['Output H'].value
        outLow = self.parameter['Output L'].value
        valH = self.terminal[3].value
        valL = self.terminal[4].value

        if flag == SIM_INIT:
            if type(inpValue) == ndarray:
                self.terminal[2].value = array(ones(len(inpValue))) * outHigh
            else:
                self.terminal[2].value = outHigh

        else:
            if type(inpValue) == ndarray:

                for i in range(len(inpValue)):
                    if inpValue[i] >= valH:
                        self.terminal[2].value[i] = outHigh

                    if inpValue[i] <= valL:
                        self.terminal[2].value[i] = outLow
            else:
                if inpValue >= valH:
                    self.terminal[2].value = outHigh
                if inpValue <= valL:
                    self.terminal[2].value = outLow
