# -*- coding: utf-8 -*-
from cmath import rect

from numpy import real, imag, angle

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM, TEXT


class Complex2XY(Component):
    '''
    @if English

    @endif

    @if Slovak

    Konverzia komplexneho cisla na realnu a imaginarnu cast.

    Hodnotou vstupneho terminalu moze byt komplexne cislo alebo pole komplexnych cisel.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'comp_xy.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.steelBlue

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t2 = self.addTerminal('x', 2, TERM.OUT, QPointF(30, -10), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        t2.termNameShow = True
        t2.termNameAlign = TEXT.RIGHT
        t2.posName = QPoint(-7, 5)
        t3 = self.addTerminal('y', 3, TERM.OUT, QPointF(30, 10), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        t3.termNameShow = True
        t3.termNameAlign = TEXT.RIGHT
        t3.posName = QPoint(-7, 5)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        c = self.terminal[1].value

        if type(c) == complex:
            self.terminal[2].value = c.real
            self.terminal[3].value = c.imag
        else:
            self.terminal[2].value = real(c)
            self.terminal[3].value = imag(c)


class XY2Complex(Component):
    '''
    @if English

    @endif

    @if Slovak

    Konverzia realnej a imaginarnej casti na komplexne cislo.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'xy_comp.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.steelBlue

        self.addTerminal('OUT', 3, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        t1 = self.addTerminal('x', 1, TERM.IN, QPointF(-30, -10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t1.termNameShow = True
        t1.termNameAlign = TEXT.LEFT
        t1.posName = QPoint(7, 5)
        t2 = self.addTerminal('y', 2, TERM.IN, QPointF(-30, 10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t2.termNameShow = True
        t2.termNameAlign = TEXT.LEFT
        t2.posName = QPoint(7, 5)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        x = self.terminal[1].value
        y = self.terminal[2].value
        self.terminal[3].value = complex(x, y)


class Complex2RP(Component):
    '''
    @if English

    @endif

    @if Slovak

    Konverzia komplexneho cisla na amplitudu a fazu.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'comp_rp.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.steelBlue

        self.addTerminal('c', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)

        t2 = self.addTerminal('r', 2, TERM.OUT, QPointF(30, -10), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        t2.termNameShow = True
        t2.termNameAlign = TEXT.RIGHT
        t2.posName = QPoint(-9, 5)
        t3 = self.addTerminal('p', 3, TERM.OUT, QPointF(30, 10), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        t3.termNameShow = True
        t3.termNameAlign = TEXT.RIGHT
        t3.posName = QPoint(-7, 5)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        c = self.terminal[1].value
        self.terminal[2].value = abs(c)
        self.terminal[3].value = angle(c)


class RP2Complex(Component):
    '''
    @if English

    @endif

    @if Slovak

    Konverzia amplitudy a fazy na  komplexne cislo.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'rp_comp.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.steelBlue

        self.addTerminal('c', 3, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        t1 = self.addTerminal('r', 1, TERM.IN, QPointF(-30, -10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t1.termNameShow = True
        t1.termNameAlign = TEXT.LEFT
        t1.posName = QPoint(9, 5)
        t2 = self.addTerminal('p', 2, TERM.IN, QPointF(-30, 10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t2.termNameShow = True
        t2.termNameAlign = TEXT.LEFT
        t2.posName = QPoint(7, 5)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightBlue)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        r = self.terminal[1].value
        p = self.terminal[2].value
        self.terminal[3].value = rect(r, p)
