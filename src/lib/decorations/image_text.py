# -*- coding: utf-8 -*-

import os

from color import Color
from component import Component
from componenttypes import TYPE_DECORATION
from lib.pseqt import *  # @UnusedWildImport
import datetime as dt
import time as tm


class DecorationText(Component):
    '''
    Zobrazenie jednoducheho textu
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_DECORATION
        self.box = QRectF(0, 0, 100, 100)

        self.font = QFont('Decorative', 10)

        self.addParameter('Text', 'Simple text', color=Color.red)
        self.addParameter('Size', 15)

    def updateShape(self):
        '''
        Nastavenie vlastnosti obrazku pri vytvoreni objektu a po zmene hodnot parametrov.
        '''

        self.text = self.parameter['Text'].value
        self.color = self.parameter['Text'].color

        self.font = QFont('Decorative', self.parameter['Size'].value)
        self.font.setItalic(True)

    def drawShape(self, gc):
        gc.setFont(self.font)
        gc.setPen(QPen(self.color, 1))

        if six.PY2 is True:
            s = str(self.text.encode('utf-8'))
        else:
            s = self.text

        fm = QFontMetrics(self.font)
                                      # urcenie rozmerov textu a centrovanie vzhladom
        w = fm.width(s)		  # k zadanej polohe referencneho bodu
        h = fm.height()

        self.box = QRectF(0, 0, w, h)
        gc.drawText(self.box, Qt.AlignLeft, s)


# spatna kompatibilita
class ImageText(DecorationText):
    def __init__(self, name, pos):
        DecorationText.__init__(self, name, pos)


class DecorationFileName(Component):
    '''
    Zobrazenie mena suboru.
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_DECORATION
        self.box = QRectF(0, 0, 100, 100)

        self.font = QFont('Decorative', 10)

        self.addParameter('Text', 'filename.pse', color=Color.blue)
        self.addParameter('Size', 15)

    def updateShape(self):
        self.color = self.parameter['Text'].color

        self.font = QFont('Decorative', self.parameter['Size'].value)
        self.font.setItalic(True)

    def drawShape(self, gc):
        if self.diagram is not None:
            if os.path.exists(self.diagram.fileName):
                (head, s) = os.path.split(self.diagram.fileName)
                self.parameter['Text'].value = s
            else:
                self.parameter['Text'].value = 'Diagram not saved'

        else:
            self.parameter['Text'].value = 'filename.pse'

        gc.setFont(self.font)
        gc.setPen(QPen(self.color, 1))

        s = str(self.parameter['Text'].value)
        fm = QFontMetrics(self.font)
                              # urcenie rozmerov textu a centrovanie vzhladom
        w = fm.width(s)	   # k zadanej polohe referencneho bodu
        h = fm.height()

        self.box = QRectF(0, 0, w, h)
        gc.drawText(self.box, Qt.AlignLeft, s)


class DecorationTime(Component):
    '''
    Zobrazenie aktualneho casu
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_DECORATION
        self.box = QRectF(0, 0, 100, 100)

        self.font = QFont('Decorative', 10)

        s = tm.strftime("%H:%M:%S", dt.datetime.now().timetuple())

        self.addParameter('Text', s, color=Color.darkGreen)
        self.addParameter('Size', 15)

    def updateShape(self):
        self.color = self.parameter['Text'].color

        self.font = QFont('Decorative', self.parameter['Size'].value)
        self.font.setItalic(True)

    def drawShape(self, gc):
        self.parameter['Text'].value = tm.strftime("%H:%M:%S", dt.datetime.now().timetuple())

        gc.setFont(self.font)
        gc.setPen(QPen(self.color, 1))

        s = str(self.parameter['Text'].value)
        fm = QFontMetrics(self.font)
                              # urcenie rozmerov textu a centrovanie vzhladom
        w = fm.width(s)	   # k zadanej polohe referencneho bodu
        h = fm.height()

        self.box = QRectF(0, 0, w, h)
        gc.drawText(self.box, Qt.AlignLeft, s)
