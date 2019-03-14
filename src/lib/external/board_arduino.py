# -*- coding: utf-8 -*-

from component import *
from terminal import *
from color import *
import serial
import numpy
import struct

import time as tm


class ArduinoBoard(Component):
    '''
    @if English

    Communication interface for Arduino Pro Mini.

    @endif

    @if Slovak

    Komunikacne rozhranie pre Arduino Pro Mini.

    @todo - osetrit synchronizaciu komunikacie na zaciatku simulacie.

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.shapeImage = 'arduino_logo_02.svg'
        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.shapeFillColor = Color.mediumAquamarine
        self.box = QRectF(-40, -60, 80, 120)

        t1 = self.addTerminal('DI', 1, TERM.IN, QPointF(-40, -40), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t1.termNameShow = True
        t1.posName = QPoint(7, 5)

        t2 = self.addTerminal('P0', 2, TERM.IN, QPointF(-40, -20), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t2.termNameShow = True
        t2.posName = QPoint(7, 5)

        t3 = self.addTerminal('P1', 3, TERM.IN, QPointF(-40, 0), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t3.termNameShow = True
        t3.posName = QPoint(7, 5)

        t4 = self.addTerminal('S0', 4, TERM.IN, QPointF(-40, 20), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t4.termNameShow = True
        t4.posName = QPoint(7, 5)

        t5 = self.addTerminal('S1', 5, TERM.IN, QPointF(-40, 40), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        t5.termNameShow = True
        t5.posName = QPoint(7, 5)

        t10 = self.addTerminal('A0', 10, TERM.OUT, QPointF(40, -20), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        t10.termNameShow = True
        t10.termNameAlign = TEXT.RIGHT
        t10.posName = QPoint(-7, 5)

        t11 = self.addTerminal('A1', 11, TERM.OUT, QPointF(40, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        t11.termNameShow = True
        t11.termNameAlign = TEXT.RIGHT
        t11.posName = QPoint(-7, 5)

        t12 = self.addTerminal('D0', 12, TERM.OUT, QPointF(40, 20), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        t12.termNameShow = True
        t12.termNameAlign = TEXT.RIGHT
        t12.posName = QPoint(-7, 5)

        term = self.addTerminal('CLOCK', 100, TERM.IN, QPointF(0, -60), TERM.DIR_SOUTH, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        term.termDiscColor = Color.red
        term.termConnColor = Color.red
        term.termConnFill = Color.red

        self.addParameter('Port', '/dev/ttyUSB0', visibleName=True)

        self.port = None    # komunikacny port
        self.addr = 0x55    # adresa + zahlavie paketu

    def drawShape(self, gc):

        grad = QLinearGradient(0, -55, 0, 110)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, self.shapeFillColor)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-35, -55, 70, 110, 5, 5)

        size = self.shapeSvg.sizeHint()
        size.scale(60, 60, Qt.KeepAspectRatio)
        self.shapeSvg.setMaximumSize(size)

        self.drawIcon(gc, -30, -30)

    def sim(self, flag, value, time, step):

        p = [self.addr, 0, 0, 0, 0, 0, 0, 0]

        if flag == SIM_INIT:

            # zatvorenie existujuceho otvoreneho komunikacneho portu
            if self.port is not None:
                self.port.close()
                self.port = None

            if self.port is None:
                try:
                    # self.port.close()
                    self.port = serial.Serial(self.parameter['Port'].value, 230400, parity=serial.PARITY_NONE, stopbits=2, timeout=0.1)
                    # inicializacia bufferov serioveho rozhrania

                    self.shapeFillColor = Color.mediumAquamarine

                    count = 0
                    while True:
                        self.port.flushInput()
                        self.port.flushOutput()

                        for dt in p:
                            self.port.write(struct.pack('B', dt))

                        tm.sleep(0.005)

                        try:
                            resp = self.port.read(6)
                            [addr, d0h, d0l, d1h, d1l, din] = struct.unpack('BBBBBB', resp)
                            if addr == self.addr:
                                break
                            count = count + 1

                            if count == 10:
                                print('chyba synchronizacie')
                                break
                        except:
                            pass

                except:
                    # chyba v pripojeni
                    self.port = None
                    self.shapeFillColor = Color.red    # zmena farby - chybovy stav

        elif flag == SIM_STEP:
            if self.port is None:
                return

            if self.terminal[100].value >= 1:
                # inicializacia buffrov - chyba v prenose moze sposobit rozpadnutie komunikacie
                self.port.flushInput()
                self.port.flushOutput()

                # 1. byte - adresa - header paketu
                #p = [self.addr, 0, 0, 0, 0, 0, 0, 0]

                # 2. byte - digitalny out port, hodnota moze byt vektor alebo skalar
                inp = self.terminal[1].value
                if (type(inp) == numpy.ndarray) or (type(inp) == list):
                    # hodnota je vektor
                    for i in range(len(inp)):
                        vectorLength = len(inp)
                        if vectorLength > 8:
                            vectorLength = 8
                        data = 0
                        for j in range(vectorLength):
                            data = data + ((int(inp[j]) & 0x01) << j)
                        p[1] = data
                else:
                    # hodnota vektoru je skalar
                    data = int(inp) & 0xFF
                    p[1] = data

                # 3. byte - PWM 0
                # osetrenie limitnych hodnot
                value = self.terminal[2].value

                if value > 255:
                    value = 255

                if value < 0:
                    value = 0

                p[2] = int(value)

                # 4. byte - PWM 1
                # osetrenie limitnych hodnot
                value = self.terminal[3].value

                if value > 255:
                    value = 255

                if value < 0:
                    value = 0

                p[3] = int(value)

                # 5., 6.  byte - servo 0
                inp = int(self.terminal[4].value)
                if inp < 500:
                    inp = 500

                if inp > 2200:
                    inp = 2200

                dh = (inp & 0xFF00) >> 8
                dl = inp & 0xFF
                p[4] = dh
                p[5] = dl

                # 7., 8.  byte - servo 1
                inp = int(self.terminal[5].value)
                if inp < 500:
                    inp = 500

                if inp > 2200:
                    inp = 2200

                dh = (inp & 0xFF00) >> 8
                dl = inp & 0xFF
                p[6] = dh
                p[7] = dl

                for dt in p:
                    self.port.write(struct.pack('B', dt))

                # tm.sleep(0.001)

                try:
                    resp = self.port.read(6)
                    [addr, d0h, d0l, d1h, d1l, din] = struct.unpack('BBBBBB', resp)
                    self.terminal[10].value = d0h * 256 + d0l
                    self.terminal[11].value = d1h * 256 + d1l
                    self.terminal[12].value = din
                except:
                    # chyba pri nacitani alebo dekodovani, inicializacii komunikacie
                    self.terminal[10].value = 0
                    self.terminal[11].value = 0
                    self.terminal[12].value = 0

        elif flag == SIM_FINISH:
            if self.port is not None:
                self.port.flushInput()
                self.port.flushOutput()
                self.port.close()
                self.port = None

            self.terminal[10].value = 0
            self.terminal[11].value = 0
            self.terminal[12].value = 0
