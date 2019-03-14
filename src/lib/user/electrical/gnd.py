from component import Component
from componenttypes import TYPE_SPICE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Gnd(Component):
    '''
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)
        self.compType = TYPE_SPICE
        self.box = QRectF(-20, 0, 40, 23)

        self.addTerminal('GND', 1, TERM.INOUT, QPointF(0, 0), TERM.DIR_WEST)

    def drawShape(self, gc):
        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))
        path.moveTo(0, 0)
        path.lineTo(0, 20)
        path.addRect(-15, 20, 30, 3)
        gc.drawPath(path)
