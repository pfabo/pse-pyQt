from color import Color
from component import Component
from componenttypes import TYPE_SPICE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class ResH(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SPICE
        self.box = QRectF(-40, -10, 80, 20)

        self.addParameter('Ref',  'R',  True, QPointF(0, -15), Color.black)
        self.addParameter('Value', '4k7', True, QPointF(0, 15), Color.blue)

        self.addTerminal('A', 1, TERM.INOUT, QPointF(-40, 0))
        self.addTerminal('B', 2, TERM.INOUT, QPointF(40, 0))

    def drawShape(self, gc):

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.addRect(-23, -8, 46, 16)
        path.moveTo(-40, 0)
        path.lineTo(-23, 0)
        path.moveTo(40, 0)
        path.lineTo(23, 0)

        gc.drawPath(path)


class ResV(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SPICE
        self.box = QRectF(-10, -40, 20, 80)

        self.addParameter('Ref',  'R', True, QPointF(20, -10), Color.black)
        self.addParameter('Value', '1k', True, QPointF(20, 10), Color.blue)

        self.addTerminal('A', 1, TERM.INOUT, QPointF(0, -40))
        self.addTerminal('B', 2, TERM.INOUT, QPointF(0, 40))

    def drawShape(self, gc):

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.addRect(-8, -23, 16, 46)
        path.moveTo(0, -40)
        path.lineTo(0, -23)
        path.moveTo(0, 40)
        path.lineTo(0, 23)

        gc.drawPath(path)
