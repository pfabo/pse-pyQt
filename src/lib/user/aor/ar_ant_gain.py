# -*- coding: utf-8 -*-

from numpy import array

from color import Color
from component import Component
from componenttypes import SIM_INIT, TYPE_SIM_DISCRETE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class AR_AntGain(Component):
    '''!
    @if SLOVAK
    @brief Nastavenie anténneho zosilňovača a atenuátora

    Komponent pre nastavenie anténneho atenuátora.
    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.firebrick

        self.addTerminal('IN', 1, TERM.IN, QPointF(-35, 0), TERM.DIR_EAST, TERM.IN_ARROW_FILL, TERM.IN_ARROW)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(35, 0), TERM.DIR_EAST, TERM.OUT_ARROW_FILL, TERM.OUT_ARROW)

        self.addParameter('Gain', '0', False, QPointF(-3, 30))
        # PYTHON3
        #self.command = bytes('AT0\r', encoding='ascii')

    def drawShape(self, gc):

        grad = QLinearGradient(-30, -30, 0, 60)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.yellowGreen)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))

        path = QPainterPath()

        path.moveTo(-30, -30)
        path.lineTo(-25, -30)
        path.lineTo(-25, 30)
        path.lineTo(-30, 30)
        path.lineTo(-30, -30)

        path.moveTo(-25, -30)
        path.lineTo(30, 0)
        path.lineTo(-25, 30)
        gc.drawPath(path)

        txt = self.parameter['Gain'].value
        if txt in ['0', '-10', '-20'] is True:
            txt = txt + ' dB'
        font = QFont('Decorative', 10)
        font.setItalic(True)
        gc.setFont(font)
        gc.setPen(QPen(Color.red, 1))
        gc.drawText(QRectF(-20, -10, 25, 20), Qt.AlignCenter, txt)

    def updateShape(self):
        setup = self.parameter['Gain'].value
        # kontrola parametrov
        if (setup in ['AMP', '0', '-10', '-20', 'AUT']) is not True:
            # zle zadany parameter
            setup = '0'
            self.parameter['Gain'].value = setup
            print('>>> Warning - component AR_AntGain')
            print('    Wrong parameter, use: AMP, 0, -10, -20, AUT ')
        else:
            if setup == 'AMP':
                setup = '0'
            elif setup == '0':
                setup = '1'
            elif setup == '-10':
                setup = '2'
            elif setup == '-20':
                setup = '3'
            elif setup == 'AUT':
                setup = '4'

        if six.PY3:
            self.command = bytes('AT' + setup + '\r', encoding='ascii')

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            # retazenie prikazov
            self.terminal[2].value = array([self.terminal[1].value, self.command])
