# -*- coding: utf-8 -*-
from numpy import ones, array

from color import Color
from component import Component, VirtualComponent
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Gain(Component):
    '''
    @if English

    @endif

    @if Slovak

    Zosilnenie vstupnej veliciny Out = Gain * In + Offset

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-40, -30, 80, 60)

        self.addTerminal('IN', 1, TERM.IN, QPointF(-40, 0))
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(40, 0))

        self.addParameter('Gain', 1.0, True, QPointF(-10, 0), Color.black, False)
        self.addParameter('Offset', 0.0, False, QPointF(10, 55), Color.black, True)

    def drawShape(self, gc):

        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.yellow)
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

    def sim(self, flag, value, time, step):
        gain = self.parameter['Gain'].value
        offs = self.parameter['Offset'].value

        if flag == SIM_INIT:
            self.terminal[1].value = 0
            self.terminal[2].value = 0
        else:
            inp = array(self.terminal[1].value)
            self.terminal[2].value = inp * gain + offs


class VirtGain(VirtualComponent):
    '''!
    @if English

    @endif

    @if Slovak

    Virtuálny blok zosilnenia.

    Y = gain * x

    @endif
    '''
    def __init__(self):

        VirtualComponent.__init__(self)

        self.compType = TYPE_SIM_CONTINUOUS
        self.className = 'VirtGain'

        self.addTerminal('IN', 1, TERM.IN)
        self.addTerminal('OUT', 2, TERM.OUT)

        self.gain = 1.0

    def sim(self, flag, value, time, step):
        self.terminal[2].value = self.terminal[1].value * self.gain


class VirtSumGain(VirtualComponent):
    '''!
    @if English


    @endif

    @if Slovak

    Blok sumácie a nasobenia.

    Pocet vstupov je urcenu v parametre konstruktora.

    @endif
    '''
    def __init__(self, inputs):

        VirtualComponent.__init__(self)

        self.inputs = inputs
        self.compType = TYPE_SIM_CONTINUOUS
        self.className = 'VirtSumGain'
        self.gain = ones(inputs)

        for i in range(inputs):
            self.addTerminal('IN' + str(i + 1), i + 1, TERM.IN)

        self.addTerminal('OUT', inputs + 1, TERM.OUT)

    def sim(self, flag, value, time, step):

        value = 0.0
        for i in range(self.inputs):
            value = value + self.terminal[i + 1].value * self.gain[i]

        self.terminal[self.inputs + 1].value = value
