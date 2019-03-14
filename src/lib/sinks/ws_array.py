# -*- coding: utf-8 -*-
from numpy import ndarray

from color import Color
from component import Component, PARAM
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT, SIM_RESET, \
    SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class WsArray(Component):
    """!
    @if Slovak

    Zapis hodnot terminalu do pola.

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.shapeImage = 'ws_array.png'
        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeColor = Color.blue
        self.box = QRectF(-30, -30, 60, 60)

        term_in = self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        term_in.termDiscColor = Color.black       # farby pre vstup - vektor
        term_in.termDiscFill = Color.white
        term_in.termConnColor = Color.black
        term_in.termConnFill = Color.black

        self.addParameter('Value', [], paramType=PARAM.LIST)

        self.value = []

    def drawShape(self, gc):

        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.mediumAquamarine)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -13)

    def sim(self, flag, value, time, step):
        inp = self.terminal[1].value

        if flag == SIM_INIT or flag == SIM_RESET: 	# re / inicializaci dat
            # inicializacia vystupnej hodnoty, vynulovanie pola
            self.parameter['Value'].value = []

            # pri vektore inicializacia zloziek pola
            if type(inp) == ndarray:
                for i in range(len(inp)):
                    self.parameter['Value'].value.append([])

        if flag == SIM_UPDATE:
            if type(inp) == ndarray:
                for i in range(len(inp)):
                    self.parameter['Value'].value[i].append(inp[i])
            else:
                self.parameter['Value'].value.append(inp)
