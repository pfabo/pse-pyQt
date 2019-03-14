# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

from numpy import array

from color import Color
from component import Component
from componenttypes import SIM_INIT, TYPE_SIM_DISCRETE, SIM_STEP, SIM_FINISH
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM

import time as tm
import numpy as np
import serial


class AR_Control(Component):
    '''
    @if English

    @endif

    @if Slovak

    @todo - spatna kontrola nastavenych parametrov
    @todo - kontrola komunikacneho portu

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.shapeImage = 'aor.svg'
        self.box = QRectF(-40, -60, 80, 120)
        self.shapeColor = Color.firebrick

        self.addTerminal('ANT', 2, TERM.IN, QPointF(-40, -30), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('FREQ', 3, TERM.IN, QPointF(-40, 30), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('DATA', 1, TERM.OUT, QPointF(40, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('Port', '\dev\ttyUSB0', visibleName=True)
        self.port = None
        self.state = False    # indikator prechodu cez inicializaciu, v prvom kroku simulacie sa inicializuje prijimac

    def drawShape(self, gc):

        grad = QLinearGradient(0, -40, 0, 80)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.yellowGreen)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-35, -55, 70, 110, 5, 5)

        font = QFont('Decorative', 10)
        font.setItalic(True)
        gc.setFont(font)
        gc.setPen(QPen(Color.red, 1))
        gc.drawText(QRectF(-35, -45, 70, 20), Qt.AlignCenter, 'AOR')
        gc.drawText(QRectF(-35, -30, 70, 20), Qt.AlignCenter, 'AR 5001')

        self.shapeSvg.render(gc, targetOffset=QPoint(-30, -10))

    def sim(self, flag, value, time, step):
        if flag == SIM_INIT:
            if self.state is False:
                self.port = serial.Serial('/dev/ttyUSB0', 115200,
                                          parity=serial.PARITY_NONE,
                                          stopbits=1, timeout=0.05)
                self.port.flushInput()
                self.port.flushOutput()
                self.state = True

        elif flag == SIM_STEP:
            if self.state is True:
                self.state = False
                # v prvom kroku nastavenie prijimaca
                # 1. inicializacia anteny
                for cmd in self.terminal[2].value:
                    self.port.write(cmd)
                    tm.sleep(0.1)

                # 2. inicializacia frekvencii
                freq = self.terminal[3].value
                if type(freq) == np.ndarray:
                    cf = int(freq[0] * 1e6)   # center frequency
                    cmd = bytes('CF' + str(cf) + '\r', encoding='ascii')
                    self.port.write(cmd)
                    tm.sleep(0.1)

                    fp = int(freq[1] * 1e6)   # span frequency
                    cmd = bytes('FP' + str(fp) + '\r', encoding='ascii')
                    self.port.write(cmd)
                    tm.sleep(0.1)

                self.port.flushInput()
                self.port.flushOutput()

            # nacitanie hodnot spektralneho analyzatora
            self.port.write(b'FD\r')
            # format odpovede
            # FD <sp> \r \n bbb... 160x ...bbb \r \n
            q = self.port.read(168)

            u = q[5:166]
            w = u.decode('ascii')
            data = []
            for i in range(160):
                data.append((ord(w[i]) - 32.0))  # 100.0)
            self.terminal[1].value = array(data)

        elif flag == SIM_FINISH:
            self.port.write(b'EX\r')
            self.port.flushInput()
            self.port.flushOutput()
