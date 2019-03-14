# -*- coding: utf-8 -*-
import six

from component import Component
from componenttypes import TYPE_CONN_VIRTUAL, TYPE_CONNECTION
from terminal import TERM


if six.PY2:
    from PyQt4.QtGui import *  # @UnusedWildImport
    from PyQt4.QtCore import *  # @UnusedWildImport
else:
    from PyQt5.QtWidgets import *  # @UnusedWildImport
    from PyQt5.QtGui import *  # @UnusedWildImport
    from PyQt5.QtCore import *  # @UnusedWildImport


class VirtualConnection(Component):
    '''
    @if English

    @endif

    @if Slovak

    Neviditelny prepojovaci komponent pre spojenie sieti (net-ov).
    Zoznam prepojeni sa vytvara dynamicky na zaklade terminalov sieti.
    Poskytuje spolocny terminal pre vzajomne prepojenie virtualnych sieti.
    Komponent nie je zaradeny do grafickeho kontaineru.

    @endif
    '''

    def __init__(self, name='VirtualConnection', pos=QPoint(0, 0)):
        Component.__init__(self, name, pos)
        self.compType = TYPE_CONN_VIRTUAL
        self.addTerminal('IN', 1, TERM.CONN, QPointF(0, 0))


class Connection(Component):
    '''
    @if English

    @endif

    @if Slovak

    Specialny prepojovaci komponent pre prepojenie sieti (net-ov). Siete
    su prepojene pomocou specialneho terminalu typu TERM.CONN.

    @endif
    '''

    def __init__(self, name, pos):
        '''
        '''
        Component.__init__(self, name, pos)

        self.compType = TYPE_CONNECTION
        self.box = QRectF(-5, -5, 10, 10)

        self.addTerminal('CONN', 1, TERM.CONN, QPointF(0, 0), TERM.DIR_SOUTH, TERM.NONE, TERM.NONE)
        self.setZValue(10)

    def drawShape(self, gc):
        # @TODO - parametrizovat farbu prepojenia podla pripojenej siete
        gc.setPen(QPen(Qt.darkGreen))
        gc.setBrush(QBrush(Qt.darkGreen))
        gc.drawEllipse(-3, -3, 6, 6)
