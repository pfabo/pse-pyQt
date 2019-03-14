# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_INIT, SIM_UPDATE, SIM_FINISH
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class WdSpinbox(Component):
    '''Horizontalny spinbox.'''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(0, -10, 10, 20)

        self.addParameter('Min',   0)
        self.addParameter('Max', 100)

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(10, 0),  TERM.DIR_EAST)

        self.spinbox = QSpinBox()
        self.spinbox.valueChanged.connect(self.spinboxValueChanged)
        self.isEmbedded = False

        self.value = 0

    def spinboxValueChanged(self):
        self.value = self.spinbox.value()

    def updateShape(self):
        self.spinbox.setMinimum(self.parameter['Min'].value)
        self.spinbox.setMaximum(self.parameter['Max'].value)

        sc = self.scene()
        if sc != None and self.isEmbedded == False:
            sc.addWidget(self.spinbox)
            self.isEmbedded = True

    def deleteShape(self):
        self.spinbox.setVisible(False)

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.moveTo(10, 0)
        path.lineTo(0, 0)
        gc.drawPath(path)

        x = self.position.x()
        y = self.position.y()
        w = self.spinbox.width()
        h = self.spinbox.height()
        self.spinbox.move(x - w, y - h / 2)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.value = self.spinbox.value()

        elif flag == SIM_UPDATE:
            self.terminal[1].value = self.value

        elif flag == SIM_FINISH:
            pass
