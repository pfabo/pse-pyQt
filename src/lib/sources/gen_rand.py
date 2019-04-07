# -*- coding: utf-8 -*-
import random

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class GenRandInt(Component):
    """!
    @if English

    Return a random integer N such that a <= N <= b.

    @endif

    @if Slovak

    Return a random integer N such that a <= N <= b.

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'genint.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Upper limit', 63, visibleName=True)
        self.addParameter('Lower limit', 0, visibleName=True)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.green)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[1].value = 0
        elif flag == SIM_UPDATE:
            b = self.parameter['Upper limit'].value
            a = self.parameter['Lower limit'].value
            val = random.randint(a, b)
            self.terminal[1].value = val


class GenNoiseGauss(Component):
    """!
    @if English

    Noise with Gaussian distribution, Mean is the mean value and Sigma is the standard deviation.

    @endif


    @if Slovak

    \brief <H3><B>Generátor šumu</B></H3>

    Generátor šumu s normálnou (Gaussovou) distribúciou. Pre generátor je možné nastaviť
    strednú hodnotu generovaného šumu a štandardnú odchýlku.

    <B><I>Parametre komponentu</I></B>

    <I>Mean</I>

    Parameter definuje strednú hodnotu generovaného šumu. Stredná hodnota šumu je definovaná ako

    \f[ \mu = \frac{1}{N} \sum_{i=0}^{N-1} x_i \f]

    <I>Sigma</I>

    Parameter definuje štandardnú odchýlku generovaného šumu. Štandardná odchýlka šumu je definovaná ako

    \f[ \sigma^2 = \frac{1}{N-1} \sum_{i=0}^{N-1} (x_i - \mu)^2 \f]

    Maximálna hodnota amplitúdy šumu je úmerná  \f$ V_{max} = 6 ... 8 * \sigma \f$.

    <B>Literatúra</B>

    <B>Príklady</B>

    @endif
    """
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'gennoise.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Mean', 0.0, visibleName=True)
        self.addParameter('Sigma', 1.0, visibleName=True)

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.green)
        gc.setBrush(QBrush(grad))
        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[1].value = 0
        elif flag == SIM_UPDATE:
            m = self.parameter['Mean'].value
            s = self.parameter['Sigma'].value
            val = random.gauss(m, s)
            self.terminal[1].value = val
