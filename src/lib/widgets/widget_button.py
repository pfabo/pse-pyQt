# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class WdButton(Component):
    '''
    Tlacitko generujuce hodnotu True pri stlaceni (False pri uvolneni).
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(0, -10, 20, 20)

        self.addParameter('Text', 'SET')

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(10, 0))

        self.button = QPushButton()
        self.button.pressed.connect(self.buttonPressed)
        self.button.released.connect(self.buttonReleased)
        self.isEmbedded = False

        self.value = False

    def buttonPressed(self):
        self.value = True

    def buttonReleased(self):
        self.value = False

    def updateShape(self):

        s = self.parameter['Text'].value
        self.button.setText(s)

        sc = self.scene()
        if sc is not None and self.isEmbedded is False:
            sc.addWidget(self.button)
            self.isEmbedded = True

    def deleteShape(self):
        self.button.setVisible(False)

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.moveTo(10, 0)
        path.lineTo(0, 0)
        gc.drawPath(path)

        x = self.position.x()
        y = self.position.y()
        w = self.button.width()
        h = self.button.height()
        self.button.move(x - w, y - h / 2)

    def sim(self, flag, value, time, step):
        self.terminal[1].value = self.value


class WdButtonSwitch(Component):
    '''
    Tlacitko prepinajuce hodnotu True/False pri stlaceni.
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(0, -10, 20, 20)

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(10, 0))

        self.button = QPushButton()
        self.button.pressed.connect(self.buttonPressed)

        self.palette = self.button.palette()
        self.palette.setColor(self.palette.ButtonText, Color.red)
        self.button.setPalette(self.palette)

        self.isEmbedded = False

        self.value = False

    def buttonPressed(self):
        if self.value is False:
            self.value = True
            self.button.setText('True')
        else:
            self.value = False
            self.button.setText('False')

    def updateShape(self):
        self.value = False
        self.button.setText('False')

        sc = self.scene()
        if sc is not None and self.isEmbedded is False:
            sc.addWidget(self.button)
            self.isEmbedded = True

    def deleteShape(self):
        self.button.setVisible(False)

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.moveTo(10, 0)
        path.lineTo(0, 0)
        gc.drawPath(path)

        x = self.position.x()
        y = self.position.y()
        w = self.button.width()
        h = self.button.height()
        self.button.move(x - w, y - h / 2)

    def sim(self, flag, value, time, step):
        self.terminal[1].value = self.value
