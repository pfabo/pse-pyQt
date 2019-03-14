from color import Color
from component import Component
from componenttypes import TYPE_SPICE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class CapH(Component):
    '''
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SPICE
        self.box = QRectF(-30, -20, 60, 40)

        self.addParameter('Ref',  'C',  True, QPoint(0, -30), Color.black)
        self.addParameter('Value', '1nF', True, QPoint(0, 30), Color.blue)

        self.addTerminal('A', 1, TERM.INOUT, QPointF(-30, 0), TERM.DIR_WEST)
        self.addTerminal('B', 2, TERM.INOUT, QPointF(30, 0), TERM.DIR_EAST)

    def drawShape(self, gc):
        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.moveTo(-30, 0)
        path.lineTo(-5, 0)
        path.moveTo(30, 0)
        path.lineTo(5, 0)

        path.moveTo(5, 20)
        path.lineTo(5, -20)

        path.moveTo(-5, 20)
        path.lineTo(-5, -20)

        gc.drawPath(path)


class CapV(Component):
    '''
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SPICE
        self.box = QRectF(-20, -30, 40, 60)

        self.addParameter('Ref',  'C',  True, QPoint(20, -15), Color.black)
        self.addParameter('Value', '1nF', True, QPoint(20, 15), Color.blue)

        self.addTerminal('A', 1, TERM.INOUT, QPointF(0, -30))
        self.addTerminal('B', 2, TERM.INOUT, QPointF(0, 30))

    def drawShape(self, gc):
        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.moveTo(0, -30)
        path.lineTo(0, - 5)
        path.moveTo(0, 30)
        path.lineTo(0,  5)

        path.moveTo(20, 5)
        path.lineTo(-20, 5)

        path.moveTo(20, -5)
        path.lineTo(-20, -5)

        gc.drawPath(path)
