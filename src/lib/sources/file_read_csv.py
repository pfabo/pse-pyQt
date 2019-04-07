# -*- coding: utf-8 -*-
from color import Color
from component import Component, PARAM
from componenttypes import TYPE_SIM_DISCRETE, SIM_INIT, SIM_STEP, SIM_FINISH
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM

# hodnoty pre definovanie stavu citania suboru
FILE_CLOSED = 0
FILE_OPENED = 1
FILE_READ = 2
FILE_ERROR = 10


class FileRead_CSV(Component):
    """!
    @if Slovak

    Komponent pre načítanie hodnôt zo súboru do výstupného terminálu.

    Komponent načíta numerické hodnoty z textového súboru, meno súboru je zadané
    parametrom <I>File</I>.
    Čítanie súboru je po riadkoch, v prípade viacerých hodnôt na riadku vytvorí vektor
    a priradí ho hodnote výstupného terminálu, pri jednej hodnote na riadku je výstupná
    hodnota skalár.

    Okamžik čítania je možné synchronizovať na externé hodiny cez voliteľný terminál <I>Clock</I>.

    @todo nastavenie typu delimiteru
    @todo nastavenie opakovania po dočítaní hodnôt na koniec súboru
    @todo v pripade chyby otvorenia alebo čítania súboru (zlý formát) zmeniť farbu objektu

    @endif

    @if English

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_DISCRETE
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeImage = 'file_write_csv.svg'
        self.shapeColor = Color.black

        self.fp = None              # referencia na otvoreny subor
        self.state = FILE_CLOSED    # stavova premenna - stav suboru

        self.addTerminal('OUT', 1, TERM.OUT, QPointF(30, 0), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)

        self.addParameter('File', '', paramType=PARAM.FILE_CSV)
        self.addParameter('Clock', 0)

    def updateShape(self):
        super(FileRead_CSV, self).updateShape()

        if self.parameter['Clock'].value == 1:  # TODO - uprava parametra na True/False
            if 2 in self.terminal:
                pass
            else:
                term = self.addTerminal('CLOCK', 2, TERM.IN, QPointF(20, -5), TERM.DIR_SOUTH, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
                term.termDiscColor = Color.red
                term.termConnColor = Color.red
                term.termConnFill = Color.red
        else:
            if 2 in self.terminal:
                if self.terminal[2].connect != []:
                    print('>>> WARNING ')
                    print('    FileRead_CSV : Remove clock terminal')
                    print('                   Clock terminal is connected !')
                    self.parameter['Clock'].value = 1  # True
                else:
                    del self.terminal[2]
            else:
                pass

    def drawShape(self, gc):

        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.green)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):
        ext = self.parameter['Clock'].value

        if flag == SIM_INIT:
            if self.state == FILE_CLOSED:
                try:
                    self.fp = open(self.parameter['File'].value, 'r')
                except:
                    print('>>> FileRead_CSV : Chyba pri otvarani suboru')
                    self.fp = None
                    return
                self.state = FILE_OPENED

                # v pripade aktivneho terminalu Clock je vystup inicializovany prvou hodnotou
                # zo suboru (po prvu zmenu terminalu Clock)
                if ext == 1:  # True:
                    self.setOutput()

        elif flag == SIM_STEP:
            # pri externom clocku je hodnota prevedena len v stave clock=1
            if ext == 1:  # True:
                if self.terminal[2].value < 1:
                    return

            self.setOutput()

        elif flag == SIM_FINISH:
            self.fp.close()
            self.state = FILE_CLOSED

    def setOutput(self):
        """!
        @if Slovak

        Pomocná funkcia pre nastavenie výstupu.

        Funcia načíta riadok zo súboru, parsuje ho podla delimitera, vytvorí a nastavi
        hodnotu výstupného terminálu.
        Po dočítaní na koniec súboru zostáva hodnota terminálu nezmenená.

        @endif
        """
        sr = self.fp.readline()

        # nacitanie konca suboru, hodnota terminalu zostava nezmenena
        if sr == '':
            return

        sd = sr.split(';')
        data = []
        for i in sd:
            data.append(float(i))
        if len(data) == 1:
            self.terminal[1].value = data[0]
        else:
            self.terminal[1].value = data
