from color import Color
from component import Component
from componenttypes import TYPE_SPICE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Diode(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SPICE
        self.box = QRectF(-30, -20, 60, 40)

        self.addParameter('Ref',  'D',    True, QPointF(0, -25), Color.black)
        self.addParameter('Value', 'DIODE', True, QPointF(0, 25), Color.blue)

        self.addTerminal('A', 1, TERM.INOUT, QPoint(-30, 0))
        self.addTerminal('K', 2, TERM.INOUT, QPoint(30, 0))

    def drawShape(self, gc):

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.moveTo(-30, 0)
        path.lineTo(-10, 0)

        path.moveTo(30, 0)
        path.lineTo(14, 0)

        path.moveTo(-10, -15)
        path.lineTo(-10, 15)
        path.lineTo(10, 0)
        path.lineTo(-10, -15)

        path.addRect(10, -13, 4, 26)
        gc.drawPath(path)
