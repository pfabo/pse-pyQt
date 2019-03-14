# -*- coding: utf-8 -*-
from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTROL
from lib.pseqt import *  # @UnusedWildImport
from sim import SIM_SOLVER_RT2


class Solver_RT2(Component):

    '''
    Simulation Control - Real time, fixed step RK2 Solver

    Ikona pre solver RK2 synchronizovany na realny cas.
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTROL
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black
        self.solver = SIM_SOLVER_RT2

        self.engine = None    # referencia na simulator, inicializuje sa na zaciatku simulacie
                              # v SimulatorEngine:startSimulation, umoznuje modifikaciu parametrov simulacie pocas behu

        self.addParameter('Step', 0.1, visibleName=True)
        self.addParameter('Stop Time', 10, visibleName=True)

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.cyan)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        font = QFont('Decorative', 12)
        font.setItalic(True)
        gc.setFont(font)
        gc.setPen(QPen(Color.blue, 1))
        gc.drawText(self.box, Qt.AlignCenter, 'RT2')
