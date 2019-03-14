# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_DISCRETE, SIM_INIT, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class WdProgressBar(Component):
    '''Widget s vertikalnym sliderom.'''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.box = QRectF(-20, -10, 20, 20)

        self.addParameter('Min',   0.0)
        self.addParameter('Max', 100.0)

        self.addTerminal('IN', 1, TERM.IN, QPointF(-10, 0))

        self.bar = QProgressBar()
        self.isEmbedded = False

        self.value = 0

    def updateShape(self):
        self.bar.setMinimum(self.parameter['Min'].value)
        self.bar.setMaximum(self.parameter['Max'].value)

        sc = self.scene()
        if sc is not None and self.isEmbedded is False:
            sc.addWidget(self.bar)
            self.isEmbedded = True

    def deleteShape(self):
        self.bar.setVisible(False)

    def drawShape(self, gc):
        gc.setPen(QPen(self.shapeColor))
        path = QPainterPath()
        path.moveTo(-10, 0)
        path.lineTo(0, 0)
        gc.drawPath(path)

        x = self.position.x()
        y = self.position.y()
        h = self.bar.height()
        self.bar.move(x, y - h / 2)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.bar.setValue(0)

        if flag == SIM_UPDATE:
            inp = self.terminal[1].value
            self.bar.setValue(inp)
