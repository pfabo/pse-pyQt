# -*- coding: utf-8 -*-
from numpy import sin, pi, cos

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class GenSine(Component):
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'gensine.svg'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Amplitude', 1.0, visibleName=True)
        self.addParameter('Offset', 0.0, visibleName=True)
        self.addParameter('Frequency', 1.0, visibleName=True)
        self.addParameter('Phase', 0.0, visibleName=True)

    def drawShape(self, gc):

        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.green)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        ampl = self.parameter['Amplitude'].value
        offs = self.parameter['Offset'].value
        f = self.parameter['Frequency'].value
        phase = self.parameter['Phase'].value

        self.terminal[1].value = ampl * sin(2 * pi * f * time + phase) + offs


class GenCos(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'gencos.svg'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Amplitude', 1.0, visibleName=True)
        self.addParameter('Offset', 0.0, visibleName=True)
        self.addParameter('Frequency', 1.0, visibleName=True)
        self.addParameter('Phase', 0.0, visibleName=True)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.green)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        ampl = self.parameter['Amplitude'].value
        offs = self.parameter['Offset'].value
        f = self.parameter['Frequency'].value
        phase = self.parameter['Phase'].value

        self.terminal[1].value = ampl * cos(2 * pi * f * time + phase) + offs
