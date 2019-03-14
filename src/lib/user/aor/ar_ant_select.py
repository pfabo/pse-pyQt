# -*- coding: utf-8 -*-

from color import Color
from component import Component
from componenttypes import SIM_INIT, TYPE_SIM_DISCRETE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class AR_Antenna(Component):
    '''!
    @if SLOVAK
    @brief Výber antény

    Komponent pre výber anténneho vstupu prijímača alebo anténneho multiplexeru.
    Výber antény je určený hodnotou parametra <B>Antenne</B>, ktorý môže mať
    nasledujúce hodnoty: AUT, 1, 2, 3, 4
    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.firebrick

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        # parameter vyberu anteny
        # AUT - 0
        # 1 ... 4
        self.addParameter('Antenna', '1')
        # PYTHON3
        # self.command = bytes('AN1\r', encoding='ascii')
        # PYTHON2
        # ???

    def drawShape(self, gc):

        grad = QLinearGradient(-30, -30, 0, 60)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.yellowGreen)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        gc.setPen(QPen(Color.black, 1))
        path = QPainterPath()

        path.moveTo(0, -20)
        path.lineTo(0, 20)
        path.moveTo(0, 0)
        path.lineTo(15, -20)
        path.moveTo(0, 0)
        path.lineTo(-15, -20)
        gc.drawPath(path)

        font = QFont('Decorative', 8)
        font.setItalic(True)
        gc.setFont(font)
        gc.setPen(QPen(Color.red, 1))
        gc.drawText(QRectF(0, 5, 25, 20), Qt.AlignCenter | Qt.AlignTop, str(self.parameter['Antenna'].value))

    def updateShape(self):
        setup = self.parameter['Antenna'].value
        # kontrola parametrov
        if (setup in ['AUT', '1', '2', '3', '4']) is not True:
            # zle zadany parameter
            setup = '1'
            self.parameter['Antenna'].value = setup
            print('>>> Warning - component AR_Antenna')
            print('    Wrong parameter, use: AUT, 1, 2, 3, 4 ')
        else:
            if setup == 'AUT':
                setup = '0'
        # PYTHON3
        #self.command = bytes(('AN' + setup + '\r'), encoding='ascii')

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[1].value = self.command
