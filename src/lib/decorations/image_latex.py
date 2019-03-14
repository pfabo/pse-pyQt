# -*- coding: utf-8 -*-

from matplotlib.mathtext import MathTextParser

from component import Component
from componenttypes import TYPE_DECORATION
from lib.pseqt import *  # @UnusedWildImport


class ImageLaTex(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)
        self.compType = TYPE_DECORATION
        self.bitmapName = ''

        self.addParameter('LaTex', r'$ \Phi_E = \oint \ E \cdot d A $ ')

    def updateShape(self):
        try:
            self.bitmapName = './tmp/tex_bmp_' + str(self.uid) + '.png'
            q = MathTextParser('Bitmap')
            q.to_png(self.bitmapName, self.parameter['LaTex'].value)

            self.png = QPixmap(self.bitmapName)

        except:
            print ('>>> ERROR ImageLaTex.updateShape')
            print ('    Syntax Error - chyba pri update/parsovani LaTex retazca alebo renedrovani')
            print ('    obrazku ' + self.bitmapName)
            self.png = QPixmap(self.path + '/img/error_tex_format.png')

    def drawShape(self, gc):
        w = self.png.width()
        h = self.png.height()
        gc.drawPixmap(0, 0, w, h, self.png)
        self.box = QRectF(0, 0, w, h)
