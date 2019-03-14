# -*- coding: utf-8 -*-
from decimal import getcontext, Decimal

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CLOCK, SIM_INIT, SIM_STEP
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Clock(Component):
    '''
    @if English

    Clock source.

    @endif

    @if Slovak

    Zdroj hodinovych impulzov o dlzke jedneho simulacneho kroku
    pre diskretne komponenty.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.shapeImage = 'clock.svg'
        self.compType = TYPE_SIM_CLOCK
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        term = self.addTerminal('CLOCK', 1, TERM.OUT, QPointF(0, 30), TERM.DIR_SOUTH, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        term.termDiscColor = Color.red
        term.termConnColor = Color.red
        term.termConnFill = Color.red

        self.addParameter('Period', 0.1, False, QPointF(40, 30), Color.black, True)
        self.addParameter('Offset', 0.0, False, QPointF(40, 45), Color.black, True)

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
        Generovanie hodinovych impulzov podla zadnej periody a fazy.
        Pre presnu synchronizaciu je pouzity datovy typ Decimal.
        '''

        # 1 usec rozlisenie casu
        getcontext().prec = 6

        tp = Decimal(self.parameter['Period'].value)
        ofs = Decimal(self.parameter['Offset'].value)
        step = Decimal(step)
        time = Decimal(time)

        # kontrola na chybove stavy
        #	1.  krok simulacie < ako nastavena perioda hodin,
        if (step > tp):
            print('>>> WARNING: Component CLock ', self.parameter['Ref'].value)
            print('    Clock period (', tp, ') < step of simulation (', step, ')')
            return

        if flag == SIM_INIT:
            self.terminal[1].value = 0

        elif flag == SIM_STEP:
            if time > 0.0:

                q = (time + ofs) / step
                w = tp / step

                if (q % w) == 0:
                    self.terminal[1].value = 1
                else:
                    self.terminal[1].value = 0
