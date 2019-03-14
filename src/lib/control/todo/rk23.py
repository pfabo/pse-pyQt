# -*- coding: utf-8 -*-

from component import *
from terminal import *
from color import *
from sim import SIM_SOLVER_RK2


class Solver_RK23(Component):

    '''
    Simulation Control - Fixed step RK23 Solver
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTROL
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black
        self.solver = SIM_SOLVER_RK2

        self.engine = None    # referencia na simulator, inicializuje sa na zaciatku simulacie
                              # v SimulatorEngine:startSimulation, umoznuje modifikaciu parametrov simulacie pocas behu

        self.addParameter('Step', 0.005)
        self.addParameter('Stop Time', 10.0)

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
        gc.drawText(self.box, Qt.AlignCenter, 'RK23')
