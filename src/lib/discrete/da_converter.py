# -*- coding: utf-8 -*-

from numpy import ones, hstack, zeros, logical_and

from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_INIT, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Dac(Component):
    '''!
    @if English

    Unipolar or bipolar D/A Convertor.

    @endif

    @if Slovak

    Unipolarny / bipolarny digitalno - analogovy prevodnik s nastavitelnym
    rozlisenim.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeImage = 'adc.svg'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.addParameter('Vref H', 1, False, QPointF(40, 30), Color.black, True)
        self.addParameter('Vref L', -1, False, QPointF(40, 30), Color.black, True)
        self.addParameter('Resolution', 6, False, QPointF(40, 30), Color.black, True)

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        term = self.addTerminal('CLOCK', 3, TERM.IN, QPointF(0, -25), TERM.DIR_SOUTH, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        term.termDiscColor = Color.red
        term.termConnColor = Color.red
        term.termConnFill = Color.red

    def updateShape(self):
        super(Dac, self).updateShape()

        # kontrola Vh, Vl, rozlisenia
        if self.parameter['Vref H'].value < self.parameter['Vref L'].value:
            self.parameter['Vref H'].value = 1.0
            self.parameter['Vref L'].value = -1.0

        if self.parameter['Resolution'].value < 1:
            self.parameter['Resolution'].value = 1

        vh = self.parameter['Vref H'].value
        vl = self.parameter['Vref L'].value
        nb = self.parameter['Resolution'].value

        self.bit = (vh - vl) / float(pow(2, nb))

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.khaki)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

        font = QFont('Decorative', 8)
        font.setItalic(True)
        gc.setFont(font)
        gc.setPen(QPen(Color.red, 1))
        gc.drawText(QRectF(-10, -10, 20, 20), Qt.AlignHCenter | Qt.AlignVCenter, str(self.parameter['Resolution'].value))

    def sim(self, flag, value, time, step):

        if flag == SIM_INIT:
            self.terminal[2].value = 0.0

        elif flag == SIM_UPDATE:
            if self.terminal[3].value < 1:
                return

            mask = ones(nb)
            # vypocet masky vah
            for i in range(1, nb):
                mask[i] = 2 * mask[i - 1]
            # inverzia masky pre vahovanie parametrov v spravnom poradi
            # mask=mask[::-1]

            inp = self.terminal[1].value  # vektor logickych hodnot (0,1), (false/true)

            w = len(inp)
            if w < nb:
                inp = hstack((zeros(nb - w), inp))

            # uprava vstupnych dat - logicky komparator
            data = logical_and(ones(nb), inp)

            temp = data * mask
            value = sum(temp)

            self.setTermValue(2, value)
