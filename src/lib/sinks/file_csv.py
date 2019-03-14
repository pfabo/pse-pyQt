# -*- coding: utf-8 -*-
from numpy import ndarray

from color import Color
from component import Component, PARAM
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_UPDATE, SIM_INIT, SIM_FINISH
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class FileCSV(Component):
    '''
    Zapis hodnot terminalu do textoveho suboru.

    @todo vyber typu delimiteru
    @todo vyber typu ukoncenia riadku
    @todo synchronizacia na externy clock
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.shapeImage = 'file_write_csv.svg'
        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeColor = Color.blue
        self.box = QRectF(-30, -30, 60, 60)

        term_in = self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0),
                                   TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL,
                                    TERM.IN_ARROW_SMALL)
        term_in.termDiscColor = Color.black       # farby pre vstup - vektor
        term_in.termDiscFill = Color.white
        term_in.termConnColor = Color.black
        term_in.termConnFill = Color.black

        self.addParameter('File', 'log_data.csv', paramType=PARAM.FILE_CSV_SAVE)
        self.addParameter('Append', False, paramType=PARAM.BOOL)

        self.__fp = None

    def drawShape(self, gc):

        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.mediumAquamarine)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            if self.parameter['Append'].value:
                mode = 'a'
            else:
                mode = 'w'
            self.__fp = open(self.parameter['File'].value, mode)

        elif flag == SIM_UPDATE:
            inp = self.terminal[1].value
            if type(inp) == ndarray:
                s = ','.join([str(val) for val in inp])
            else:
                s = str(inp)
            self.__fp.write(s + '\n')

        elif flag == SIM_FINISH:
            self.__fp.close()
