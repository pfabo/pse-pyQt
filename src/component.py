# -*- coding: utf-8 -*-
from math import modf
import logging
import os
import sys

import six

from color import Color
from componenttypes import *  # @UnusedWildImport
from net import VirtualNet
from terminal import TERM, Terminal, VirtualTerminal


if six.PY2:
    from PyQt4.QtGui import *  # @UnusedWildImport
    from PyQt4.QtCore import *  # @UnusedWildImport
    from PyQt4.QtSvg import QSvgWidget  # @UnresolvedImport @UnusedImport
else:
    from PyQt5.QtSvg import QSvgWidget  # @UnusedImport
    from PyQt5.QtWidgets import *  # @UnusedWildImport
    from PyQt5.QtGui import *  # @UnusedWildImport
    from PyQt5.QtCore import *  # @UnusedWildImport

LOG = logging.getLogger(__name__)


# typy parametrov komponentu, urcuju vyber editora pre editovanie parametrov
class PARAM:
    NONE = 0  # nezadany typ parametra
    STRING = 1
    BOOL = 2
    BINARY = 3
    INT = 4
    FLOAT = 5
    COMPLEX = 6
    COLOR = 7
    LIST = 8

    FILE = 100
    FILE_PSE = 101
    FILE_CSV = 102
    FILE_PNG = 103
    FILE_SVG = 104
    IMAGE = 105
    FILE_CSV_SAVE = 106
    FILE_HDF5_SAVE = 107


class VirtualParameter():
    '''!
    @if English


    @endif

    @if Slovak

    Struktura reprezentujuca parametre komponentu.

    @endif
    '''

    def __init__(self, name, value):
        self.name = name			# meno parametra
        self.value = value			# hodnota parametra

    def setSelected(self, state):
        pass


class Parameter(QGraphicsItem):
    """!
    @if English

    Component parameter.

    @endif

    @if Slovak

    Trieda parametrov komponentu.

    Parameter je samostatny graficky objekt, sucast skupiny objektov. Obsahuje hodnotu, ktora urcuje
    vlastnosti komponentu, ku ktoremu parameter patri. Typ hodnoty urcuje typ parametra - standardne pri
    vytvarani paramtra, je mozne ho modifikovat premennou self.paramType.

    Premenna self.parent urcuje suradnicovu sustavu, voci ktorej je paremeter umiestneny na ploche editora.

    @endif
    """

    def __init__(self, name, value, visibleValue, position, color, visibleName, paramType, parent=None):

        super(Parameter, self).__init__(parent)

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.parent = parent		# referencia na agregujuci komponent
        self.paramType = paramType		# typ parametra
        self.position = position		# aktualna poloha vzhladom na rodicovsky komponent
        self.name = name			# meno parametra
        self.value = value			# hodnota parametra
        self.visibleValue = visibleValue 	# viditelnost parametra
        self.visibleName = visibleName 	# viditelnost mena parametra
        self.color = color			# farba textu parametra
        self.borderColor = Color.blue        # farba borderu parametra
        self.font = QFont('Decorative', 10)
        self.box = QRectF(0, 0, 10, 10)

        # automaticke urcenie typu parametra, ak nebol explicitne zadany, pri
        # neurcenom resp. neznamom type parametra sa nastavi PARAM.STRING

        if self.paramType == PARAM.NONE:

            if type(value) == int:
                self.paramType = PARAM.INT

            elif type(value) == float:
                self.paramType = PARAM.FLOAT

            elif type(value) == complex:
                self.paramType = PARAM.COMPLEX

            else:
                self.paramType = PARAM.STRING

    def __str__(self):
        out = 'Parameter('
        out += 'name:%s ' % self.name
        out += 'value:%s ' % self.value
        out += 'paramType:%s ' % self.paramType
        # out += 'position:%s ' % self.position
        out += 'visibleValue:%s ' % self.visibleValue
        out += 'visibleName:%s ' % self.visibleName
        # out += 'color:%s )' % self.color  # farba textu parametra
        return out

    def paint(self, painter, option, widget=None):
        '''!
        @if English

        @endif

        @if Slovak

        Grafické zobrazenie parametra.

        Vizuálne zobrazenie hodnoty parametra závisí od typu parametra a nastavenia flagov.

        @endif
        '''
        # painter.setRenderHint(QPainter.TextAntialiasing)

        if self.visibleValue is True:
            painter.setFont(self.font)
            painter.setPen(QPen(self.color, 1))

            # uprava zobrazenia hodnoty parametrov
            s = str(self.value)
            if self.paramType == PARAM.STRING:
                pass

            elif self.paramType == PARAM.INT:
                pass

            elif self.paramType == PARAM.FLOAT:
                # uprava zobrazenia, nezobrazuju sa desatinne nuly
                if modf(self.value)[0] == 0.0:
                    s = str(int(self.value))

            # zobrazenie mena parametra
            if self.visibleName is True:
                    s = self.name + '=' + s
            else:
                if self.paramType in [PARAM.FILE_PSE,
                                      PARAM.FILE_CSV,
                                      PARAM.FILE_PNG]:
                    # pri  PARAM.FILE sa pri vybere zobrazenia mena parametru zobrazi
                    # cela cesta k suboru, inak len samotne meno suboru
                    if os.path.exists(self.value):
                        (head, s) = os.path.split(self.value)
                    else:
                        s = 'Error file name'

            fm = QFontMetrics(self.font)    # urcenie rozmerov textu a centrovanie vzhladom
            tw = fm.width(s)	        # k zadanej polohe referencneho bodu
            th = fm.height()

            self.box = QRectF(self.position.x() - tw / 2, self.position.y() - th / 2, tw, th)
            painter.drawText(self.box, Qt.AlignCenter, s)

            # vykreslenie borderu komponentu - podla rozmerov textu
            if self.isSelected() is True:
                painter.setPen(QPen(self.borderColor, 1, Qt.DashLine))
                painter.setBrush(QBrush(Qt.NoBrush))
                painter.drawRect(self.box)
        else:
            self.box = QRectF(0, 0, 0, 0)

    def boundingRect(self):
        return self.box

    def setPosition(self, p):
        q = self.parent.pos()
        self.position = p - q


class Component(QGraphicsItem):
    """!
    @if English

    Superclass for visual components.

    @endif

    @if Slovak

    Supertrieda pre vizualne komponenty.

    @endif
    """

    def __init__(self, className, position=QPoint(0, 0), parent=None):
        super(Component, self).__init__(parent)

        # self.isSelected=False			# priznak vybraneho komponentu
        self.setPos(position)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        # cesta k umiestneniu suboru - treba pre urcenie umiestnenia
        # suboru s obrazkom k shape v adresaroch ./img
        file_path = sys.modules[self.__class__.__module__].__file__
        self.path, file_name = os.path.split(file_path)

        self.shapeSvg = None			# referencia na svg ikony v shape
        self.shapePng = None
        self.position = position			# aktualna poloha objektu

        self.uid = 1				# identifikacne cislo objektu
        self.className = className			# meno triedy objektu
        self.diagram = None                           # ref na diagram, na ktorom je umiestneny komponent
        self.compType = TYPE_DECORATION		# typ objektu
        self.box = QRectF(0, 0, 10, 10)		# ohranicenie objektu
        self.shapeImage = ''		         # obrazok komponentu (SVG,PNG ... - ak je pouzity)
        self.shapeColor = Color.red			# farba komponentu vytvoreneho na graf. kontexte
        self.shapeFillColor = Color.cadetBlue         # farba vyplne komponentu
        self.borderColor = Color.blue		# farba ohranicenia objektu

        self.flippedVertical = False                  # priznak vertikalneho preklopenia
        self.flippedHorizontal = False                # priznak horizontalneho preklopenia

        self.terminal = {}			        # zoznam terminalov komponentu

        self.parameter = {}			        # parametre komponentu
        self.paramList = []                          # zoznam parametrov komponentu v poradi ich vytvaranie,
                                                     # pouziva sa pri editovani vlastnosti komponentu
                                                     # (nahrada usporiadaneho slovnika pre Python 2)

        self.addParameter('Ref', 'A')                 # default parameter - referencia alebo meno komponentu
        self.setZValue(10)

    def __str__(self):
        '''
        '''
        s = '\n'
        s = s + '<C> Comp. name :' + str(self.className) + '\n'
        s = s + '           uid :' + str(self.uid) + '\n'
        s = s + '           ref :' + self.parameter['Ref'].value + '\n'
        s = s + '      selected :' + str(self.isSelected()) + '\n'
        s = s + '    Terminal(s):' + '\n'
        for t in self.terminal.keys():
            s = s + '          Number :' + str(self.terminal[t].num) + '\n'
            s = s + '          Name   :' + str(self.terminal[t].name) + '\n'
            s = s + '          Value  :' + str(self.terminal[t].value) + '\n'
            s = s + '          Type   :' + \
                str(self.terminal[t].termType) + '\n'
            if len(self.terminal[t].connect) == 0:
                s = s + '             Connect: []' + '\n'
            else:
                s = s + '             Connect:' + '\n'
                for n in self.terminal[t].connect:
                    s = s + '             Net name: ' + str(n.name) + ' Start = ' \
                          + n.startComponent.parameter['Ref'].value + '[' + str(n.startTerminal) + '] \t' + \
                        '  End  = ' + n.endComponent.parameter[
                            'Ref'].value + '[' + str(n.endTerminal) + ']' + '\n'
        return s

    def drawShape(self, painter):
        """!
        @if English

        @endif

        @if Slovak

        Virtualna metoda implementovana v derivovanych komponentoch, neimplementovat v supertriede,
        spolocne vlastnosti su implementovane v metode paint.

        @endif
        """
        pass

    def paint(self, painter, option, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)

        # vykreslenie komponentu
        self.drawShape(painter)

        # vykreslenie terminalov na povrchu komponentu
        # TODO - volba vykreslenia terminalov
        for n in self.terminal:
            self.terminal[n].drawTerminal(painter)

        # vykreslenie borderu komponentu
        if self.isSelected() is True:
            painter.setPen(QPen(self.borderColor, 1, Qt.DashLine))
            painter.setBrush(QBrush(Qt.NoBrush))
            painter.drawRect(self.box)

    def boundingRect(self):
        '''
        @if English

        @endif

        @if Slovak

        Ohraničenie komponentu.

        Štandardné ohraničenie komponentu, pre správnu identifikaciu terminalov je rozmer
        ohraničenia zvačšeny o 10px vzhladom na viditelny box.

        @endif
        '''
        box = QRectF(self.box)	         # deep copy povodneho ohranicenia
        box.adjust(-5, -5, 10, 10)		# temp. uprava rozmerov
        return box

    def updateShape(self):
        '''
        @if English

        @endif

        @if Slovak

        Aktualizácia zobrazenia komponentu.

        Uprava shape komponentu po jeho vytvoreni, zmene parametrov alebo vlastnosti. V derivovanych
        komponentoch moze obsahovat obnovenie farebnej schemy objektu napr. po odstraneni chyby,
        ktora bola opticky indikovana odlisnym (cervenym) sfarbenim objektu.

        @endif
        '''
        # nacitanie grafickeho obrazku shapeImage
        shapeFile = self.path + '/img/' + self.shapeImage

        if os.path.isfile(shapeFile) is True:

            if shapeFile.endswith('.svg') is True:
                self.shapeSvg = QSvgWidget(shapeFile)
                self.shapeSvg.setAttribute(Qt.WA_NoSystemBackground)

            if shapeFile.endswith('.png') is True:
                self.shapePng = QPixmap(shapeFile)

    def drawIcon(self, gc, x, y):
        '''
        @if English

        @endif

        @if Slovak

        Vykreslenie ikony komponentu (SVG alebo PNG).

        Ikona komponentu sa nemení pri horizontálnom preklopení (flip horizontal) komponentu.

        @endif
        '''
        # zrusenie preklopenia komponentu
        if self.flippedHorizontal is True:
            t = gc.transform()
            t.setMatrix(-t.m11(), t.m12(), t.m13(), t.m21(), t.m22(), t.m23(), t.m31(), t.m32(), t.m33())
            gc.setTransform(t)

        #print(self.shapePng)
        if self.shapePng is not None:
            w = self.shapePng.width()
            h = self.shapePng.height()
            gc.drawPixmap(x, y, w, h, self.shapePng)

        if self.shapeSvg is not None:
            self.shapeSvg.render(gc, targetOffset=QPoint(x, y))

        # obnovenie predchadzajuceho nastavenia
        if self.flippedHorizontal is True:
            t = gc.transform()
            t.setMatrix(-t.m11(), t.m12(), t.m13(), t.m21(), t.m22(), t.m23(), t.m31(), t.m32(), t.m33())
            gc.setTransform(t)

    def deleteShape(self):
        """!
        @if English

        @endif

        @if Slovak

        Upratanie externych casti komponentu pri mazanie pocas editovania,
        ktore nie su zaradene do struktury grafickych komponentov.

        Metoda sa volá pri operacii delete komponentu z editora.

        Priklad použitia - interaktivny komponent (QPushButton) je vložený na plochu
        QGraphicsScene priamo metodou addWidget, pri delete komponentu
        nie je možné vložený button zmazať vyradením z kontainera itemov.

        @endif
        """
        pass

    def addTerminal(self, name='', num=1, termtype=0, position=(0, 0), direction=0, connType=TERM.NONE, discType=TERM.CROSS):
        """!
        @if English

        Define new terminal.

        @endif

        @if Slovak

        Pridanie noveho terminálu komponentu.

        Vytvorenie noveho terminálu a zaradenie ho do slovnika terminalov, klúčom je číslo terminálu.
        Vrati referenciu terminalu pre dalsie upravy.

        @endif
        """
        term = Terminal(self, name, num, termtype, position, direction)
        self.terminal[num] = term
        term.termDiscType = discType
        term.termConnType = connType

        return term

    def setPosition(self, position):
        '''
        Nastavenie polohy komponentu.
        '''
        self.setPos(position)
        self.position = position

    def addParameter(self, name, value, visible=False, position=QPoint(0, 0), color=Color.black, visibleName=False, paramType=PARAM.NONE):
        '''!
        @if English

        Add new component parameter.

        @endif

        @if Slovak

        Priradenie noveho parametra komponentu.

        @endif
        '''
        # kontrola na existenciu parametra, zabranenie opakovanemu vytvaraniu rovnakych parametrov
        if name not in self.parameter:
            # vytvorenie noveho parameter
            param = Parameter(name, value, visible, position, color, visibleName, paramType, self)
            self.parameter[name] = param
            self.paramList.append(param)
        else:
            # update vlastnosti existujuceho parametra
            self.parameter[name].value = value
            self.parameter[name].visibleValue = visible
            self.parameter[name].position = position
            self.parameter[name].color = color
            self.parameter[name].visibleName = visibleName
            self.parameter[name].paramType = paramType

    def sim(self, flag, value, time, step):
        """!
        @if English

        @endif

        @if Slovak

        Implementácia algoritmu simulácie.

        Metóda je definovana v derivovaných objektoch.

        @endif
        """
        pass

    def gen(self):
        """!
        @if English

        @endif

        @if Slovak

        @endif
        """
        pass


class AgregateComponent(Component):
    '''
    Supertrieda pre komponenty obsahujuce vnutornu strukturu zlozenu z
    virtualnych komponentov.

    Vnutorna struktura - virtualny diagram je ekvivalentna standardnemu
    diagramu, pri simulacii sa komponenty a prepojenia pridavaju
    k existujucim zoznamom v diagrame.

    Virtualny diagram je mozne vytvarat staticky alebo programovo (dynamicky).
    Nie je mozne menit strukturu diagramu pocas simulacie.
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.componentList = []		 # lokalny zoznam virtualnych komponentov
        self.netList = []			 # lokalny zoznam virtualnych prepojeni
        self.compType = TYPE_SIM_AGREGAT
        self.compCounter = self.uid * 1000  # lokalny counter odvodeny od UID komponentu
        self.netCounter = self.uid * 1000

    def addComponent(self, comp):
        '''
        Pridanie noveho komponentu do virtualneho diagramu.
        '''
        self.compCounter = self.compCounter + 1
        comp.uid = self.compCounter
        self.componentList.append(comp)
        return comp

    def addNet(self, comp1, term1, comp2, term2):
        '''
        Pridanie noveho prepojenia do diagramu.

        Prepojenie je ekvivalentom standardneho Net-u, neobsahuje ale nijake
        vertexy.
        '''
        net = VirtualNet(comp1, term1, comp2, term2)
        self.netCounter = self.netCounter + 1
        net.uid = self.netCounter
        self.netList.append(net)
        return net


class VirtualComponent():
    '''!
    @if English


    @endif

    @if Slovak

    Supertrieda pre virtualne komponenty.

    Implementacia supertriedy pre zjednodusene komponenty bez grafickeho
    zobrazovania na ploche.

    @endif
    '''

    def __init__(self):
        self.uid = 0			# identifikacne cislo objektu
        self.terminal = {}			# zoznam terminalov komponentu
        self.parameter = {}			# parametre komponentu
        self.className = ''
        self.addParameter('Ref', 'VIRT')

    def addTerminal(self, name, num, termtype):
        '''
        Vytvorenie noveho terminalu a zaradenie ho do slovnika.
        '''
        term = VirtualTerminal(self, name, num, termtype)
        self.terminal[num] = term

    def addParameter(self, name, value):
        '''
        Priradenie noveho parametra komponentu.
        '''
        param = VirtualParameter(name, value)
        self.parameter[name] = param
        self.parameter[name].value = value

    def sim(self, flag, value, time, step):
        pass
