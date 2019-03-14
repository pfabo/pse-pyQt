# -*- coding: utf-8 -*-
from numpy import array, ndarray

from color import Color
from component import Component
from componenttypes import TYPE_SIM_CONTINUOUS
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class BusCompressor(Component):
    """!
    @if English

    @endif

    @if Slovak

    Kompresor zbernice s variabilným počtom vstupov.

    Kompresor poskladá vstupné hodnotu do výstupného vektora. Počet vstupov je možné
    meniť vo vlastnostiach komponentu, zmena je povolená len pre komponent bez
    pripojených vstupov. Maximálny počet vstupov je 99.

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-10, -15, 20, 50)

        self.addParameter('Inputs', 2)
        term_out = self.addTerminal('OUT', 100, TERM.OUT, QPointF(10, 0), TERM.DIR_EAST, TERM.OUT_ARROW_FILL, TERM.OUT_ARROW)
        term_out.termDiscColor = Color.black       # farby pre vystup - vektor
        term_out.termDiscFill = Color.white
        term_out.termConnColor = Color.black
        term_out.termConnFill = Color.black

    def drawShape(self, gc):

        n = self.parameter['Inputs'].value

        if (n % 2) == 0:  # kontrola parne/neparne cislo
            y = (n // 2) * 20 - 10
        else:
            y = (n // 2) * 20

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        for j in range(-1, 2):
            path.moveTo(j, -y - 10)
            path.lineTo(j, y + 10)
        gc.drawPath(path)

        self.box = QRectF(-10, -y - 10, 20, 2 * y + 20)

    def updateShape(self):
        '''
        @todo - kontrola pripojenych terminalov, zmena poctu terminalo sa moze robit len v
               pripade, ak su vsetky terminaly odpojene. Uprava - je mozne zmenit pocet
               terminalov, treba
        @todo - povodne pripojene prepojit na rovnaky terminal
               - zvysne zakoncit Connection alebo vymazat ?
        '''
        n = self.parameter['Inputs'].value
        if n < 2:
            self.parameter['Inputs'].value = 2
            print ('>>> WARNING <<<')
            print ('    Component Mux: Number of inputs must be >=2')
            return
        else:
            t = self.terminal.keys()
            # kontrola pripojenych terminalov
            for k in t:
                if self.terminal[k].connect != []:
                    print ('>>> WARNING <<<')
                    print ('    Component Mux: Connected terminal(s) (docasne neimplementovane)')
                    return

            # zamazanie povodnych terminalov
            tempArr = []
            for k in t:
                if k != 100:
                    tempArr.append(k)
            for q in tempArr:
                del self.terminal[q]

            # generovanie noveho poctu terminalov
            y = 0
            if (n % 2) == 0:  # kontrola - parne/neparne cislo
                y = -(n // 2) * 20 + 10
            else:
                y = -(n // 2) * 20

            out = []
            for i in range(n):
                term_in = self.addTerminal('IN' + str(i + 1), (i + 1), TERM.IN, QPointF(-10, y), TERM.DIR_EAST, TERM.IN_ARROW_FILL, TERM.IN_ARROW)
                term_in.termDiscColor = Color.black
                term_in.termDiscFill = Color.white
                term_in.termConnColor = Color.black
                term_in.termConnFill = Color.black

                y = y + 20
                out.append(0.0)
            self.terminal[100].value = array(out)

    def sim(self, flag, value, time, step):

        term = list(self.terminal.keys())
        term.remove(100)

        out = []
        for k in range(self.parameter['Inputs'].value):
            value = self.terminal[k + 1].value
            out.append(value)
        self.terminal[100].value = array(out)


class BusExpander(Component):
    """!
    @if English

    @endif

    @if Slovak

    \brief <H3><B>Expandér zbernice</B></H3>

    Komponent rozloží vstupný vektor na jeho položky,
    ktorých hodnoty sú skopírované na samostatné výstupy.

    <B><I>Parametre komponentu</I></B>

    <I>Outputs</I>

    Parameter definuje počet výstupov, na ktorý je rozložený vstupný vektor. Ak je počet výstupov
    väčší ako veľkosť vstupného vektora, hodnota neaktívneho výstupu je nulová, ak je počet výstupov
    menší ako veľkosť vstupného vektora, do výstupov u kopírované položky zo od začiatku vetktora
    a ostatné sú ignorované.

    Počet výstupov je možné meniť len vtedy, ak nie je komponent pripojený.

    <B>Literatúra</B>

    <B>Príklady</B>

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.box = QRectF(-10, -15, 20, 50)

        term_in = self.addTerminal('IN', 100, TERM.IN, QPointF(-10, 0), TERM.DIR_EAST, TERM.IN_ARROW_FILL, TERM.IN_ARROW)
        term_in.termDiscColor = Color.black       # farby pre vstup- vektor
        term_in.termDiscFill = Color.white
        term_in.termConnColor = Color.black
        term_in.termConnFill = Color.black

        self.addParameter('Outputs', 2)

    def drawShape(self, gc):

        n = self.parameter['Outputs'].value

        if (n % 2) == 0:  # kontrola parne/neparne cislo
            y = (n // 2) * 20 - 10
        else:
            y = (n // 2) * 20

        path = QPainterPath()
        gc.setPen(QPen(self.shapeColor))

        for j in range(-1, 2):
            path.moveTo(j, -y - 10)
            path.lineTo(j, y + 10)

        gc.drawPath(path)

        self.box = QRectF(-10, -y - 10, 20, 2 * y + 20)

    def updateShape(self):
        '''
        ToDo - kontrola pripojenych terminalov, zmena poctu terminalov sa moze robit len v
               pripade, ak su vsetky terminaly odpojene. Uprava - je mozne zmenit pocet
               terminalov, treba
               - povodne pripojene prepojit na rovnaky terminal
               - zvysne zakoncit Connection
        '''
        n = self.parameter['Outputs'].value
        if n < 2:
            self.parameter['Outputs'].value = 2
            print ('>>> WARNING <<<')
            print ('    Component Mux: Number of outputs must be >=2')
            return
        else:
            t = self.terminal.keys()
            for k in t:
                if self.terminal[k].connect != []:
                    print ('>>> WARNING <<<')
                    print ('    Component Mux: Connected terminal(s) (docasne neimplementovane)')
                    return

            tempArr = []
            for k in t:
                if k != 100:
                    tempArr.append(k)
            for q in tempArr:
                del self.terminal[q]

            # generovanie noveho poctu terminalov
            y = 0
            if (n % 2) == 0:  # kontrola parne/neparne cislo
                y = -(n // 2) * 20 + 10
            else:
                y = -(n // 2) * 20

            for i in range(n):
                term_out = self.addTerminal('OUT' + str(i + 1), (i + 1), TERM.OUT, QPointF(10, y), TERM.DIR_EAST, TERM.OUT_ARROW_FILL, TERM.OUT_ARROW)
                term_out.termDiscColor = Color.black       # farby pre vystup - vektor
                term_out.termDiscFill = Color.white
                term_out.termConnColor = Color.black
                term_out.termConnFill = Color.black

                y = y + 20

            self.box = QRectF(-10, -y - 10, 20, 2 * y + 20)

    def sim(self, flag, value, time, step):

        n = self.parameter['Outputs'].value

        value = self.terminal[100].value  # nacitanie hodnoty vstupneho terminalu

        if (type(value) == ndarray) or (type(value) == list):
            q = len(value)			# dlzka vstupneho vektora
            w = min(q, n)			# minimum z poctu terminalov a vstupnych hodnot
            for i in range(w):		# iteracia po zozname terminalov
                self.terminal[i + 1].value = value[i]
        else:
            self.terminal[1].value = value    # zle pripojeny komponent,
                                              # skalarna velicina na vstupe
