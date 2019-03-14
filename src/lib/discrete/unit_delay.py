# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_INIT, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class UnitDelay(Component):
    '''
    @if English

    Unit delay component.

    @endif

    @if Slovak

    Oneskorenie jednotkoveho kroku (systemovy delay definovany v nastaveni solveru).

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.shapeImage = 'unit_delay.png'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.compType = TYPE_SIM_DISCRETE

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.khaki)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -15, -15)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT or flag == SIM_UPDATE:
            self.terminal[2].value = self.terminal[1].value


class UnitDelayClk(Component):
    '''
    @if English

    Unit delay component with external clock.

    @endif

    @if Slovak

    Oneskorenie jednotkoveho krok synchronizovane na externe hodiny.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.shapeImage = 'unit_delay.png'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.compType = TYPE_SIM_DISCRETE

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        term = self.addTerminal('CLOCK', 3, TERM.IN, QPointF(0, -25), TERM.DIR_SOUTH, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        term.termDiscColor = Color.red
        term.termConnColor = Color.red
        term.termConnFill = Color.red

        self.value = 0.0

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.khaki)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -15, -15)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            # self.terminal[2].value = self.terminal[1].value
            # self.value = self.terminal[2].value
            self.value = 0.0

        if flag == SIM_UPDATE:
            if self.terminal[3].value < 1:
                return
            else:
                self.terminal[2].value = self.value
                self.value = self.terminal[1].value
