# -*- coding: utf-8 -*-
from numpy import arange, sin, ndarray

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT, SIM_RESET, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Plot_XY(Component):

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.maxLines = 8	     # maximalny pocet zobrazenych grafov
        self.numTraces = 1      # aktualny pocet zobrazovanych stop (dlzka vstupnych dat)

        self.x_size = 240
        self.y_size = 180

        self.data_x = []		# datove polia
        self.data_y = []

        for i in range(self.maxLines):
            self.data_y.append([])

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-5, -5, self.x_size + 10, self.y_size + 10)
        self.shapeColor = Color.blue

        TERM.y = self.addTerminal('IN_Y', 1, TERM.IN, QPointF(-10, 60), TERM.DIR_EAST, TERM.IN_ARROW_FILL, TERM.IN_ARROW)
        TERM.y.termDiscColor = Color.black       # farby pre vstup - vektor
        TERM.y.termDiscFill = Color.white
        TERM.y.termConnColor = Color.black
        TERM.y.termConnFill = Color.black

        TERM.x = self.addTerminal('IN_X', 2, TERM.IN, QPointF(-10, 120), TERM.DIR_EAST, TERM.IN_ARROW_FILL, TERM.IN_ARROW)
        TERM.x.termDiscColor = Color.black       # farby pre vstup - vektor
        TERM.x.termDiscFill = Color.white
        TERM.x.termConnColor = Color.black
        TERM.x.termConnFill = Color.black

        self.addParameter('Y-Max', 5.0)
        self.addParameter('Y-Min', -5.0)
        self.addParameter('X-Max', 5.0)
        self.addParameter('X-Min', -5.0)

        self.colors = [Color.blue, Color.red, Color.green, Color.black]

        # demo data
        self.data_y.append([])
        self.data_x.append([])
        q = arange(0, 10, 0.1)
        self.data_y[0] = 3 * sin(3 * q)
        self.data_x[0] = 3 * sin(2 * q)

    def updateShape(self):
        # zmazanie demo-dat, ak doslo k zmene mierky grafu
        # po nacitani parametrov objektu zo suboru
        if(self.parameter['Y-Max'].value != 5.0 or
                self.parameter['Y-Min'].value != -5.0 or
                self.parameter['X-Max'].value != 5.0 or
                self.parameter['X-Min'].value != -5.0):
            self.data_x = []
            self.data_y = []

    def drawShape(self, gc):

        grad = QLinearGradient(0, -5, 0, 180)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.greenYellow)
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

        # TODO - kontrola nastavenie rozsahov (max > min)
        ymax = self.parameter['Y-Max'].value
        ymin = self.parameter['Y-Min'].value
        xmax = self.parameter['X-Max'].value
        xmin = self.parameter['X-Min'].value

        cy = self.y_size / (ymax - ymin)
        dy = (ymax + ymin) / 2.0

        cx = self.x_size / (xmax - xmin)
        dx = (xmax + xmin) / 2.0

        lines = 1
        if (type(self.terminal[1].value) == ndarray) or (type(self.terminal[1].value) == list):
            lines = len(self.terminal[1].value)

        # kontrola na dlzku datoveho pola, vykresluje sa len ked su
        # v poliach data
        # todo - uprava pre polia obsahujuce velmi velky pocet poloziek,
        # spomaluje to vykreslovanie
        gc.setBrush(Qt.NoBrush)

        # ziadne data, prazdny vektor
        if len(self.data_x) == 0:
            return

        if len(self.data_x[0]) > 1:
            for j in range(lines):
                if j < self.maxLines:
                    try:
                        # osetrenie zmeny dlzky pola pocas vykreslovania simulacnym threadom vynimkou
                        # iteracia po jednotlivych stopach, vyber farby stopy
                        gc.setPen(QPen(self.colors[j % 4]))
                        path = QPainterPath()

                        path.moveTo(
                            self.x_size / 2 + (self.data_x[j][0] - dx) * cx,
                            self.y_size / 2 - (self.data_y[j][0] - dy) * cy)
                        # vykreslenie dat stopy
                        for i in range(1, len(self.data_x[0])):
                            xp = self.x_size / 2 + (self.data_x[j][i] - dx) * cx
                            yp = self.y_size / 2 - (self.data_y[j][i] - dy) * cy
                            path.lineTo(xp, yp)

                        gc.drawPath(path)
                    except:
                        print('volajaka chyba')
                        # vynimka pri zmene dlzky pola pri upgrade jeho dlzky
                        pass

    def sim(self, flag, value, time, step):
        ymax = self.parameter['Y-Max'].value
        ymin = self.parameter['Y-Min'].value

        xmax = self.parameter['X-Max'].value
        xmin = self.parameter['X-Min'].value

        if flag == SIM_INIT or flag == SIM_RESET: 	# re / inicializaci dat
            self.data_x = []
            self.data_y = []
            for i in range(self.maxLines):
                self.data_x.append([])
                self.data_y.append([])
            # self.timeRestart=time

        elif flag == SIM_UPDATE:

            value_y = self.terminal[1].value
            value_x = self.terminal[2].value

            # TODO - kontrola na sirku vektora X a Y vstupu

            # zaradenie dat z y-vstupu
            if (type(value_y) == ndarray) or (type(value_y) == list):
                for i in range(len(value_y)):
                    if i < self.maxLines:
                        dataVal = value_y[i]
                        if value_y[i] >= ymax:
                            dataVal = ymax
                        if value_y[i] <= ymin:
                            dataVal = ymin
                        self.data_y[i].append(dataVal)
            else:
                dataVal = value_y
                if value_y >= ymax:
                    dataVal = ymax
                if value_y <= ymin:
                    dataVal = ymin
                self.data_y[0].append(dataVal)

            # zaradenie dat z x-vstupu
            if (type(value_x) == ndarray) or (type(value_x) == list):
                for i in range(len(value_x)):
                    if i < self.maxLines:
                        dataVal = value_x[i]
                        if value_x[i] >= xmax:
                            dataVal = xmax
                        if value_x[i] <= xmin:
                            dataVal = xmin
                        self.data_x[i].append(dataVal)
            else:
                dataVal = value_x
                if value_x >= xmax:
                    dataVal = xmax
                if value_x <= xmin:
                    dataVal = xmin
                self.data_x[0].append(dataVal)
