# -*- coding: utf-8 -*-
import logging
import os

from component import Component, PARAM
from componenttypes import TYPE_DECORATION
from lib.pseqt import *  # @UnusedWildImport


LOG = logging.getLogger(__name__)


class ImageSVG(Component):
    '''!
    @if English

    @endif

    @if Slovak

    Zobrazenie SVG obrazku

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_DECORATION
        self.box = QRectF(0, 0, 100, 100)     # rozmery boxu obrazku su urcene az po renderovani
        img = './lib/decorations/img/pse_logo.svg'
        self.addParameter('Image', img, paramType=PARAM.FILE_SVG)
        self.addParameter('Width', 128)
        self.addParameter('Height', 256)

    def updateShape(self):
        # kontrola cesty k obrazku, v pripade neexistujuceho suboru zobrazenie
        # obrazku s chybovym hlasenim
        path = self.parameter['Image'].value
        # workaround pictures saved with src prefix:
        if path.startswith('./src'):
            path = '.%s' % path[5:]
        # end of workaround

        if not os.path.exists(path):
            LOG.error('%s not exists' % path)
            path = './lib/decorations/img/error_svg_import.svg'
        self.svg = QSvgWidget(path)

        # kontrola rozmerov obrazku - rozmery musia byt nenulove a kladne
        if self.parameter['Width'].value <= 0:
            self.parameter['Width'].value = 1

        if self.parameter['Height'].value <= 0:
            self.parameter['Height'].value = 1

        size = self.svg.sizeHint()
        size.scale(self.parameter['Width'].value, self.parameter['Height'].value, Qt.KeepAspectRatio)
        self.svg.setMaximumSize(size)

        # uprava zobrazenia, priesvitne pozadie obrazku
        pal = QPalette(self.svg.palette()) 			 # kopia existujucej palety
        pal.setColor(QPalette.Window, QColor(Qt.transparent))   # nastavenie farby - vyber podla vlastnosti
        self.svg.setPalette(pal)

    def drawShape(self, gc):
        self.svg.render(gc)
        w = self.svg.width()
        h = self.svg.height()
        self.box = QRectF(0, 0, w, h)
