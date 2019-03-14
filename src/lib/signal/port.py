# -*- coding: utf-8 -*-
from color import Color
from component import Component, VirtualComponent
from componenttypes import TYPE_NET_TERM, TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class PortIn(Component):
    """!
    @if English

    @endif

    @if Slovak

    Vstupný prepojovaci terminál sieti.

    Terminál slúži na prepojenie oddelených sietí s rovnakým názvom.

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_NET_TERM
        self.box = QRectF(-30, -15, 60, 30)

        self.addParameter('Port', 'A', color=Color.red)

        term_in = self.addTerminal('IN', 1, TERM.CONN, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        term_in.termDiscColor = Color.black
        term_in.termDiscFill = Color.white
        term_in.termConnColor = Color.black
        term_in.termConnFill = Color.black

    def drawShape(self, gc):
        grad = QLinearGradient(0, -10, 0, 20)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.grey)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(Color.black, 1))
        gc.drawRoundedRect(-25, -10, 50, 20, 5, 5)

        gc.setPen(QPen(self.parameter['Port'].color, 1))
        s = self.parameter['Port'].value
        self.font = QFont('Decorative', 10)
        fm = QFontMetrics(self.font)
                             # urcenie rozmerov textu a centrovanie vzhladom
        # tw = fm.width(s)	  # k zadanej polohe referencneho bodu
        th = fm.height()

        qr = QRectF(-25, -th / 2, 50, th)
        gc.drawText(qr, Qt.AlignCenter, s)


class PortOut(Component):
    """!
    @if English

    @endif

    @if Slovak

    Vystupný prepojovaci terminál sieti.

    Terminál slúži na prepojenie oddelených sietí s rovnakým názvom.

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_NET_TERM
        self.box = QRectF(-30, -15, 60, 30)

        self.addParameter('Port', 'A', color=Color.red)
        term_out = self.addTerminal('OUT', 1, TERM.CONN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        term_out.termDiscColor = Color.black
        term_out.termDiscFill = Color.white
        term_out.termConnColor = Color.black
        term_out.termConnFill = Color.black

    def drawShape(self, gc):
        '''
        '''
        grad = QLinearGradient(0, -10, 0, 20)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.grey)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(Color.black, 1))
        gc.drawRoundedRect(-25, -10, 50, 20, 5, 5)

        gc.setPen(QPen(self.parameter['Port'].color, 1))
        s = self.parameter['Port'].value
        self.font = QFont('Decorative', 10)
        fm = QFontMetrics(self.font)
                             # urcenie rozmerov textu a centrovanie vzhladom
        # tw = fm.width(s)	  # k zadanej polohe referencneho bodu
        th = fm.height()

        qr = QRectF(-25, -th / 2, 50, th)
        gc.drawText(qr, Qt.AlignCenter, s)


# backward compatibility
class NetTermIn(PortIn):
    def __init__(self, name, pos):
        PortIn.__init__(self, name, pos)


class NetTermOut(PortOut):
    def __init__(self, name, pos):
        PortOut.__init__(self, name, pos)


class PortNull(Component):
    """!
    @if English

    @endif

    @if Slovak

    Vstupný ukončovací terminál.

    Používa sa ako ukončovací (vstupný) terminál, je určený pre logické ukončenie siete,
    v ktorej sa vyskytuje výstupný terminál a prepojovacie terminály, typicky
    výstupný terminál bloku. Informácia vstupujúca do ukončovacieho terminálu nie je
    ďalej spracovávaná.

    @endif
    """

    def __init__(self, name, pos):
        '''
        '''
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-30, -15, 60, 30)

        term_in = self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        term_in.termDiscColor = Color.black
        term_in.termDiscFill = Color.white
        term_in.termConnColor = Color.black
        term_in.termConnFill = Color.black

    def drawShape(self, gc):
        '''
        '''
        grad = QLinearGradient(0, -10, 0, 20)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.grey)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(Color.black, 1))
        gc.drawRoundedRect(-25, -10, 50, 20, 5, 5)

        gc.setPen(QPen(Color.blue, 1))
        self.font = QFont('Decorative', 10)
        fm = QFontMetrics(self.font)
                             # urcenie rozmerov textu a centrovanie vzhladom
        # tw = fm.width(s)	  # k zadanej polohe referencneho bodu
        th = fm.height()

        qr = QRectF(-25, -th / 2, 50, th)
        gc.drawText(qr, Qt.AlignCenter, 'NULL')


class VirtProxyInOut(VirtualComponent):
    '''!
    @if English


    @endif

    @if Slovak

    Pomocny proxy port pre prepojenie virtualnej a realnej casti komponentu.

    Virtualny In -> Globalny Out - prepojenie na vystupny terminal komponentu

    @endif
    '''

    def __init__(self, proxyTerm):
        VirtualComponent.__init__(self)
        self.className = 'VirtProxyInOut'
        self.proxyTerm = proxyTerm
        self.compType = TYPE_SIM_CONTINUOUS
        self.addTerminal('IN', 1, TERM.IN)

    def sim(self, flag, value, time, step):
        self.proxyTerm.value = self.terminal[1].value


class VirtProxyOutIn(VirtualComponent):
    '''!
    @if English


    @endif

    @if Slovak

    Pomocny proxy port pre prepojenie virtualnej a realnej casti komponentu

    Globalny In -> Lokalny Out - prepojenie na vstupny terminal komponentu

    @endif
    '''

    def __init__(self, proxyTerm):
        VirtualComponent.__init__(self)
        self.className = 'VirtProxyOutIn'
        self.proxyTerm = proxyTerm
        self.compType = TYPE_SIM_CONTINUOUS
        self.addTerminal('OUT', 1, TERM.OUT)

    def sim(self, flag, value, time, step):
        self.terminal[1].value = self.proxyTerm.value
