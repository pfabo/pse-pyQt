# -*- coding: utf-8 -*-
from numpy import fmod

from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_INIT, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class LogPulse(Component):
    '''Jednokanalovy generator impulzov s logickum vystupom.'''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeImage = 'genpulse.svg'
        self.shapeColor = Color.black

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Frequency', 1.0, False, QPointF(10, 30), Color.black, True)		# frekvencia v abs. hodnote casu
        self.addParameter('Pulse Width', 50, False, QPointF(40, 40), Color.black, True)		# sirka pulzu v %
        self.addParameter('Phase', 0.0, False, QPointF(10, 50), Color.black, True)		# faza impulzu
        self.addParameter('Polarity', 1, False, QPointF(10, 60), Color.black, True)		# polarita

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.khaki)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        '''
        TODO - kontrola parametrov
        '''
        f = self.parameter['Frequency'].value
        w = self.parameter['Pulse Width'].value
        ph = self.parameter['Phase'].value
        pol = self.parameter['Polarity'].value

        if flag == SIM_INIT:
            if pol is True:
                self.terminal[1].value = 1  # , True)
            else:
                self.terminal[1].value = 0  # False)

        elif flag == SIM_UPDATE:

            q = fmod(time + ph, 1 / f)

            if q * f <= w * 0.01:
                value = True
                if pol is False:
                    value = False
            else:
                value = False
                if pol is False:
                    value = True

            self.terminal[1].value = value
