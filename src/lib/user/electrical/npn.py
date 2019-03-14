from color import Color
from component import Component
from componenttypes import TYPE_SPICE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Npn(Component):
    '''
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SPICE
        self.box = QRectF(0, 0, 40, 60)

        self.shapeImage = 'npn.svg'

        self.addParameter('Ref',  'Q',    True, QPointF(10, 10), Color.black)
        self.addParameter('Value', 'NPN', True, QPointF(10, 60), Color.blue)

        self.addTerminal('B', 1, TERM.INOUT, QPointF(0, 30), TERM.DIR_WEST)
        self.addTerminal('C', 2, TERM.INOUT, QPointF(40, 60), TERM.DIR_NORTH)
        self.addTerminal('E', 3, TERM.INOUT, QPointF(40, 0), TERM.DIR_SOUTH)

    def drawShape(self, gc):
        self.shapeSvg.render(gc)
