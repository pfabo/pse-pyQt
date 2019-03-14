# -*- coding: utf-8 -*-

from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_INIT, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class WdDial(Component):
    '''Widget s potenciometrom'''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(-10, 0, 20, 20)

        self.addParameter('Min',   0)
        self.addParameter('Max', 100)

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(0, 10))

        self.slider = QDial()
        self.slider.valueChanged.connect(self.sliderValueChanged)
        self.isEmbedded = False

        self.value = 0

    def sliderValueChanged(self):
        self.value = self.slider.value()

    def updateShape(self):
        self.slider.setMinimum(self.parameter['Min'].value)
        self.slider.setMaximum(self.parameter['Max'].value)

        sc = self.scene()
        if sc is not None and self.isEmbedded is False:
            sc.addWidget(self.slider)
            self.isEmbedded = True

    def deleteShape(self):
        self.slider.setVisible(False)

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.moveTo(0, 10)
        path.lineTo(0, 0)
        gc.drawPath(path)

        x = self.position.x()
        y = self.position.y()
        w = self.slider.width()
        h = self.slider.height()
        self.slider.move(x - w / 2, y - h)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.value = self.slider.value()

        elif flag == SIM_UPDATE:
            self.terminal[1].value = self.value
