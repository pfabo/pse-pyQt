# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Console(Component):
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'console.svg'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.blue

        term_in = self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0),
                                   TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL,
                                   TERM.IN_ARROW_SMALL)
        term_in.termDiscColor = Color.black  # farby pre vstup - vektor
        term_in.termDiscFill = Color.white
        term_in.termConnColor = Color.black
        term_in.termConnFill = Color.black

        self.addParameter('Start time', 0.0)
        self.addParameter('End time', -1.0)

    def drawShape(self, gc):
        '''
        '''
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.mediumAquamarine)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        '''
       @todo - parametricke formatovanie hodnot (decimalnej casti, parameter 'Decimal digits')
             - formatovany vystup vektorov (poloziek)
        '''

        if flag == SIM_UPDATE:
            if self.parameter['End time'].value == -1.0:
                pass
            elif time < self.parameter['Start time'].value or time > self.parameter['End time'].value:
                return
            print(self.parameter['Ref'].value, ':', '{0:.4}'.format(
                time), self.terminal[1].value)
