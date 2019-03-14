# -*- coding: utf-8 -*-

from component import *
from terminal import *
from color import *
import serial
import time
import six


class TomcatBoard(Component):
    '''
    @if English

    Scratch board interface

    Output vector:

    [0]	"input D",
    [1]	"input C",
    [2]	"input B",
    [3]	"button",
    [4]	"input A",
    [5]	"light",
    [6]	"sound",
    [7]	"slider"

    @endif

    @if Slovak

    Trieda rozhrania pre kompatibilné zariadenia so Scratch-Board.

    Scratch-Board odpoveda na povel 0x01 polom o dlzke 18 bytov. Toto
    pole je konverotovane n vektor out, ktory je ulozeny do vystupneho
    terminalu.

    Položky výstupného vektora:

    [0]	"input D",
    [1]	"input C",
    [2]	"input B",
    [3]	"button",
    [4]	"input A",
    [5]	"light",
    [6]	"sound",
    [7]	"slider"

    @todo - osetrit pripad komunikacie s nespravnym FTDI zariadenim

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.shapeImage = 'tomcat_board.svg'
        self.compType = TYPE_SIM_DISCRETE
        self.shapeColor = Color.black
        self.shapeFillColor = Color.mediumAquamarine
        self.box = QRectF(-30, -30, 60, 60)

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        term = self.addTerminal('CLOCK', 2, TERM.IN, QPointF(0, -30), TERM.DIR_SOUTH, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        term.termDiscColor = Color.red
        term.termConnColor = Color.red
        term.termConnFill = Color.red

        self.addParameter('Port', '/dev/ttyUSB0', visibleName=True)
        self.addParameter('Raw data', 0, visibleName=True)

        self.port = None

    def drawShape(self, gc):

        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, self.shapeFillColor)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, tm, step):

        if flag == SIM_INIT:
            if self.port is None:
                try:
                    self.port = serial.Serial(self.parameter['Port'].value, 38400, parity=serial.PARITY_NONE, stopbits=2, timeout=0.1)
                except:
                    # chyba v pripojeni - neda sa otvorit komunikacny port
                    self.port = None
                    self.shapeFillColor = Color.red    # zmena farby - chybovy stav
                    print('>>> ERROR TomcatBoard - chyba pripojenia')

            if self.port is not None:
                # inicializacia buffrov serioveho rozhrania
                self.port.flushInput()
                self.port.flushOutput()
                self.shapeFillColor = Color.mediumAquamarine

        elif flag == SIM_STEP:
            if self.port is None:
                return

            # synchronizacia na clock
            if self.terminal[2].value >= 1:

                self.port.write(b'\x01')               # vyslanie / prijem spravy

                time.sleep(0.05)                       # casove oneskorenie 0.1 sec
                response = self.port.read(18)          # dlzka prijimanej spravy, prijme binarny retazec
                out = zeros(8)                         # spracovanie odpovede
                if len(response) == 18:
                    for i in range(9):
                        # rozlisenie podla verzie pythonu, verzia 3 pouziva byte array
                        if six.PY2 is True:
                            hd = ord(response[2 * i])
                            ld = ord(response[2 * i + 1])
                        else:
                            hd = (response[2 * i])
                            ld = (response[2 * i + 1])

                        channel = (hd & 0x78) / 8
                        data = (hd & 0x07) * 128 + (ld & 0x7F)

                        if channel < 8:
                            out[channel] = data

                    # linearizacia a uprava charakterisitk senzorov
                    # [3] button
                    out[3] = 1 - out[3] / 1023

                    # [7] slider
                    out[7] = (int)((1 - out[7] / 1023.0) * 100)

                    # sound
                    out[6] = out[6] / 1023.0 * 100

                    # light
                    out[5] = (1 - out[5] / 1023.0) * 100

                    self.terminal[1].value = out

        elif flag == SIM_FINISH:
            if self.port is not None:
                self.port.flushInput()
                self.port.flushOutput()
                self.port.close()
                self.port = None
