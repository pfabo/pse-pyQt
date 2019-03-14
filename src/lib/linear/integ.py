# -*- coding: utf-8 -*-
from color import Color
from component import Component, VirtualComponent
from componenttypes import TYPE_SIM_INTEGRAL, SIM_INIT, SIM_DERIVE, SIM_STEP
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Integ(Component):
    '''!
    @if English

    @endif

    @if Slovak

    Štandardný integrator Out = Int(Gain * In) dt + InitValue

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_INTEGRAL
        self.box = QRectF(-40, -30, 80, 60)
        self.shapeImage = 'integ_02.svg'

        self.addTerminal('IN', 1, TERM.IN, QPointF(-40, 0))
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(40, 0))

        self.addParameter('Gain', 1.0, False, QPointF(0, 40), Color.black, True)
        self.addParameter('Init value', 0.0, False, QPointF(0, 55), Color.black, True)

        # stavova premenna integratora - kazda simulacna metoda si re-definuje vlastnu velkost pola
        # zakladna velkost je pre nastavenie vo volani sim(SIM_INIT ... ) pri resete diagramu
        # bez definovanej simulacnej metody
        self.contState = [0]

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

        w = 40
        h = 35
        size = self.shapeSvg.sizeHint()
        size.scale(w, h, Qt.KeepAspectRatio)
        self.shapeSvg.setMaximumSize(size)

        self.shapeSvg.render(gc, QPoint(-20, -h / 2))

    def sim(self, flag, value, time, step):

        inp = self.terminal[1].value
        init = self.parameter['Init value'].value
        gain = self.parameter['Gain'].value

        if (flag == SIM_INIT):
            self.terminal[1].value = 0.0
            self.terminal[2].value = init
            self.contState[0] = init / gain

        elif flag == SIM_DERIVE:
            return inp

        elif flag == SIM_STEP:
            self.terminal[2].value = value * gain


class VirtInteg(VirtualComponent):
    '''!
    @if English


    @endif

    @if Slovak

    Integracny blok, bez saturacie, poc. podmienka y(0-)=0

    @endif
    '''

    def __init__(self):
        VirtualComponent.__init__(self)
        self.compType = TYPE_SIM_INTEGRAL
        self.className = 'VirtInt'
        self.addTerminal('IN', 1, TERM.IN)
        self.addTerminal('OUT', 2, TERM.OUT)

    def sim(self, flag, value, time, step):

        inp = self.terminal[1].value

        if flag == SIM_INIT:
            self.terminal[2].value = 0.0

        elif flag == SIM_DERIVE:
            return inp

        elif flag == SIM_STEP:
            self.terminal[2].value = value
