from color import Color
from component import Component
from componenttypes import TYPE_SPICE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Opamp(Component):
    '''
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SPICE
        self.box = QRectF(0, 10, 80, 60)

        self.addParameter('Ref',  'A',  True, QPointF(50, 20), Color.black)
        self.addParameter('Value', 'OP', True, QPointF(50, 60), Color.blue)

        self.addTerminal('IN+', 1, TERM.INOUT, QPoint(0, 20))
        self.addTerminal('IN-', 2, TERM.INOUT, QPoint(0, 60))
        self.addTerminal('OUT', 3, TERM.INOUT, QPoint(80, 40))

    def drawShape(self, gc):

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.moveTo(0, 20)
        path.lineTo(10, 20)

        path.moveTo(0, 60)
        path.lineTo(10, 60)

        path.moveTo(70, 40)
        path.lineTo(80, 40)

        path.moveTo(10, 10)
        path.lineTo(10, 70)
        path.lineTo(70, 40)
        path.lineTo(10, 10)

        path.moveTo(13, 20)
        path.lineTo(21, 20)

        path.moveTo(13, 60)
        path.lineTo(21, 60)

        path.moveTo(17, 56)
        path.lineTo(17, 64)

        gc.drawPath(path)
