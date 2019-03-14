# -*- coding: utf-8 -*-

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTROL
from lib.pseqt import *
from sim import SIM_SPICE


class Generator_SPICE(Component):

    '''
    Generator - NgSpice script
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTROL
        self.box = QRectF(-10, -10, 60, 60)
        self.shapeColor = Color.black
        self.solver = SIM_SPICE

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -5, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.cyan)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-5, -5, 50, 50, 5, 5)

        font = QFont('Decorative', 12)
        font.setItalic(True)
        gc.setFont(font)
        gc.setPen(QPen(Color.blue, 1))
        gc.drawText(self.box, Qt.AlignCenter, 'SPC')
