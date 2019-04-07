# -*- coding: utf-8 -*-
from numpy import fmod

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class GenPulse(Component):
    '''!
    @if Slovak
    @brief Všeobecný generátor impulzov.

    Vlastnosti generátora sa nastavujú nasledujúcimi parametrami
    - <B>Amplitude</B> Amplitúda (rozkmit) impulzov
    - <B>Offset</B> Posunutie jednosmernej úrovne výstupného signálu voči nule
    - <B>Frequency</B> Frekvenci impulzov vztiahnutá k systémovému času
    - <B>Pulse Width</B> Šírka implulzu, rozsah 0% - 100%
    - <B>Phase</B> Fáza impluzov
    - <B>Polarity</B> Polarita impulzov (True/False)
    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'genpulse.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Amplitude', 1.0, visibleName=True)    # +/- aplituda kmitov
        self.addParameter('Offset', 0.0, visibleName=True)       # offset voci nule
        self.addParameter('Frequency', 1.0, visibleName=True)    # frekvencia v abs. hodnote casu
        self.addParameter('Pulse Width', 50, visibleName=True)   # sirka pulzu v %
        self.addParameter('Phase', 0.0, visibleName=True)        # faza impulzu
        self.addParameter('Polarity', 'True', visibleName=True)  # polarita True/False

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.green)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def updateShape(self):
        super(GenPulse, self).updateShape()
        self.ampl = self.parameter['Amplitude'].value
        self.offs = self.parameter['Offset'].value
        self.f = self.parameter['Frequency'].value
        self.w = self.parameter['Pulse Width'].value
        self.ph = self.parameter['Phase'].value
        pol = self.parameter['Polarity'].value

        # kontrola hodnoty parametra
        if self.f <= 0:
            self.f = 1e-38

        self.pol = True
        if pol in ['True', 'T', 'true', 't', '1']:
            self.parameter['Polarity'].value = 'True'
        else:
            self.pol = False
            self.parameter['Polarity'].value = 'False'

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[1].value = 0
        else:

            q = fmod(time + self.ph, 1 / self.f)

            if q * self.f <= self.w * 0.01:
                value = self.ampl
            else:
                value = -self.ampl

            if self.pol is False:
                value = -value

            self.terminal[1].value = value + self.offs


class GenOneShot(Component):
    '''!
    @if Slovak
    @brief Všeobecný generátor jednotlivého impulzu.

    Vlastnosti generátora sa nastavujú nasledujúcimi parametrami
    - <B>Amplitude</B> Amplitúda (rozkmit) impulzov
    - <B>Offset</B> Posunutie jednosmernej úrovne výstupného signálu voči nule
    - <B>Start</B> Začiatok impulzu
    - <B>Stop</B> Koniec impulzu
    - <B>Polarity</B> Polarita impulzu (True/False)
    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'oneshot.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Amplitude', 1.0, visibleName=True)    # +/- aplituda kmitov
        self.addParameter('Offset', 0.0, visibleName=True)       # offset voci nule
        self.addParameter('Start', 1.0, visibleName=True)        # zaciatok
        self.addParameter('Stop', 2.0, visibleName=True)           # koniec
        self.addParameter('Polarity', 'True', visibleName=True)  # polarita True/False

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.green)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def updateShape(self):
        super(GenOneShot, self).updateShape()
        self.ampl = self.parameter['Amplitude'].value
        self.offs = self.parameter['Offset'].value
        self.start = self.parameter['Start'].value
        self.stop = self.parameter['Stop'].value
        pol = self.parameter['Polarity'].value

        # kontrola hodnoty parametra
        if self.start < 0.0:
            self.start = 0.0
            self.parameter['Start'].value = self.start

        if self.stop < 0.0:
            self.stop = 0.0
            self.parameter['Stop'].value = self.stop

        if self.start >= self.stop:    # chybne zadanie, default hodnoty
            self.start = 1.0
            self.stop = 2.0
            self.parameter['Start'].value = self.start
            self.parameter['Stop'].value = self.stop

        self.pol = True
        if pol in ['True', 'T', 'true', 't', '1']:
            self.parameter['Polarity'].value = 'True'
        else:
            self.pol = False
            self.parameter['Polarity'].value = 'False'

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            if self.pol is True:
                self.terminal[1].value = -self.ampl + self.offs
            else:
                self.terminal[1].value = self.ampl + self.offs
        else:

            if time >= self.start and time <= self.stop:
                value = self.ampl
            else:
                value = -self.ampl

            if self.pol is False:
                value = -value

            self.terminal[1].value = value + self.offs


class GenPulseSeq(Component):
    '''!
    @if Slovak
    @brief Všeobecný generátor postupnosti impulzov.

    Vlastnosti generátora sa nastavujú nasledujúcimi parametrami
    - <B>Amplitude</B> Amplitúda (rozkmit) impulzov
    - <B>Offset</B> Posunutie jednosmernej úrovne výstupného signálu voči nule
    - <B>Start</B> Začiatky impulzov
    - <B>Stop</B> Konce impulzu
    - <B>Polarity</B> Polarita impulzov (True/False)
    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'pulseseq.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Amplitude', 1.0, visibleName=True)    # +/- aplituda kmitov
        self.addParameter('Offset', 0.0, visibleName=True)       # offset voci nule
        self.addParameter('Start', '[1.0, 2.0]', visibleName=True)        # zaciatok
        self.addParameter('Stop', '[1.5, 3.0]', visibleName=True)           # koniec
        self.addParameter('Polarity', 'True', visibleName=True)  # polarita True/False

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.green)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def updateShape(self):
        super(GenPulseSeq, self).updateShape()

        self.ampl = self.parameter['Amplitude'].value
        self.offs = self.parameter['Offset'].value
        pol = self.parameter['Polarity'].value

        s1 = self.parameter['Start'].value
        s1 = s1.replace('[', '')  # uprava retazca
        s1 = s1.replace(']', '')
        q1 = s1.split(',')
        self.start = []
        for i in q1:
            self.start.append(float(i))

        s2 = self.parameter['Stop'].value
        s2 = s2.replace('[', '')  # uprava retazca
        s2 = s2.replace(']', '')
        q2 = s2.split(',')
        self.stop = []
        for i in q2:
            self.stop.append(float(i))

        self.pol = True
        if pol in ['True', 'T', 'true', 't', '1']:
            self.parameter['Polarity'].value = 'True'
        else:
            self.pol = False
            self.parameter['Polarity'].value = 'False'

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            if self.pol is True:
                self.terminal[1].value = -self.ampl + self.offs
            else:
                self.terminal[1].value = self.ampl + self.offs
        else:

            value = -self.ampl

            try:
                for i in range(len(self.start)):
                    if time >= self.start[i] and time <= self.stop[i]:
                        value = self.ampl
                        break
            except:
                # chybne hodnoty v poliach
                pass

            if self.pol is False:
                value = -value
            self.terminal[1].value = value + self.offs
