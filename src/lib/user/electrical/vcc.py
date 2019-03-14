from color import Color
from component import Component
from componenttypes import TYPE_SPICE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Vcc(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)
        self.compType = TYPE_SPICE
        self.box = QRectF(-10, -25, 20, 30)

        self.addParameter('Vcc', '+5V', True, QPointF(0, -35), Color.blue)
        self.addTerminal('A', 1, TERM.INOUT, QPointF(0, 0), TERM.DIR_WEST)

    def drawShape(self, gc):
        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.moveTo(0, 0)
        path.lineTo(0, -15)
        path.addEllipse(-5, -25, 10, 10)
        gc.drawPath(path)
