# -*- coding: utf-8 -*-
from numpy import arange, sin, ndarray

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT, SIM_RESET, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Plot_DT(Component):
    '''Time plot - dot plot'''
    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.maxLines = 8		# maximalny pocet zobrazenych grafov
        self.numTraces = 1          # aktualny pocet zobrazovanych stop (dlzka vstupnych dat)

        self.x_size = 240
        self.y_size = 180

        self.data_x = []		# datove polia
        self.data_y = []

        for i in range(self.maxLines):
            self.data_y.append([])

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-5, -5, self.x_size + 10, self.y_size + 10)
        self.shapeColor = Color.blue

        term_in = self.addTerminal('IN', 1, TERM.IN, QPointF(-10, 90),
                                   TERM.DIR_EAST, TERM.IN_ARROW_FILL, TERM.IN_ARROW)
        term_in.termDiscColor = Color.black  # farby pre vstup - vektor
        term_in.termDiscFill = Color.white
        term_in.termConnColor = Color.black
        term_in.termConnFill = Color.black

        self.addParameter('Y-Max', 5.0)
        self.addParameter('Y-Min', -5.0)
        self.addParameter('X-Base', 10.0)

        self.colors = [Color.red, Color.black, Color.green, Color.blue]

        # demo data
        self.data_y.append([])
        self.data_x = arange(0, 10, 0.05)
        self.data_y[0] = 2 * sin(3 * self.data_x)

    def updateShape(self):
        # zmazanie demo-dat, ak doslo k zmene mierky grafu
        # po nacitani parametrov objektu zo suboru
        if(self.parameter['Y-Max'].value != 5.0 or
                self.parameter['Y-Min'].value != -5.0 or
                self.parameter['X-Base'].value != 10):
            self.data_x = []
            self.data_y = []

    def drawShape(self, gc):
        grad = QLinearGradient(0, -5, 0, 180)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.lightSteelBlue)  # yellow)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-5, -5, self.x_size + 10, self.y_size + 10, 5, 5)

        # vykreslenie mriezky a okraju grafu

        gc.setPen(QPen(Color.steelBlue, 1))
        gc.drawRect(0, 0, self.x_size, self.y_size)

        gc.setPen(QPen(Color.lightGrey, 1))
        xtics = 10
        ddx = self.x_size / xtics
        path = QPainterPath()
        for j in range(1, xtics):
            path.moveTo(ddx * j, 0)
            path.lineTo(ddx * j, self.y_size)
        gc.drawPath(path)

        ytics = 8
        ddy = self.y_size / ytics
        path = QPainterPath()
        for j in range(1, ytics):
            path.moveTo(0, ddy * j)
            path.lineTo(self.x_size, ddy * j)
        gc.drawPath(path)

        ymax = self.parameter[
            'Y-Max'].value  # TODO - kontrola nastavenie rozsahov
        ymin = self.parameter['Y-Min'].value

        maxTime = self.parameter['X-Base'].value
        cx = self.x_size / maxTime
        cy = self.y_size / (ymax - ymin)
        dy = (ymax + ymin) / 2.0

        lines = 1
        if type(self.terminal[1].value) == ndarray:
            lines = len(self.terminal[1].value)

        # kontrola na dlzku datoveho pola, vykresluje sa len ked su
        # v poliach data
        # todo - uprava pre polia obsahujuce velmi velky pocet poloziek,
        # spomaluje to vykreslovanie
        gc.setBrush(Qt.NoBrush)

        if len(self.data_x) > 1:
            for j in range(lines):
                if j < self.maxLines:
                    try:
                        # osetrenie zmeny dlzky pola pocas vykreslovania simulacnym threadom vynimkou
                        # iteracia po jednotlivych stopach, vyber farby stopy
                        gc.setPen(QPen(self.colors[j % 4]))

                        # vykreslenie dat stopy
                        for i in range(1, len(self.data_x)):
                            xp = self.data_x[i] * cx
                            yp = self.y_size / 2 - \
                                (self.data_y[j][i] - dy) * cy
                            gc.drawPoint(int(xp), int(yp))

                    except:
                        # vynimka pri zmene dlzky pola pri upgrade jeho dlzky
                        pass

    def sim(self, flag, value, time, step):
        '''Vykreslenie casoveho zaznamu'''
        #step = 0.1

        ymax = self.parameter['Y-Max'].value
        ymin = self.parameter['Y-Min'].value

        if flag == SIM_INIT or flag == SIM_RESET: 	# re / inicializaci dat
            self.data_x = []
            self.data_y = []
            for i in range(self.maxLines):
                self.data_y.append([])

        elif flag == SIM_UPDATE:

            value = self.terminal[1].value

            self.data_x.append(time)
            if type(value) == ndarray:
                for i in range(len(value)):
                    if i < self.maxLines:
                        dataVal = value[i]
                        if value[i] >= ymax:
                            dataVal = ymax
                        if value[i] <= ymin:
                            dataVal = ymin
                        self.data_y[i].append(dataVal)
            else:
                dataVal = value
                if value >= ymax:
                    dataVal = ymax
                if value <= ymin:
                    dataVal = ymin
                self.data_y[0].append(dataVal)
