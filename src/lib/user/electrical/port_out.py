from color import Color
from component import Component
from componenttypes import TYPE_SPICE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class NetOut(Component):
    '''
    Prepojovaci komponent sieti.
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SPICE
        self.box = QRectF(0, -10, 50, 20)

        self.addParameter('Ref', 'A')
        self.addParameter('Port', 'A', True, QPointF(25, 0), Color.blue)
        self.addTerminal('OUT', 1, TERM.CONN, QPointF(0, 0),
                         TERM.DIR_WEST,
                         TERM.OUT_ARROW_SMALL_FILL,
                         TERM.OUT_ARROW_SMALL)

    def drawShape(self, gc):
        '''
        '''
        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        path.moveTo(0, 0)
        path.lineTo(10, -10)
        path.lineTo(45, -10)

        path.moveTo(0, 0)
        path.lineTo(10, 10)
        path.lineTo(45, 10)

        path.lineTo(50, 5)
        path.lineTo(50, -5)
        path.lineTo(45, -10)

        gc.drawPath(path)
