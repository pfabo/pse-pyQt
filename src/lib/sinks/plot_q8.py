# -*- coding: utf-8 -*-
from numpy import arange, zeros, ndarray

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS, SIM_INIT, SIM_RESET, SIM_UPDATE
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class Plot_Q8(Component):

    '''
    Digitalny zaznamnik pre 4 stopy. Polozky vstupneho vektor nad rozsah
    zaznamnika su ignorovane, pri mensom pocte su zobrazovane ako False.

    Scope Mode - umoznuje prekreslenie grafu po prekroceni jeho casoveho
    rozsahu od zaciatku


    TODO - vykreslenie mierky grafu (casovy rozsahu osi X-osi, vzorkovanie)
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.maxLines = 8		# maximalny pocet zobrazenych grafov
        self.x_size = 240
        self.y_size = 180

        self.data_x = []		# datove polia
        self.data_y = []

        for i in range(self.maxLines):
            self.data_y.append([])

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-5, -5, self.x_size + 10, self.y_size + 10)
        self.shapeColor = Color.blue
        self.colors = [Color.blue, Color.red, Color.green, Color.black]

        self.timeOffset = 0		# offset pre refresh stopy v scope mode

        term_in = self.addTerminal('IN', 1, TERM.IN, QPointF(-10, 90), TERM.DIR_EAST, TERM.IN_ARROW_FILL, TERM.IN_ARROW)
        term_in.termDiscColor = Color.black  # farby pre vstup - vektor
        term_in.termDiscFill = Color.white
        term_in.termConnColor = Color.black
        term_in.termConnFill = Color.black

        self.addParameter('X-Base', 10.0)
        self.addParameter('Scope', 1)

        # inicializacia - vykreslenie stop
        self.data_x = arange(0, 10, 0.1)
        for q in range(self.maxLines):
            self.data_y[q] = zeros(len(self.data_x))

    def updateShape(self):
        # zmazanie demo-dat, ak doslo k zmene mierky grafu
        # po nacitani parametrov objektu zo suboru
        if self.parameter['X-Base'].value != 10:
            self.data_x = []
            self.data_y = []

    def drawShape(self, gc):

        grad = QLinearGradient(0, -5, 0, 280)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.yellow)
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

        for j in range(self.maxLines):
            path = QPainterPath()
            path.moveTo(0, self.y_size - 5 - j * 22.5)
            path.lineTo(self.x_size, self.y_size - 5 - j * 22.5)
            gc.drawPath(path)

        # skalovanie x-ovej osi grafu
        maxTime = self.parameter['X-Base'].value
        cx = self.x_size / maxTime

        # kontrola na dlzku datoveho pola, vykresluje sa len ked su
        # v poliach data
        # TODO - uprava pre polia obsahujuce velmi velky pocet poloziek,
        # spomaluje to vykreslovanie - vynechanie / preskocenie zvoleneho poctu bodov
        # tak, aby zostalo zachovane rozlisenie 1px/bod
        gc.setBrush(Qt.NoBrush)

        for j in range(self.maxLines):
            try:
            # osetrenie zmeny dlzky pola pocas vykreslovania simulacnym threadom vynimkou
            # iteracia po jednotlivych stopach, vyber farby stopy
                gc.setPen(QPen(self.colors[j % 4]))
                path = QPainterPath()

                path.moveTo(0, self.y_size - 5 - j * 22.5 - self.data_y[j][0] * 20)
                # vykreslenie dat stopy
                for i in range(1, len(self.data_x)):
                    xp = self.data_x[i] * cx
                    yp = self.y_size - 5 - j * 22.5 - self.data_y[j][i] * 20
                    path.lineTo(xp, yp)

                gc.drawPath(path)
            except:
                # vynimka pri zmene dlzky pola pri upgrade jeho dlzky, nesedi rozmer
                # pola data_x a data_y
                pass

    def sim(self, flag, value, time, step):
        maxTime = self.parameter['X-Base'].value
        scopeMode = self.parameter['Scope'].value

        if flag == SIM_INIT or flag == SIM_RESET: 	# re / inicializaci dat
            self.data_x = []
            self.data_y = []
            for i in range(self.maxLines):
                self.data_y.append([])

            self.timeOffset = 0

        elif flag == SIM_UPDATE:
            # kontrola na prekrocenie casoveho rozsahu grafu
            # v pripade scopeMode==1 sa graf prekresluje od zaciatku s casovym
            # posunom
            if time >= (maxTime + self.timeOffset):
                if scopeMode == 0:
                    return
                else:
                    # scope mode - vynulovanie poli, nastavenie noveho offsetu
                    self.data_x = []
                    self.data_y = []
                    for i in range(self.maxLines):
                        self.data_y.append([])

                    self.timeOffset = time

            value = self.terminal[1].value
            self.data_x.append(time - self.timeOffset)

            temp = zeros(self.maxLines)		# docasny vektor hodnot

            if type(value) == ndarray or type(value) == list:
                for i in range(len(value)):
                    if i < self.maxLines:  # vektorova hodnota, osetrenie pretecenia
                        temp[i] = value[i]
            else:
                temp[0] = value				# skalarna hodnota - do stopy no.0

            for q in range(self.maxLines):  # komparator a zaradenie hodnot do poli stop
                if temp[q] >= 0.5:
                    self.data_y[q].append(1)
                else:
                    self.data_y[q].append(0)
