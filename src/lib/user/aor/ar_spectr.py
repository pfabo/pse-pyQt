# -*- coding: utf-8 -*-

from numpy import array

from color import Color, convertColor
from component import Component
from componenttypes import SIM_INIT, TYPE_SIM_DISCRETE, SIM_STEP
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM
import numpy as np


class AR_Spectrogram(Component):

    """!
    @if English

    Spectrogram (Time & Frequecy & Amplitude Graph)

    @endif

    @if Slovak

    Zobrazenie spektrogramu v bitovej mape.

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.box = QRectF(-5, -5, 330, 210)
        self.shapeColor = Color.black

        self.addTerminal('IN', 1, TERM.IN, QPointF(-10, 100),
                         TERM.DIR_EAST, TERM.IN_ARROW_FILL, TERM.IN_ARROW)

        self.x = 0        # poloha aktualneho zapisu
        self.cursor = 1

    def updateShape(self):
        b = np.ones((320, 160)).astype(np.uint32) * 64
        self.image = QImage(b, 320, 160, QImage.Format_RGB32)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -5, 0, 200)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.mediumAquamarine)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-5, -5, 330, 210, 5, 5)

        gc.drawImage(0, 0, self.image.scaled(320, 200))

    def sim(self, flag, value, time, step):

        if flag == SIM_INIT:
            pass

        elif flag == SIM_STEP:
            w = self.terminal[1].value
            # ocakavame pole, ine hodnoty ignorujeme
            if type(w) == np.ndarray:

                for i in range(160):   # w:
                    R, G, B = convertColor(w[i] / 70.0)
                    p = (255 << 24 | R << 16 | G << 8 | B)
                    self.image.setPixel(self.x, i, p)
                    self.image.setPixel(self.cursor, i, 0xFF00FF00)

                self.x = self.x + 1
                self.cursor = self.cursor + 1

                if self.x >= 320:
                    self.x = 0

                if self.cursor >= 320:
                    self.cursor = 0


class AR_Spectrum(Component):

    '''
    @if English

    FFT Spectrum.

    @endif

    @if Slovak

    Zobrazenie FFT spektra

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.box = QRectF(-5, -5, 330, 210)
        self.shapeColor = Color.black

        self.addTerminal('IN', 1, TERM.IN, QPointF(-10, 100),
                         TERM.DIR_EAST, TERM.IN_ARROW_FILL, TERM.IN_ARROW)

        # integralna hodnota spektra
        self.intVal = []
        for i in range(10):
            self.intVal.append(np.zeros(160))
        self.intVal = array(self.intVal)

    def updateShape(self):
        b = np.ones((320, 160)).astype(np.uint32) * 0xFF073F32
        self.image = QImage(b, 320, 160, QImage.Format_RGB32)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -5, 0, 200)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.mediumAquamarine)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-5, -5, 330, 210, 5, 5)

        gc.drawImage(0, 0, self.image.scaled(320, 200))

    def sim(self, flag, value, time, step):

        if flag == SIM_INIT:
            pass

        elif flag == SIM_STEP:
            w = self.terminal[1].value
            # ocakavame pole, ine hodnoty ignorujeme
            if type(w) == np.ndarray:

                # integral - shift hodnot pola
                for i in range(9, 0, -1):
                    self.intVal[i] = self.intVal[i - 1]
                self.intVal[0] = w

                z = self.intVal[0]
                for i in range(1, 10):
                    z = z + self.intVal[i]
                z = z / 10.0

                for i in range(160):   # w:
                    R, G, B = convertColor(z[i] / 100.0)
                    p = (255 << 24 | R << 16 | G << 8 | B)

                    val = int(160.0 - z[i] * 1.60)
                    if val >= 160:
                        val = 159

                    for j in range(val):
                        self.image.setPixel(2 * i, j, 0x00073F32)
                        self.image.setPixel(2 * i + 1, j, 0x00073F32)

                    for j in range(val, 160):
                        self.image.setPixel(2 * i, j, p)       # val, 0x00FFFFFF)
                        self.image.setPixel(2 * i + 1, j, p)  # val, 0x00FFFFFF)

                # zobrazenie spektra v bitovej mape
                for i in range(160):   # w:
                    # uprava y-rozsahu hodnot do skaly grafu
                    val = int(160.0 - w[i] * 1.60)
                    if val >= 160:
                        val = 159

                    self.image.setPixel(2 * i, val, 0x00FFFFFF)
                    self.image.setPixel(2 * i + 1, val, 0x00FFFFFF)
