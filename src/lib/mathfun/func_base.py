# -*- coding: utf-8 -*-

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class FunctionBase(Component):
    '''
    @if English

    Superclass for all block-based mathematical functions.

    @endif

    @if Slovak

    Supertrieda pre všetky blokové matematické funkcie.

    @endif
    '''

    def __init__(self, name, pos):

        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeFillColor = Color.yellow

        term_in = self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        term_in.termDiscColor = Color.black  # farby pre vstup - vektor
        term_in.termDiscFill = Color.white
        term_in.termConnColor = Color.black
        term_in.termConnFill = Color.black

        TERM.out = self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        TERM.out.termDiscColor = Color.black       # farby pre vystup - vektor
        TERM.out.termDiscFill = Color.white
        TERM.out.termConnColor = Color.black
        TERM.out.termConnFill = Color.black

    def updateShape(self):
        if six.PY2 is True:
            super(FunctionBase, self).updateShape()
        if six.PY3 is True:
            super().updateShape()
        # obnovenie farby vyplne po chybe (Color.red)
        self.shapeFillColor = Color.yellow

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, self.shapeFillColor)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)
