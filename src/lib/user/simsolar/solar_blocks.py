# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

from math import radians, sin, cos
from numpy import array, ndarray

from color import Color
from component import Component
from componenttypes import SIM_INIT, TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM
import datetime as dt
import time as tm

from .pysolar import radiation
from .pysolar import solar


class IncidenceAngle(Component):
    '''!
    @if English

    @endif

    @if Slovak

    Korekčný koeficient - cos uhla medzi normalou k ploche a polohovym vektorom slnka

    Parametre:

    AL - vyska slnka nad obzorom
    AZ - azimut - uhol k NORTH
    EL - uhol naklonu plochy k rovine
    DR - azimut plochy - uhol k NORTH

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'inc_angle.svg'

        self.box = QRectF(-40, -50, 80, 100)
        self.shapeColor = Color.red

        t1 = self.addTerminal('AL', 1, TERM.IN, QPointF(-40, -30), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t1.termNameShow = True
        t1.posName = QPoint(7, 5)

        t2 = self.addTerminal('AZ', 2, TERM.IN, QPointF(-40, -10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t2.termNameShow = True
        t2.posName = QPoint(7, 5)

        t3 = self.addTerminal('EL', 3, TERM.IN, QPointF(-40, 10), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t3.termNameShow = True
        t3.posName = QPoint(7, 5)

        t3 = self.addTerminal('DR', 4, TERM.IN, QPointF(-40, 30), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t3.termNameShow = True
        t3.posName = QPoint(7, 5)

        self.addTerminal('OUT', 5, TERM.OUT, QPointF(40, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

    def drawShape(self, gc):
        '''
        '''
        grad = QLinearGradient(0, -35, 0, 70)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.seaGreen)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-35, -40, 70, 80, 5, 5)

        self.drawIcon(gc, -10, -20)

    def sim(self, flag, value, time, step):
        alt = radians(self.terminal[1].value)      # alpha - oznacenie podla teorie
        azm = radians(self.terminal[2].value)      # A
        elv = radians(self.terminal[3].value)      # beta
        ddr = radians(self.terminal[4].value)      # gamma

        ca = sin(alt) * cos(elv) + cos(alt) * sin(elv) * cos(ddr - azm)

        if ca >= 0.0:
            self.terminal[5].value = ca
        else:
            ca = 0.0


class Azimut(Component):
    '''!
    @if English

    @endif

    @if Slovak

    Určenie azimutu slnka pre stanoveny deň/čas a polohu na zemi.

    Poloha je určená vstupmi LAT (zemepisná šírka) a LNG (zemepisná dĺžka). Vstup DT určuje čas
    sekundách počítaný od referenčného dátumu (1.1.1970, 0:00, konverziu aktualneho casu prevedie
    komponent Date2Epoch ).

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'azimut.svg'

        self.box = QRectF(-40, -40, 80, 80)
        self.shapeColor = Color.red

        t1 = self.addTerminal('LAT', 1, TERM.IN, QPointF(-40, -20), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t1.termNameShow = True
        t1.posName = QPoint(7, 5)

        t2 = self.addTerminal('LNG', 2, TERM.IN, QPointF(-40, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t2.termNameShow = True
        t2.posName = QPoint(7, 5)

        t3 = self.addTerminal('DT', 3, TERM.IN, QPointF(-40, 20), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t3.termNameShow = True
        t3.posName = QPoint(7, 5)

        self.addTerminal('AZM', 4, TERM.OUT, QPointF(40, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Fast', 0)

    def drawShape(self, gc):
        '''
        '''
        grad = QLinearGradient(0, -35, 0, 70)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.seaGreen)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-35, -35, 70, 70, 5, 5)

        self.drawIcon(gc, -10, -20)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[4].value = 0
        else:
            srk = self.terminal[1].value
            dlk = self.terminal[2].value
            inp = self.terminal[3].value

            if (type(inp) == ndarray) or (type(inp) == list):
                inp = self.terminal[3].value[0]

            if inp > 0:
                d = dt.datetime.fromtimestamp(inp)
                if self.parameter['Fast'].value == 0:
                    angle = solar.GetAzimuth(srk, dlk, d)
                else:
                    angle = solar.GetAzimuthFast(srk, dlk, d)

                # konverzia pre azimut od severneho smeru
                angle = 180 - angle
                if angle >= 360:
                    angle = angle - 360
                self.terminal[4].value = angle
            else:
                self.terminal[4].value = 0


class Altitude(Component):
    '''!
    @if English

    @endif

    @if Slovak

    Určenie výšky slnka nad obzorom pre stanoveny deň/čas a polohu na zemi.

    Výška je určená vstupmi LAT (zemepisná šírka) a LNG (zemepisná dĺžka). Vstup DT určuje čas
    sekundách počítaný od referenčného dátumu (1.1.1970, 0:00, konverziu aktualneho casu prevedie
    komponent Date2Epoch ).

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'altitude.svg'

        self.box = QRectF(-40, -40, 80, 80)
        self.shapeColor = Color.red

        t1 = self.addTerminal('LAT', 1, TERM.IN, QPointF(-40, -20), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t1.termNameShow = True
        t1.posName = QPoint(7, 5)

        t2 = self.addTerminal('LNG', 2, TERM.IN, QPointF(-40, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t2.termNameShow = True
        t2.posName = QPoint(7, 5)

        t3 = self.addTerminal('DT', 3, TERM.IN, QPointF(-40, 20), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t3.termNameShow = True
        t3.posName = QPoint(7, 5)

        self.addTerminal('ALT', 4, TERM.OUT, QPointF(40, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Fast', 0)

    def drawShape(self, gc):
        '''
        '''
        grad = QLinearGradient(0, -35, 0, 70)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.seaGreen)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-35, -35, 70, 70, 5, 5)

        self.drawIcon(gc, -10, -20)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[4].value = 0
        else:
            srk = self.terminal[1].value
            dlk = self.terminal[2].value
            inp = self.terminal[3].value

            if (type(inp) == ndarray) or (type(inp) == list):
                inp = self.terminal[1].value[0]

            if inp > 0:
                d = dt.datetime.fromtimestamp(inp)
                if self.parameter['Fast'].value == 0:
                    self.terminal[4].value = solar.GetAltitude(srk, dlk, d)
                else:
                    self.terminal[4].value = solar.GetAltitudeFast(srk, dlk, d)
            else:
                self.terminal[4].value = 0


class Radiation(Component):
    '''!
    @if English

    @endif

    @if Slovak

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'radiation.svg'

        self.box = QRectF(-40, -40, 80, 80)
        self.shapeColor = Color.red

        t1 = self.addTerminal('LAT', 1, TERM.IN, QPointF(-40, -20), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t1.termNameShow = True
        t1.posName = QPoint(7, 5)

        t2 = self.addTerminal('LNG', 2, TERM.IN, QPointF(-40, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t2.termNameShow = True
        t2.posName = QPoint(7, 5)

        t3 = self.addTerminal('DT', 3, TERM.IN, QPointF(-40, 20), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t3.termNameShow = True
        t3.posName = QPoint(7, 5)

        self.addTerminal('PWR', 4, TERM.OUT, QPointF(40, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

    def drawShape(self, gc):
        '''
        '''
        grad = QLinearGradient(0, -35, 0, 70)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.seaGreen)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-35, -35, 70, 70, 5, 5)

        self.drawIcon(gc, -10, -20)

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            self.terminal[4].value = 0
        else:
            srk = self.terminal[1].value
            dlk = self.terminal[2].value
            inp = self.terminal[3].value

            if (type(inp) == ndarray) or (type(inp) == list):
                inp = self.terminal[1].value[0]

            if inp > 0:
                d = dt.datetime.fromtimestamp(inp)
                angle = solar.GetAltitude(srk, dlk, d)
                self.terminal[4].value = radiation.GetRadiationDirect(d, angle)
            else:
                self.terminal[4].value = 0


class Date2Epoch(Component):
    '''!
    @if English

    @endif

    @if Slovak

    Konvertuje vektor s hodnotami dátumu a času na sekundový údaj od referenčného
    okamžiku (1.1.1970, 0:00).

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'dt_sec.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.red

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

    def drawShape(self, gc):
        '''
        '''
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.seaGreen)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        # referencny datum
        temp = [1970, 1, 1, 0, 0, 0]

        inp = self.terminal[1].value

        if (type(inp) == ndarray) or (type(inp) == list):
            # osetrenie pri inicializacii / resete - vsetky hodnoty su nulove
            if int(inp[0]) >= 1970:
                for i in range(len(inp)):
                    if i < 6:
                        temp[i] = int(inp[i])
        else:
            if flag != SIM_INIT:
                print('>>> Warning - Component Date2Epoch')
                print('    Wrong input vector format ')

        d = dt.datetime(temp[0], temp[1], temp[2], temp[3], temp[4], temp[5])

        self.terminal[2].value = tm.mktime(d.timetuple())


class Epoch2Date(Component):
    '''!
    @if Slovak

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'sec_dt.svg'

        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.red

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('OUT', 2, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

    def drawShape(self, gc):
        '''
        '''
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.seaGreen)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        inp = self.terminal[1].value

        if (type(inp) == ndarray) or (type(inp) == list):
            inp = self.terminal[1].value[0]

        if inp > 0:
            d = dt.datetime.fromtimestamp(inp)
            array = [d.year, d.month, d.day, d.hour, d.minute, d.second]
            self.terminal[2].value = array
        else:
            # print - warning, negativna vstupna hodnota
            self.terminal[2].value = [1970, 1, 1, 0, 0, 0]
