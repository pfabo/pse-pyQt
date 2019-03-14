# -*- coding: utf-8 -*-
import logging
import os

from component import Component, PARAM
from componenttypes import TYPE_DECORATION
from lib.pseqt import *  # @UnusedWildImport


LOG = logging.getLogger(__name__)


class ImagePNG(Component):
    '''!
    @if English

    @endif

    @if Slovak

    Zobrazenie PNG obrazku

    @endif
    '''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_DECORATION
        self.box = QRectF(0, 0, 100, 100)

        img = './lib/decorations/img/vc_logo_en.png'
        self.addParameter('Image', img, paramType=PARAM.FILE_PNG)
        self.addParameter('Scale', 1.0)

    def updateShape(self):
        path = self.parameter['Image'].value
        # workaround pictures saved with ./src  or src prefix:
        if path.startswith('./src'):
            path = '.%s' % path[5:]
        if path.startswith('src'):
            path = '.%s' % path[3:]
        self.parameter['Image'].value
        # end of workaround

        if not os.path.exists(path):
            LOG.error('%s not exists' % path)
            path = './lib/decorations/img/error_png_import.png'
            # self.parameter['Image'].value = path
        self.png = QPixmap(path)

    def drawShape(self, gc):
        w = self.png.width() * self.parameter['Scale'].value
        h = self.png.height() * self.parameter['Scale'].value
        gc.drawPixmap(0, 0, w, h, self.png)
        self.box = QRectF(0, 0, w, h)
