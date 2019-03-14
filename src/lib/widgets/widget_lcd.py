# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_INIT, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class WdLcdInt(Component):
    '''Celociselny LCD display, faba digitov cierna (default).'''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(-20, -10, 20, 20)

        self.addParameter('Digits', 5)
        self.addParameter('Width', 128)
        self.addParameter('Height', 46)

        self.addTerminal('IN', 1, TERM.IN, QPointF(-10, 0))

        self.display = QLCDNumber()
        self.display.setSegmentStyle(QLCDNumber.Flat)
        # self.display.intValue()
        self.display.display(1234)
        self.isEmbedded = False

    def updateShape(self):
        w = self.parameter['Width'].value
        h = self.parameter['Height'].value
        self.display.resize(w, h)

        n = self.parameter['Digits'].value
        self.display.setDigitCount(n)

        sc = self.scene()
        if sc is not None and self.isEmbedded is False:
            sc.addWidget(self.display)
            self.isEmbedded = True

    def deleteShape(self):
        self.display.setVisible(False)

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.moveTo(-10, 0)
        path.lineTo(0, 0)
        gc.drawPath(path)

        x = self.position.x()
        y = self.position.y()
        #w = self.display.width()
        h = self.display.height()
        self.display.move(x, y - h / 2)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.display.display(0)

        elif flag == SIM_UPDATE:
            value = self.terminal[1].value
            self.display.display(int(value))


class WdLcdFloat(Component):
    '''Float point display, farba digitov modra.'''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(-20, -10, 20, 20)

        self.addParameter('Digits', 5)
        self.addParameter('Width', 128)
        self.addParameter('Height', 46)

        self.addTerminal('IN', 1, TERM.IN, QPointF(-10, 0))

        self.display = QLCDNumber()
        self.display.setSegmentStyle(QLCDNumber.Flat)
        self.display.setSmallDecimalPoint(True)
        self.display.display(123.4)

        self.palette = self.display.palette()
        self.palette.setColor(self.palette.WindowText, QColor(85, 85, 255))
        self.display.setPalette(self.palette)

        self.isEmbedded = False

    def updateShape(self):
        w = self.parameter['Width'].value
        h = self.parameter['Height'].value
        self.display.resize(w, h)

        n = self.parameter['Digits'].value
        self.display.setDigitCount(n)

        sc = self.scene()
        if sc is not None and self.isEmbedded is False:
            sc.addWidget(self.display)
            self.isEmbedded = True

    def deleteShape(self):
        self.display.setVisible(False)

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.moveTo(-10, 0)
        path.lineTo(0, 0)
        gc.drawPath(path)

        x = self.position.x()
        y = self.position.y()
        #w = self.display.width()
        h = self.display.height()
        self.display.move(x, y - h / 2)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.display.display(0.0)

        elif flag == SIM_UPDATE:
            value = self.terminal[1].value
            self.display.display(value)


class WdLcdHex(Component):

    '''
    Hex display, farba digitov cervena.
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(-20, -10, 20, 20)

        self.addParameter('Digits', 5)
        self.addParameter('Width', 128)
        self.addParameter('Height', 46)

        self.addTerminal('IN', 1, TERM.IN, QPointF(-10, 0))

        self.display = QLCDNumber()
        self.display.setSegmentStyle(QLCDNumber.Flat)
        self.display.setHexMode()
        self.display.display(64176)

        self.palette = self.display.palette()
        self.palette.setColor(self.palette.WindowText, Color.red)
        self.display.setPalette(self.palette)

        self.isEmbedded = False

    def updateShape(self):
        w = self.parameter['Width'].value
        h = self.parameter['Height'].value
        self.display.resize(w, h)

        n = self.parameter['Digits'].value
        self.display.setDigitCount(n)

        sc = self.scene()
        if sc is not None and self.isEmbedded is False:
            sc.addWidget(self.display)
            self.isEmbedded = True

    def deleteShape(self):
        self.display.setVisible(False)

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.moveTo(-10, 0)
        path.lineTo(0, 0)
        gc.drawPath(path)

        x = self.position.x()
        y = self.position.y()
        #w = self.display.width()
        h = self.display.height()
        self.display.move(x, y - h / 2)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.display.display(0)

        elif flag == SIM_UPDATE:
            value = self.terminal[1].value
            self.display.display(value)


class WdLcdBin(Component):
    '''Binarny display, farba digitov zelena.'''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(-20, -10, 20, 20)

        self.addParameter('Width', 128)
        self.addParameter('Height', 46)

        self.addTerminal('IN', 1, TERM.IN, QPointF(-10, 0))

        self.display = QLCDNumber(8)
        self.display.setSegmentStyle(QLCDNumber.Flat)
        self.display.setBinMode()
        self.display.display(0xAA)

        self.palette = self.display.palette()
        self.palette.setColor(self.palette.WindowText, Color.darkGreen)
        self.display.setPalette(self.palette)

        self.isEmbedded = False

    def updateShape(self):
        w = self.parameter['Width'].value
        h = self.parameter['Height'].value
        self.display.resize(w, h)

        sc = self.scene()
        if sc is not None and self.isEmbedded is False:
            sc.addWidget(self.display)
            self.isEmbedded = True

    def deleteShape(self):
        self.display.setVisible(False)

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.moveTo(-10, 0)
        path.lineTo(0, 0)
        gc.drawPath(path)

        x = self.position.x()
        y = self.position.y()
        #w = self.display.width()
        h = self.display.height()
        self.display.move(x, y - h / 2)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.display.display(0)

        elif flag == SIM_UPDATE:
            value = self.terminal[1].value
            self.display.display(value)


class WdLcdTime(Component):
    '''Specialny display pre zobrazenie aktualneho casu simulacie.
    Predpoklada sa pouzitie v simulacii RT.

    Widget nemá terminál
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(0, -23, 128, 46)

        self.w = 128
        self.h = 46

        self.display = QLCDNumber()
        self.display.setSegmentStyle(QLCDNumber.Flat)
        self.display.intValue()
        self.display.display(0)
        self.display.resize(128, 46)

        self.palette = self.display.palette()
        self.palette.setColor(self.palette.WindowText, Color.red)
        self.display.setPalette(self.palette)

        self.isEmbedded = False

    def updateShape(self):
        sc = self.scene()
        if sc is not None and self.isEmbedded is False:
            sc.addWidget(self.display)
            self.isEmbedded = True

    def deleteShape(self):
        self.display.setVisible(False)

    def drawShape(self, gc):
        x = self.position.x()
        y = self.position.y()
        #w = self.display.width()
        h = self.display.height()
        self.display.move(x, y - h / 2)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.display.display(0)

        elif flag == SIM_UPDATE:
            self.display.display(int(time + step))
