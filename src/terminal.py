# -*- coding: utf-8 -*-

import six

from color import Color


if six.PY2:
    from PyQt4.QtGui import *  # @UnusedWildImport
    from PyQt4.QtCore import *  # @UnusedWildImport
else:
    from PyQt5.QtWidgets import *  # @UnusedWildImport
    from PyQt5.QtGui import *  # @UnusedWildImport
    from PyQt5.QtCore import *  # @UnusedWildImport


class TERM:
    # typ terminalu
    CONN = 1  # prepojovaci terminal sieti
    IN = 2  # vstupny terminal
    OUT = 4  # vystupny teminal
    INOUT = 8  # obojsmerny terminal

    # orientacia
    DIR_NORTH = 16
    DIR_SOUTH = 32
    DIR_WEST = 64
    DIR_EAST = 128

    # zobrazenia terminalu
    NONE = 5000
    CROSS = 5001
    CIRCLE = 5002
    CIRCLE_FILL = 5004
    SQUARE = 5003
    SQUARE_FILL = 5005
    IN_ARROW = 5010
    IN_ARROW_FILL = 5011
    OUT_ARROW = 5020
    OUT_ARROW_FILL = 5021
    IN_ARROW_SMALL = 5030  # small arrow
    IN_ARROW_SMALL_FILL = 5031
    OUT_ARROW_SMALL = 5040  # small arrow
    OUT_ARROW_SMALL_FILL = 5041


class TEXT:
    # umiestnenie a zarovnanie textu terminalu (meno, cislo) vzhladom k jeho polohe
    LEFT = 1
    RIGHT = 4
    TOP = 8
    DOWN = 16
    CENTER = 32


class VirtualTerminal():
    '''!
    @if English


    @endif

    @if Slovak

    Struktura reprezentujuca terminal pre virtualne komponenty.

    @endif
    '''

    def __init__(self, name, component, num, termtype):
        '''
        @param component:	referencia na komponent obsahujuci terminal
        @param name: meno terminalu
        @param num:  cislo terminalu
        '''

        self.comp = component		# referencia na rodicovsky komponent
        self.termType = termtype		# typ terminalu
        self.name = name			# meno terminalu
        self.num = num			# cislo terminalu
        self.value = 0.0			# vstupna/vystupna hodnota terminalu
        self.connect = []			# zoznam pripojenych prepojeni k terminalu


class Terminal():
    '''!
    @if English

    @endif

    @if Slovak


    @endif
    '''

    def __init__(self, component, name='', num=1, termtype=TERM.IN,
                 position=QPoint(0, 0), direction=0, parent=None):
        '''!
        @param component:	referencia na komponent obsahujuci terminal
        @param name: meno terminalu
        @param num:  cislo terminalu
        @position:   poloha terminalu vzhladom na komponent
        @direction:  orientacia terminalu
        '''

        self.comp = component
        self.value = 0.0                    # vstupna/vystupna hodnota terminalu
        self.connect = []		        # zoznam pripojenych prepojeni k terminalu

        # zakladne parametre terminalu
        self.termType = termtype	        # typ terminalu
        self.name = name		        # meno terminalu
        self.num = num		        # cislo terminalu

        # geometria terminalu
        self.width = 1		        # sirka pripojenia
        self.length = 0		        # dlzka pripoju terminalu
        self.position = position	        # relativna poloha vzhladom k originu
        self.posNum = QPoint(-3, 3)         # relativna poloha cisla terminalu
        self.posName = QPoint(-3, -12)      # relativna poloha mena

        # zobrazenie terminalu
        self.direction = direction	         # orientacia pripoju terminalu
        self.termNumberShow = False          # priznak zobrazenia cisla terminalu
        self.termNameShow = False            # priznak zobrazenia mena terminalu

        self.termDiscType = TERM.SQUARE  # zobrazenie rozpojeneho terminalu
        self.termDiscSize = 5

        self.termConnType = TERM.NONE  # zobrazenie pripojeneho terminalu
        self.termConnSize = 5

        # nastavenie texty a farieb
        self.termColor = Color.black		# farba teminalu (ciara-pripojenie)
        self.termNumberColor = Color.red     # farba cisla terminalu
        self.termNumberSize = 10             # velkost fontu pre zobrazenie cisla
        self.termNumberAlign = TEXT.LEFT

        self.termNameColor = Color.black     # farba mena terminalu
        self.termNameSize = 10               # velkost fontu pre zobrazenie mena
        self.termNameAlign = TEXT.LEFT

        self.termDiscColor = Color.blue      # farba rozpojeneho terminalu
        self.termDiscFill = Color.white      # farba vyplne rozp. terminalu
        self.termConnColor = Color.blue     # farba pripojeneho terminalu
        self.termConnFill = Color.blue       # farba vyplne pripojeneho terminalu

    #def getPosition(self):
    #    return self.position

    def __str__(self):
        '''
        '''
        s = '\n'
        s = s + '<T> Term. name :' + str(self.name) + '\n'
        s = s + '          comp :' + str(self.comp.parameter['Ref'].value) + '\n'
        s = s + '          num  :' + str(self.num) + '\n'
        s = s + '          type :' + str(self.termType) + '\n'
        return s

    def drawTerminal(self, gc):
        '''
        @if English

        @endif

        @if Slovak

        Vykreslenie tvaru terminalu. Tvar je urceny prednastavenymi parametrami
        a aktualnym stavom terminalu (pripojeny/odpojeny).

        @endif
        '''
        # nacitanie parametrov terminalu
        x = self.position.x()
        y = self.position.y()

        length = self.length
        orient = self.direction

        #===============================================================
        # vyber parametrov zobrazenia terminalu podla toho, ci je
        # terminal pripojeny
        #---------------------------------------------------------------
        # vykreslenie odpojeneho terminalu
        if self.connect == []:
            gc.setPen(QPen(self.termDiscColor))
            gc.setBrush(QBrush(self.termDiscFill))
            r = self.termDiscSize
            termType = self.termDiscType

        # k terminalu je propojeny aspon jeden net
        else:
            gc.setPen(QPen(self.termConnColor))
            gc.setBrush(QBrush(self.termConnFill))
            r = self.termConnSize
            termType = self.termConnType

        #===============================================================
        # vykreslenie tvaru terminalu podla jeho  typu
        path = QPainterPath()

        if termType == TERM.CROSS:
            path.moveTo(x - r - 1, y - r - 1)
            path.lineTo(x + r, y + r)
            path.moveTo(x - r - 1, y + r + 1)
            path.lineTo(x + r, y - r)

        elif termType == TERM.CIRCLE:
            gc.setBrush(QBrush(Qt.NoBrush))
            path.addEllipse(x - r, y - r, 2 * r, 2 * r)

        elif termType == TERM.CIRCLE_FILL:
            path.addEllipse(x - r, y - r, 2 * r, 2 * r)

        elif termType == TERM.SQUARE:
            gc.setBrush(QBrush(Qt.NoBrush))
            path.addRect(x - r, y - r, r + r, r + r)

        elif termType == TERM.SQUARE_FILL:
            path.addRect(x - r, y - r, r + r, r + r)

        #======================================================================
        # VELKE SIPKY
        #======================================================================

        #---------------------------------------------------------------
        # TERMINAL INPUT ARROW  -  prazdna velka sipka vstupna
        #---------------------------------------------------------------
        elif termType == TERM.IN_ARROW:
            gc.setBrush(QBrush(Qt.NoBrush))
            if orient == TERM.DIR_EAST:
                path.moveTo(x, y)
                path.lineTo(x, y - r)
                path.lineTo(x + r + r, y)
                path.lineTo(x, y + r)
                path.lineTo(x, y)

            elif orient == TERM.DIR_SOUTH:
                path.moveTo(x, y)
                path.lineTo(x - r, y)
                path.lineTo(
                    x, y + r + r)
                path.lineTo(x + r, y)
                path.lineTo(x, y)

            elif orient == TERM.DIR_WEST:
                path.moveTo(x, y)
                path.lineTo(x, y - r)
                path.lineTo(
                    x - r - r, y)
                path.lineTo(x, y + r)
                path.lineTo(x, y)

            elif orient == TERM.DIR_NORTH:
                path.moveTo(x, y)
                path.lineTo(x - r, y)
                path.lineTo(
                    x, y - r - r)
                path.lineTo(x + r, y)
                path.lineTo(x, y)

        #---------------------------------------------------------------
        # TERMINAL OUTPUT ARROW  -  prazdna velka sipka vystupna
        #---------------------------------------------------------------
        elif termType == TERM.OUT_ARROW:
            gc.setBrush(QBrush(Qt.NoBrush))
            if orient == TERM.DIR_EAST:
                path.moveTo(x - r - r, y - r)
                path.lineTo(
                    x, y)
                path.lineTo(x - r - r, y + r)
                path.lineTo(x - r - r, y - r)
            elif orient == TERM.DIR_SOUTH:
                path.moveTo(x - r, y - r - r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r, y - r - r)
                path.lineTo(x - r, y - r - r)
            elif orient == TERM.DIR_WEST:
                path.moveTo(x + r + r, y - r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r + r, y + r)
                path.lineTo(x + r + r, y - r)
            elif orient == TERM.DIR_NORTH:
                path.moveTo(x - r, y + r + r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r, y + r + r)
                path.lineTo(x - r, y + r + r)

        #---------------------------------------------------------------
        # TERMINAL INPUT ARROW FILL - plna velka sipka vstupna
        #---------------------------------------------------------------
        elif termType == TERM.IN_ARROW_FILL:
            if orient == TERM.DIR_EAST:
                path.moveTo(x, y)
                path.lineTo(x, y - r)
                path.lineTo(
                    x + r + r, y)
                path.lineTo(x, y + r)
                path.lineTo(x, y)

            elif orient == TERM.DIR_SOUTH:
                path.moveTo(x, y)
                path.lineTo(x - r, y)
                path.lineTo(
                    x, y + r + r)
                path.lineTo(x + r, y)
                path.lineTo(x, y)

            elif orient == TERM.DIR_WEST:
                path.moveTo(x, y)
                path.lineTo(x, y - r)
                path.lineTo(
                    x - r - r, y)
                path.lineTo(x, y + r)
                path.lineTo(x, y)

            elif orient == TERM.DIR_NORTH:
                path.moveTo(x, y)
                path.lineTo(x - r, y)
                path.lineTo(
                    x, y - r - r)
                path.lineTo(x + r, y)
                path.lineTo(x, y)

        #---------------------------------------------------------------
        # TERMINAL OUTPUT ARROW FILL - plna velka sipka vstupna
        #---------------------------------------------------------------
        elif termType == TERM.OUT_ARROW_FILL:
            if orient == TERM.DIR_EAST:
                path.moveTo(x - r - r, y - r)
                path.lineTo(
                    x, y)
                path.lineTo(x - r - r, y + r)
                path.lineTo(x - r - r, y - r)

            elif orient == TERM.DIR_SOUTH:
                path.moveTo(x - r, y - r - r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r, y - r - r)
                path.lineTo(x - r, y - r - r)

            elif orient == TERM.DIR_WEST:
                path.moveTo(x + r + r, y - r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r + r, y + r)
                path.lineTo(x + r + r, y - r)

            elif orient == TERM.DIR_NORTH:
                path.moveTo(x - r, y + r + r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r, y + r + r)
                path.lineTo(x - r, y + r + r)

        #======================================================================
        # MALE SIPKY
        #======================================================================
        #---------------------------------------------------------------
        # TERMINAL INPUT SMALL ARROW  -  prazdna mala sipka vstupna
        #---------------------------------------------------------------
        elif termType == TERM.IN_ARROW_SMALL:
            gc.setBrush(QBrush(Qt.NoBrush))
            if orient == TERM.DIR_EAST:
                path.moveTo(x, y)
                path.lineTo(x, y - r)
                path.lineTo(
                    x + r, y)
                path.lineTo(x, y + r)
                path.lineTo(x, y)

            elif orient == TERM.DIR_SOUTH:
                path.moveTo(x, y)
                path.lineTo(x - r, y)
                path.lineTo(
                    x, y + r)
                path.lineTo(x + r, y)
                path.lineTo(x, y)

            elif orient == TERM.DIR_WEST:
                path.moveTo(x, y)
                path.lineTo(x, y - r)
                path.lineTo(
                    x - r, y)
                path.lineTo(x, y + r)
                path.lineTo(x, y)

            elif orient == TERM.DIR_NORTH:
                path.moveTo(x, y)
                path.lineTo(x - r, y)
                path.lineTo(
                    x, y - r)
                path.lineTo(x + r, y)
                path.lineTo(x, y)

        #---------------------------------------------------------------
        # TERMINAL OUTPUT SMALL ARROW  -  prazdna mala sipka vystupna
        #---------------------------------------------------------------
        elif termType == TERM.OUT_ARROW_SMALL:
            gc.setBrush(QBrush(Qt.NoBrush))
            if orient == TERM.DIR_EAST:
                path.moveTo(x - r, y - r)
                path.lineTo(
                    x, y)
                path.lineTo(x - r, y + r)
                path.lineTo(x - r, y - r)

            elif orient == TERM.DIR_SOUTH:
                path.moveTo(x - r, y - r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r, y - r)
                path.lineTo(x - r, y - r)

            elif orient == TERM.DIR_WEST:
                path.moveTo(x + r, y - r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r, y + r)
                path.lineTo(x + r, y - r)

            elif orient == TERM.DIR_NORTH:
                path.moveTo(x - r, y + r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r, y + r)
                path.lineTo(x - r, y + r)

        #---------------------------------------------------------------
        # TERMINAL INPUT SMALL ARROW FILL - plna mala sipka vstupna
        #---------------------------------------------------------------
        elif termType == TERM.IN_ARROW_SMALL_FILL:
            if orient == TERM.DIR_EAST:
                path.moveTo(x, y)
                path.lineTo(x, y - r)
                path.lineTo(
                    x + r, y)
                path.lineTo(x, y + r)
                path.lineTo(x, y)

            elif orient == TERM.DIR_SOUTH:
                path.moveTo(x, y)
                path.lineTo(x - r, y)
                path.lineTo(
                    x, y + r)
                path.lineTo(x + r, y)
                path.lineTo(x, y)

            elif orient == TERM.DIR_WEST:
                path.moveTo(x, y)
                path.lineTo(x, y - r)
                path.lineTo(
                    x - r, y)
                path.lineTo(x, y + r)
                path.lineTo(x, y)

            elif orient == TERM.DIR_NORTH:
                path.moveTo(x, y)
                path.lineTo(x - r, y)
                path.lineTo(
                    x, y - r)
                path.lineTo(x + r, y)
                path.lineTo(x, y)

        #---------------------------------------------------------------
        # TERMINAL OUTPUT SMALL ARROW FILL - mala velka sipka vstupna
        #---------------------------------------------------------------
        elif termType == TERM.OUT_ARROW_SMALL_FILL:
            if orient == TERM.DIR_EAST:
                path.moveTo(x - r, y - r)
                path.lineTo(
                    x, y)
                path.lineTo(x - r, y + r)
                path.lineTo(x - r, y - r)

            elif orient == TERM.DIR_SOUTH:
                path.moveTo(x - r, y - r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r, y - r)
                path.lineTo(x - r, y - r)

            elif orient == TERM.DIR_WEST:
                path.moveTo(x + r, y - r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r, y + r)
                path.lineTo(x + r, y - r)

            elif orient == TERM.DIR_NORTH:
                path.moveTo(x - r, y + r)
                path.lineTo(
                    x, y)
                path.lineTo(x + r, y + r)
                path.lineTo(x - r, y + r)

        gc.drawPath(path)
        # pripojovaci vodic terminalu
        if self.length > 0:
            path = QPainterPath()
            gc.setPen(QPen(self.termColor))
            path.moveTo(x, y)
            if orient == TERM.DIR_NORTH:
                path.lineTo(x, y - length)
            elif orient == TERM.DIR_SOUTH:
                path.lineTo(x, y - length)
            elif orient == TERM.DIR_WEST:
                path.lineTo(x - length, y)
            elif orient == TERM.DIR_EAST:
                path.lineTo(x + length, y)

            gc.drawPath(path)

        if self.termNumberShow is True:        # zobrazenie cisla terminalu
            font = QFont('Decorative', self.termNumberSize)
            gc.setFont(font)
            gc.setPen(QPen(self.termNumberColor, 1))
            gc.drawText(self.position + QPointF(self.posNum), str(self.num))

        if self.termNameShow is True:         # zobrazenie mena terminalu
            font = QFont('Decorative', self.termNameSize)
            gc.setFont(font)
            gc.setPen(QPen(self.termNameColor, 1))

            # zarovnanie textu mena terminalu
            fm = QFontMetrics(font)    # urcenie rozmerov textu a centrovanie vzhladom
            tw = fm.width(self.name)	  # k zadanej polohe referencneho bodu
            # th = fm.height()
            if self.termNameAlign == TEXT.LEFT:
                gc.drawText(self.position + self.posName, str(self.name))
            if self.termNameAlign == TEXT.RIGHT:
                gc.drawText(self.position + self.posName - QPoint(tw, 0), str(self.name))
