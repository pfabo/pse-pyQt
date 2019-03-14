# -*- coding: utf-8 -*-

from numpy import zeros, array

from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_INIT, SIM_STEP
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class LogCounter(Component):
    '''
    N - bitove logicke pocitadlo, vystup je vektor hodnot.
    Pocitadlo je mozne synchronizovat na externe hodiny (External clock = 1)

    @todo: uprava parametra Clock na True/False
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeImage = 'counter.svg'
        self.shapeColor = Color.black

        self.bits = 4
        self.word = zeros(self.bits)
        self.value = 0

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Number of bits', self.bits)  # pocet bitov, sirka slova
        self.addParameter('External clock', 0)

    def updateShape(self):
        super(LogCounter, self).updateShape()

        self.value = 0
        self.word = zeros(self.parameter['Number of bits'].value)

        if self.parameter['External clock'].value == 1:  # TODO - uprava parametra na True/False
            if 2 in self.terminal:
                pass
            else:
                term = self.addTerminal('CLOCK', 2, TERM.IN, QPointF(0, -25), TERM.DIR_SOUTH, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
                term.termDiscColor = Color.red
                term.termConnColor = Color.red
                term.termConnFill = Color.red
        else:
            if 2 in self.terminal:
                if self.terminal[2].connect != []:
                    print('>>> WARNING ')
                    print('    LogCounter : Remove clock terminal')
                    print('                 Clock terminal is connected !')
                    self.parameter['External clock'].value = 1  # True
                else:
                    del self.terminal[2]
            else:
                pass

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.khaki)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)
        # self.shapeSvg.render(gc, targetOffset=QPoint(-20, -20))

        font = QFont('Decorative', 8)
        font.setItalic(True)
        gc.setFont(font)
        gc.setPen(QPen(Color.red, 1))
        gc.drawText(QRectF(-13, -20, 20, 20), Qt.AlignLeft | Qt.AlignTop, str(self.parameter['Number of bits'].value))

    def sim(self, flag, value, time, step):
        ext = self.parameter['External clock'].value

        if flag == SIM_INIT:
            self.value = 0
            self.terminal[1].value = self.word

        elif flag == SIM_STEP:
            # pri externom clocku je hodnota prevedena len v stave clock=1
            if ext == 1:  # True:
                if self.terminal[2].value < 1:
                    return

            self.value = self.value + 1

            n = self.parameter['Number of bits'].value
            num = self.value
            binary = zeros(n)

            for i in range(n):
                bit = num % 2
                binary[n - i - 1] = int(bit)
                num = num / 2

            self.terminal[1].value = array(binary[::-1])
