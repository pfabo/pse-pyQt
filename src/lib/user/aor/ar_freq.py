# -*- coding: utf-8 -*-

from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class AR_Frequency(Component):

    '''
    Float point display, farba digitov modra.
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.firebrick
        self.box = QRectF(0, -25, 180, 50)

        self.addParameter('Value', 102.4000)

        self.addTerminal('DATA', 1, TERM.OUT, QPointF(180, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.display = QLCDNumber()
        self.display.setSegmentStyle(QLCDNumber.Flat)
        self.display.setSmallDecimalPoint(True)
        self.display.setDigitCount(7)
        self.display.resize(175, 46)
        self.display.display(1.0001)

        self.palette = self.display.palette()
        self.palette.setColor(self.palette.WindowText, Color.mediumForestGreen)
        self.display.setPalette(self.palette)

        self.isEmbedded = False

    def updateShape(self):
        self.display.display(self.parameter['Value'].value)

        sc = self.scene()
        if (sc is not None) and (self.isEmbedded is False):
            sc.addWidget(self.display)
            self.isEmbedded = True

    def deleteShape(self):
        self.display.setVisible(False)

    def drawShape(self, gc):
        x = self.position.x()
        y = self.position.y()
        # w = self.display.width()
        h = self.display.height()
        self.display.move(x, y - h / 2)

    def sim(self, flag, value, time, step):
        self.terminal[1].value = self.parameter['Value'].value
