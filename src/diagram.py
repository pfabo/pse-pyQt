# -*- coding: utf-8 -*-

import json
import logging

from numpy import sqrt
import six

from component import Component, Parameter
from componenttypes import TYPE_CONN_VIRTUAL, TYPE_CONNECTION, TYPE_SIM_AGREGAT
from connection import Connection
from net import Net, Vertex, NET_STANDARD, NET_VIRTUAL


if six.PY2:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
else:
    # from PyQt5.QtSvg import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *

LOG = logging.getLogger(__name__)

'''!
@if English

@endif

@if Slovak

@todo - doplnit nastavenie citlivosti pre zachytavanie prepojenia k terminalom
@todo - kompenzacia pre polohu parametra pri transformacii komponentu (ROT, MIRROR)

@endif

'''

DEBUG = False


class GRID:
    NONE = 0  # mriezka nie je zobrazena
    LINE = 1  # ciarova mriezka - 10x10
    LINE_BIG = 2  # ciarova mriezka - 20x20
    DOT = 3  # bodova mriezka  - 10x10


class MODE:
    # ADD_COMPONENT = 1001		# pridanie komponentu z kniznice
    MOVE = 1002  # posuvanie komponentu alebo vertexu
    # DELETE_COMPONENT = 1003 	# zmazanie komponentu

    ADD_NEW_NET = 1006  # vytvorenie noveho prepojenia
    # DELETE_NET = 1007		# zmazanie prepojenia
    SELECT_NET = 1008  # vybranie/selekcia prepojenia/(-ni)

    ADD_NEW_VERTEX = 1009  # pridanie vrcholu k novemu prepojeniu
    MOVE_VERTEX = 1010  # posun vrcholu
    DELETE_VERTEX = 1011  # zmazanie vrcholu
    INSERT_VERTEX = 1012  # pridanie vrcholu k existujucemu prepojeniu

    ADD_JUNCTION = 1013  # pridanie prepojenia k net-u, rozdelenie na dva segmenty
    DEL_JUNCTION = 1014  # zmazanie kompletnej siete aj s pripojeniami inych sieti
    REMOVE_JUNCTION = 1015  # zmazanie prepojenia a zlucenie 2 sieti

    SIMULATION = 2000


class Diagram(QGraphicsScene):
    '''!
    @if English

    @endif

    @if Slovak

    Editor diagramov.

    Trieda pre tvorbu a editovanie diagramov, implementuje všetky aktivity
    potrebné k vytvoreniu a úpravám diagramov.


    @endif
    '''

    def __init__(self, parent=None):
        super(Diagram, self).__init__()

        self.parent = parent
                                                    # pocitadla pre identifikaciu objektov
        self.compCounter = 0                        # pocitadlo poctu komponentov v editore
        self.netCounter = 0                         # pocitadlo poctu net-ov v editore

        self.grid = 10                              # zakladny rozmer gridy
        self.snapOnGrid = True                      # lepenie komponentov na mriezku
        self.gridType = GRID.LINE  # typ mriezky
        self.gridShow = True                        # zobrazenie mriezky
        self.backgrImage = None                     # obrazok na pozadi

        self.fileName = "Untitled.pse"              # default meno suboru
        self.__mode = MODE.MOVE  # default mod editora

        # kontainery elementov editora
        self.componentList = []	                # zoznam komponentov na ploche
        self.netList = []		                # zoznam prepojeni medzi komponentami

        # inicializacia priznakov a docasnych konstant
        self.activeComponent = None	                # referencia na vybrany/posuvany komponent
        self.activeParameter = None	                # aktivny parameter kompnentu
        self.activeNet = None	                # aktivne prepojenie
        self.activeVertex = None	                # index posuvaneho vertexu

        # pridavanie noveho prepojenia
        self.createdNet = None	                # referencia na vytvarane prepojenie
        self.newVertexPosition = None               # poloha aktualne pridavaneho vertexu

        # inicializacia premennych
        self.rotAngle = 90		                # uhol rotacie komponentov
        self.rotParam = False	                # rotovanie parametrov spolu s komponentom

        self.zoom = 100                             # @todo - implementovat zoom
        self.scale = float(self.zoom) / 100.0

        self.mousePosOffset = QPoint(0, 0)          # offset polohy mysi na aktivnom komponente
                                                    # voci polohe (0,0) pri pohybe komponentu, zabranuje
                                                    # poskakovaniu komponentu na zaciatku jeho  presunu
        self.setGrid(self.gridType)

        self.refreshThread = None                   # referencia na thread periodickeho refresh komponentov na ploche
        self.startRefresh()                         # @todo - optional, spustat podla volby parametrov editora
                                                    # @todo - refresh nefunguje pocas simulacie ...

    def _set_cursor(self, cursor):
        '''set cursor to the all view widgets attached to this diagram'''
        for view in self.views():
            view.setCursor(cursor)

    def _get_mode(self):
        return self.__mode

    def _set_mode(self, mode):
        '''Set diagram mode. Mouse cursor is set accordingly.

        :param mode: enum from MODE
        '''
        if self.__mode == mode:
            return
        self.__mode = mode

        if mode in [MODE.MOVE, MODE.ADD_JUNCTION, MODE.SELECT_NET]:
            self._set_cursor(Qt.ArrowCursor)
        elif mode in [MODE.ADD_NEW_NET]:
            self._set_cursor(Qt.CrossCursor)
        elif mode in [MODE.SIMULATION]:
            self._set_cursor(Qt.BusyCursor)
        else:
            pass

    # diagram mode like MOVE, SIMULATION etc..
    mode = property(_get_mode, _set_mode)

    def startRefresh(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.refreshThread = RefreshThread(self)

    def stopRefresh(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        if self.refreshThread is not None:
            self.refreshThread.stop()
            self.refreshThread = None

    def dropEvent(self, event):
        '''!
        @if English

        @endif

        @if Slovak

        Ukoncenie drag & drop aktivity. Po ukonceni sa nastavi mod posuvania
        komponentov.

        @endif
        '''
        x = event.scenePos().x()
        y = event.scenePos().y()
        name = (event.mimeData().text())
        self.addComponent(name, x, y)

        event.setDropAction(Qt.CopyAction)
        event.accept()

        self.mode = MODE.MOVE

    def dragEnterEvent(self, event):
        '''
        '''
        event.accept()

    def dragMoveEvent(self, event):
        '''
        '''
        event.accept()

    def setGrid(self, gridType):
        '''!
        @if English

        @endif

        @if Slovak

        Nastavenie typu mriezky podľa príznaku gridType

        @endif
        '''
        if gridType == GRID.NONE:
            self.setBackgroundBrush(QBrush(QPixmap(None)))

        elif gridType == GRID.LINE:
            self.setBackgroundBrush(QBrush(QPixmap('./icons/grid_01.png')))

        elif gridType == GRID.LINE_BIG:
            self.setBackgroundBrush(QBrush(QPixmap('./icons/grid_03.png')))

        elif gridType == GRID.DOT:
            self.setBackgroundBrush(QBrush(QPixmap('./icons/grid_02.png')))

        self.gridType = gridType
        self.update()

    def cancelAction(self):
        '''!
        @if English

        @endif

        @if Slovak

        Zrusenie zadavania siete

        @endif
        '''
        # zrusenie aktualne zadavanej siete
        if self.createdNet is not None:
            # vyradenie siete z grafickeho kontaineru
            self.removeItem(self.createdNet)

            # odpojenie vytvaranej siete
            num = self.createdNet.startTerminal
            comp = self.createdNet.startComponent
            comp.terminal[num].connect.remove(self.createdNet)
            self.createdNet = None
            self.activeNet = None
            self.newVertexPosition = None

        self.mode = MODE.MOVE
        self.update()

    def mousePressEvent(self, event):
        '''!
        @if English

        @endif

        @if Slovak

        Spracovanie udalosti pri kliknuti mysi.

        @endif
        '''
        super(Diagram, self).mousePressEvent(event)
        x = event.scenePos().x()
        y = event.scenePos().y()

        # deaktivovanie vsetkych elementov diagramu
        self.activeComponent = None
        if self.activeVertex is not None:
            self.activeVertex.net.setSelected(False)
            self.activeVertex = None
        self.activeParameter = None

        # vyber elementu pod kurzorom mysi
        t = QTransform()
        item = self.itemAt(x, y, t)

        # zrusenie vyberu siete cez bounding box, siet sa vybera len cez metodu
        # findNearestEdge
        if isinstance(item, Net) is True:
            item.setSelected(False)
            item = None

        if item is None:
            # ziaden element sa nevyskytuje v dosahu mysi
            # vyhladanie najblizsej hrany
            net, index, pos, dist = self.findNearestEdge(x, y)
            if net is not None:
                net.setSelected(True)

        if self.mode == MODE.SIMULATION:
            # povolenie vyberu (a zmeny vlastnosti) pre komponenty v simulacnom mode
            if isinstance(item, Component) is True:
                self.activeComponent = item
                self.activeComponent.setSelected(True)

        #-------------------------------------------
        # posuvanie elementov diagramu
        #-------------------------------------------
        elif self.mode == MODE.MOVE:
            if isinstance(item, Component) is True:
                self.activeComponent = item
                self.activeComponent.setSelected(True)
                # korekcia posunu komponentu voci polohe mysi
                if self.snapOnGrid is True:
                    gr = self.grid
                    x = gr * ((x + gr / 2) // gr)
                    y = gr * ((y + gr / 2) // gr)

                self.mousePosOffset = self.activeComponent.mapFromScene(x, y)

            if isinstance(item, Parameter):
                self.activeParameter = item

            if isinstance(item, Vertex):
                self.activeVertex = item
                self.activeVertex.net.setSelected(True)

        #-------------------------------------------
        # pridanie novej siete
        #-------------------------------------------
        elif self.mode == MODE.ADD_NEW_NET:
            self.unselectAll()

            num, (tx, ty), comp = self.findNearestTerminal(x, y)

            if num is not None:
                # najdeny terminal, vytvorenie noveho docasneho prepojenia
                # do zoznamu aktivnych prepojeni sa zaradi po regulernom
                # pripojeni ku koncovemu terminalu
                self.createdNet = Net(self)
                self.createdNet.setSelected(True)
                self.addItem(self.createdNet)		# zaradenie do GUI kontainera

                self.createdNet.isNewNet = True

                # inicializacia pociatocneho bodu prepojenia
                # suradnicami terminalu
                self.createdNet.startTerminal = num
                self.createdNet.startComponent = comp

                # zaradenie polohy terminalu do zoznamu vertexov
                self.createdNet.addVertex(tx, ty)

                # zmena stavu pripojeneho terminalu
                comp.terminal[num].connect.append(self.createdNet)

                if DEBUG:
                    print('>>> Mode MODE.ADD_NEW_NET')
                    print('    Start terminal : num=', num, 'x=', tx, 'y=', ty, 'comp=', comp.className)
                    print('    New net name   :', self.createdNet.name)

                # zmena modu, zadavanie dalsich vertexov alebo ukoncenie
                # prepojenia
                self.mode = MODE.ADD_NEW_VERTEX

        #-------------------------------------------
        # novy vertex pripojenia a ukoncenie prepojenia
        #-------------------------------------------
        elif self.mode == MODE.ADD_NEW_VERTEX:
            # kontrola na ukoncenie netu na terminali
            num, (tx, ty), comp = self.findNearestTerminal(x, y)

            if num is not None:
                # kontrola koncoveho bodu - koncovymm terminalom nemoze byt
                # startovaci terminal
                if (self.createdNet.startTerminal == num and self.createdNet.startComponent == comp):
                    # ignorovanie kliknutia v blizkosti terminalu
                    return

                # inicializacia koncoveho bodu prepojenia
                self.createdNet.endTerminal = num
                self.createdNet.endComponent = comp

                # zaradenie polohy terminalu do zoznamu vertexov
                self.createdNet.addVertex(tx, ty)

                # zaradenie ukonceneho prepojenia do zoznamu prepojeni
                self.netList.append(self.createdNet)
                self.createdNet.isNewNet = False
                self.createdNet.setSelected(False)

                if DEBUG:
                    print('>>> Mode MODE.ADD_NEW_VERTEX')
                    print('    Zadavanie vertexov ukoncene, najdeny koncovy terminal')
                    print('    Net            :', self.createdNet.name)
                    print('    Terminal       : num=', num, 'x=', tx, 'y=', ty, 'comp=', comp.className)
                    print('    Vertex list')
                    for v in self.createdNet.vertexList:
                        print('    ', v)

                # zmena stavu pripojeneho terminalu
                comp.terminal[num].connect.append(self.createdNet)
                self.createdNet = None
                self.newVertexPosition = None

                self.mode = MODE.ADD_NEW_NET

            else:
                # pridanie dalsieho vertexu (v mriezke)
                if self.snapOnGrid is True:
                    gr = self.grid
                    x = gr * ((x + gr / 2) // gr)
                    y = gr * ((y + gr / 2) // gr)

                self.createdNet.addVertex(x, y)
                self.createdNet.setSelected(True)

                if DEBUG:
                    print('>>> Mode MODE.ADD_NEW_VERTEX')
                    print('    Created new vertex at : ', x, y)

        #-------------------------------------------
        # add vertex - pridanie noveho vertexu
        #-------------------------------------------
        elif self.mode == MODE.INSERT_VERTEX:
            net, index, pos, dist = self.findNearestEdge(x, y)

            if net is not None:
                self.activeVertex = net.insertVertex(index + 1, x, y)

                # po pridani vertexu prechod do modu presunu vertexu
                # inicializacia hodnot pre presun (lave tlacitko je stlacene)
                self.activeNet = net

                self.mode = MODE.MOVE

                if DEBUG:
                    print ('>>> Mode MODE.INSERT_VERTEX')
                    print ('    Net name        : ', net.name)

        #-------------------------------------------
        # delete vertex - vyber vertexu pre mazanie
        #-------------------------------------------
        elif self.mode == MODE.DELETE_VERTEX:
            if isinstance(item, Vertex) is True:
                item.net.deleteVertex(item)
                if DEBUG:
                    print ('>>> Mode MODE.DELETE_VERTEX')

        #-------------------------------------------
        # add connection - pridanie prepojenia k existujucemu netu
        #-------------------------------------------
        elif self.mode == MODE.ADD_JUNCTION:
            if self.snapOnGrid is True:
                gr = self.grid
                x = gr * ((x + gr / 2) // gr)
                y = gr * ((y + gr / 2) // gr)
            self.addConnection(x, y)

            self.mode = MODE.MOVE

        #-------------------------------------------
        # znazanie prepojenia
        #-------------------------------------------
        elif self.mode == MODE.REMOVE_JUNCTION:
            self.deleteConnection(x, y)

            self.mode = MODE.MOVE

        self.update()

    def mouseMoveEvent(self, event):
        '''!
        @if English

        @endif

        @if Slovak

        Spracovanie udalosti pri pohybe mysi.

        @endif
        '''
        x = event.scenePos().x()
        y = event.scenePos().y()

        if self.snapOnGrid is True:
            gr = self.grid
            x = gr * ((x + gr / 2) // gr)
            y = gr * ((y + gr / 2) // gr)

        if self.mode == MODE.MOVE:
            # print('MOVE EVENT', self.activeComponent)
            # pusuvanie elementov pri stlacenom lavom tlacitku mysi

            if (event.buttons() and Qt.LeftButton) == Qt.LeftButton:

                if self.activeComponent is not None:
                    # uprava suradnic - ofset komponentu voci polohe mysi
                    self.activeComponent.setPosition(
                        QPoint(x, y) - self.mousePosOffset)

                if self.activeVertex is not None:
                    self.activeVertex.setPosition(QPointF(x, y))
                    self.activeVertex.net.updateBoundingRect()

                if self.activeParameter is not None:
                    self.activeParameter.setPosition(QPointF(x, y))

        elif self.mode == MODE.ADD_NEW_VERTEX:
            self.newVertexPosition = (x, y)

        super(Diagram, self).mouseMoveEvent(event)

        # QApplication.setOverrideCursor(self.cursor)
        self.update()

    def mouseReleaseEvent(self, event):
        '''!
        '''
        super(Diagram, self).mouseReleaseEvent(event)
        self.update()

    def findNearestEdge(self, x, y):
        '''!
        @if English

        @endif

        @if Slovak

        Vyhladanie najblizsej hrany (useku medzi dvoma vertexami).
        Vrati dvojicu vertexov hrany.

        @todo algoritmus BRUTE FORCE, optimalizovat len na prehladavanie
              najblizsich prepojeni, ulozit do usporiadanej mnoziny podla
              polohy.

        @endif
        '''
        self.unselectAll()

        distance = 1e6
        foundNet = None
        vertIndex = None
        vertPos = None

        # prehladanie zoznamu prepojeni standardnych prepojeni, virtualne
        # prepojenia su z prehladavania vylucene
        for c in self.netList:
            if c.netType == NET_STANDARD:
                index = 0

                x1 = c.vertexList[0].position().x()
                y1 = c.vertexList[0].position().y()

                for q in c.vertexList[1:]:
                    x2 = q.position().x()
                    y2 = q.position().y()
                    px = x2 - x1
                    py = y2 - y1

                    if (x2 == x1) and (y2 == y1):
                        # kliknutie na existujuci vertex
                        # vrati hodnotu vzdialenosti d=0 a polohu zaciatku
                        # vertexu
                        d = 0

                    else:
                        # kliknutie mimo vertexu
                        tm = px * px + py * py
                        u = ((x - x1) * px + (y - y1) * py) / float(tm)

                        if u > 1:
                            u = 1
                        elif u < 0:
                            u = 0

                        xn = x1 + u * px
                        yn = y1 + u * py

                        dx = xn - x
                        dy = yn - y

                        d = sqrt(dx * dx + dy * dy)

                    if d < distance:
                        distance = d
                        foundNet = c
                        vertIndex = index
                        vertPos = (x1, y1)
                    index = index + 1

                    (x1, y1) = (x2, y2)

        if distance < 20:
            return foundNet, vertIndex, vertPos, distance
        else:
            return None, None, None, None

    def findNearestTerminal(self, x, y):
        '''!
        Vyhlada najblizsi terminal. Vrati cislo terminalu, polohu a komponent.

        @type (x,y):	tuple
        @param (x,y):	pozicia vzhladom ku ktorej sa vyhladava najblizsi komponent

        @todo - parametrizovat v nastaveni citlivost vyhladavania
        '''
        distance = 1e6		# vzdialenost k najdenemu komponentu
        termNum = None		# cislo terminalu
        termPos = None		# poloha terminalu
        item = None			# koponent, ku ktoremu patri najdeny terminal

        t = QTransform()
        item = self.itemAt(x, y, t)

        # zrusenie vyberu siete cez bounding box, siet sa vybera len cez metodu
        # findNearestEdge
        if isinstance(item, Net):
            item.setSelected(False)
            item = None

        if isinstance(item, Component):
            # iteracia po zozname terminalov podla cisla terminalu
            for num in item.terminal.keys():
                t = item.terminal[num]

                # poloha terminalu, prepocet na realnu poziciu pri otoceni
                # komponentu
                tpos = t.position
                q = item.mapToScene(tpos)

                tx = q.x()
                ty = q.y()
                d = sqrt((tx - x) * (tx - x) + (ty - y) * (ty - y))

                if d < distance:
                    distance = d
                    termNum = num
                    termPos = (tx, ty)

        if distance > 15:
            # TODO - vzdialenost parametrizovat v nastaveni
            # terminal neexistuje alebo nenajdeny
            return None, (0, 0), item
        else:
            return termNum, termPos, item

    def unselectAll(self):
        '''!
        @if English

        @endif

        @if Slovak

        Zrusenie selekcie vsetkych komponentov (vykreslenie orig. a ine).

        @endif
        '''
        for comp in self.componentList:
            comp.setSelected(False)
            for k in comp.parameter.keys():
                comp.parameter[k].setSelected(False)

        for q in self.netList:
            q.setSelected(False)
        self.update()

    def addComponent(self, compClassName, x, y):
        '''!
        @if English

        @endif

        @if Slovak

        Zaradenie komponentu do zoznamu. Vytvori novy objekt na zaklade mena triedy.

        @endif
        '''

        if DEBUG:
            print ('>>> FUNC Diagram.addComponent  arg:', compClassName)
        self.unselectAll()

        x = x / self.scale
        y = y / self.scale

        if self.snapOnGrid is True:
            gr = self.grid
            x = gr * ((x + gr / 2) // gr)
            y = gr * ((y + gr / 2) // gr)

        # doplnenie pre PYTHON 2 - compClassName je typu QString
#        compClassName = str(compClassName)

        # constructor = globals()[compClassName]
        import lib
        try:
            constructor = getattr(lib, compClassName)
        except AttributeError:
            constructor = globals()[compClassName]

        component = constructor(compClassName, QPoint(x, y))
        self.compCounter = self.compCounter + 1

        # inicializacia a uprava parametrov komponentu, inicalizacia referencie
        # na diagram pre komponenty, ktore potrebuju pristup k systemovym prostriedkom
        component.uid = self.compCounter
        component.diagram = self

        # inicializacia referencie komponentu (ak je zadana)
        if 'Ref' in component.parameter:
            component.parameter['Ref'].value = component.parameter['Ref'].value + str(component.uid)

        self.addItem(component)
        self.componentList.append(component)

        component.updateShape()

        self.activeComponent = None
        return component

    def copyComponent(self):
        '''!
        @if English

        @endif

        @if Slovak

        Kopia selektovanych komponentov

        @endif
        '''
        if DEBUG:
            print ('>>> FUNC Diagram.copyComponent')

        newCompList = []
        offset = QPoint(30, 30)

        # vyber selektovanych komponentov
        for comp in self.componentList:
            # TODO - kontrola typu komponentu pre kopirovanie
            if comp.isSelected() is True:
                newCompList.append(comp)

        # vytvaranie kopii vybranych komponentov
        for comp in newCompList:
            name = comp.className
            pos = comp.position + offset
            newComp = self.addComponent(name, pos.x(), pos.y())
            # kopia nastavenia parametrov komponentu s vynimkou hodnoty refrencie
            for p in comp.parameter:
                if p != 'Ref':
                    newComp.parameter[p].value = comp.parameter[p].value
                newComp.parameter[p].position = comp.parameter[p].position
                newComp.parameter[p].visibleValue = comp.parameter[p].visibleValue
                newComp.parameter[p].visibleName = comp.parameter[p].visibleName
                newComp.parameter[p].color = comp.parameter[p].color
            newComp.updateShape()

    def deleteNet(self, net):
        '''!
        @if English

        @endif

        @if Slovak

        Odstranenie netu, odstrani net zo zoznamu prepojeni terminalov.

        @endif
        '''

        if isinstance(net, Net) is not True:
            if DEBUG:
                print ('>>> FUNC Diagram.deleteNet arg: wrong fnnction argument type')
            return

        if DEBUG:
            print ('>>> FUNC Diagram.deleteNet arg:', net.name)

        # 1. odstranenie prepojenia z prepojeni v zoznamoch terminalov
        # startovaci terminal
        term = net.startComponent.terminal[net.startTerminal]

        # odstranenie prepojenia zo zoznamu sieti pripojenych k terminalu
        term.connect.remove(net)

        # koncovy terminal
        term = net.endComponent.terminal[net.endTerminal]

        # odstranenie prepojenia zo zoznamu sieti pripojenych k terminalu
        term.connect.remove(net)

        for v in net.vertexList:		# odstranenie vertexov z graf. kontainera
            v.setVisible(False)
            self.removeItem(v)

        if net.netType != NET_VIRTUAL:
            net.setVisible(False)
            self.removeItem(net)		# odstranenie siete z grafickeho kontainera
        self.netList.remove(net)
        del net

    def deleteComponentWithNets(self, comp):
        '''!
        @if English

        @endif

        @if Slovak

        Zmazanie vybraneho komponentu vratane vsetkych pripojenych sieti.

        @endif
        '''
        if isinstance(comp, Component) is not True:
            return

        # zoznam terminalov komponentu
        tlist = comp.terminal

        # iteracia po zozname terminalov komponentov
        for tnum in tlist:
            # tnum obsahuje cislo - kluc terminalu v slovniku, vyber terminalu
            term = tlist.get(tnum)

            # zmazanie vsetkych prepojeni terminalu
            while len(term.connect) > 0:
                self.deleteNet(term.connect[0])

        # zmazanie komponentu
        if comp.compType != TYPE_CONN_VIRTUAL:
            comp.setVisible(False)
            self.removeItem(comp)

        self.componentList.remove(comp)
        comp.deleteShape()
        del comp

    def deleteComponent(self, comp):
        """!
        @if English

        @endif

        @if Slovak

        Zmazanie komponentu bez pripojenych netov.

        Zmazane terminaly komponentu sa nahradia prepojovacimi objektami.

        @todo pri mazani komponentu CONNECTION s pripojenenym len jednym
              netom zmazat aj pripojeny net.

        @endif
        """
        if isinstance(comp, Component) is not True:
            if DEBUG:
                print ('>>> FUNC Diagram.deleteComponent arg: wrong function argument type')
            return

        if DEBUG:
            print ('>>> FUNC Diagram.deleteComponent arg:', comp)

        #if isinstance(comp, Connection) is True:
        # 1. Zmazanie prepojenia medzi net, vysledok mazania zavisi od stavu prepojenia,
        #    resp. poctu a typu pripojenych net-ov
        if comp.compType == TYPE_CONNECTION:
            self.deleteConnection(comp)
            return

        # 2. Zmazanie bloku -vyzaduje zmazanie vnutornych prepojeni v blokoch
        #    medzi terminalom a portom vnutornej struktury pred mazanim komponentu
        if comp.compType == TYPE_SIM_AGREGAT:
            for t in comp.terminal:
                for n in comp.netList:    # zoznam LOKALNYCH prepojenie v bloku
                    if n in comp.terminal[t].connect:
                        comp.terminal[t].connect.remove(n)
            # Vynulovanie lokalnych zoznamov komponentov a prepojeni v bloku
            comp.componentList = []
            comp.netList = []

        # 3. Mazanie komponentu, kontrola pripojenych netov k terminalu
        #    Ak je k terminalu nieco pripojene, terminal bude nahradeny
        #    komponentom Connection

        # zoznam terminalov komponentu
        tlist = comp.terminal

        # iteracia po zozname terminalov komponentov
        for tnum in tlist:
            # tnum obsahuje cislo - kluc terminalu v slovniku, vyber terminalu
            term = tlist.get(tnum)

            # ak je k terminalu daco pripojene, ziskanie polohy terminalu
            if len(term.connect) > 0:
                # vypocet plohy terminalu
                pos = term.position
                q = comp.mapToScene(pos)

                # vytvorenie objektu prepojenia na mieste terminalu
                conn = self.addComponent('Connection', q.x(), q.y())

                # skopirovanie zoznamu pripojenych netov k terminalu do objektu conn
                conn.terminal[1].connect = term.connect

                # vymena terminalov vo vsetkych prepojeniach iteracia cez vsetky nety
                # pripojene k terminalu komponentu
                for n in term.connect:
                    # vymena referencii terminalov v nete za prepojovaci komponent,
                    # vymena sa riadi cislom terminalu aktualneho komponentu
                    if(n.startTerminal == tnum) and (n.startComponent == comp):
                        n.startComponent = conn
                        n.startTerminal = 1
                    if(n.endTerminal == tnum) and (n.endComponent == comp):
                        n.endComponent = conn
                        n.endTerminal = 1

        # zmazanie komponentu
        self.componentList.remove(comp)

        if comp.compType != TYPE_CONN_VIRTUAL:
            comp.setVisible(False)
            self.removeItem(comp)

        comp.deleteShape()
        del comp

    def deleteAll(self):
        '''!
        @if English

        @endif

        @if Slovak

        Zmazanie vsetkych elementov, reset lokalnych premennych.

        @endif
        '''
        if DEBUG:
            print ('>>> FUNC Diagram.deleteAll')

        self.activeComponent = None
        self.createdNet = None
        self.newVertexPosition = None
        self.activeNet = None
        self.activeVertex = None

        self.compCounter = 0
        self.netCounter = 0

        # zmazanie vizualnych casti komponentov a zastavenie internych threadov
        for c in self.componentList:
            c.deleteShape()

        del self.netList
        del self.componentList

        self.netList = []
        self.componentList = []

        self.clear()
        self.update()

    def addConnection(self, x, y):
        '''!
        @if English

        @endif

        @if Slovak

        Pridanie prepojenia k existujucemu net-u.

        Net bude rozdeleny na dva samostatne nety, v bode prepojeni bude
        objekt tr. Junction, oba net-y budu pripojene k nemu.

        Osetrene pridavanie prepojenia na miesto existujuceho terminalu
        a vertexu.

        @todo - kontrola na lavu a pravu cast siete

        @endif
        '''
        if DEBUG:
            print ('>>> FUNC Diagram.addConnection arg: x=', x, 'y=', y)

        # vyhladanie najblizsej hrany netu k pozicii x,y
        net, index, pos, dist = self.findNearestEdge(x, y)  		# @UnusedVariable
        # net   - ref na najdeny net
        # index - por. cislo najdeneho vertexu
        # pos   - ploha vertexu
        # dist  - najdena vzdialenost

        if net is not None:
            # vylucenie pridanie prepojenia na terminal (zaciatocny
            # koncovy bod netu alebo iny connection), dist=0
            if dist == 0 and ((x, y) == net.vertexList[0] or (x, y) == net.vertexList[-1]):
                return

            if DEBUG:
                print ('    Found net       : ', net)
                #print ('    Vertex list     : ', net.vertexList)

            # objekt prepojenia
            conn = self.addComponent('Connection', x, y)

            # rozdelenie netu na dva useky
            # lava strana - inicializacia noveho netu, kopia vertexov do noveho
            # netu
            leftNet = Net(self)
            for v in net.vertexList[:(index + 1)]:
                leftNet.addVertex(v.position().x(), v.position().y())

            leftNet.addVertex(x, y)

            leftNet.startTerminal = net.startTerminal
            leftNet.startComponent = net.startComponent

            leftNet.startComponent.terminal[
                net.startTerminal].connect.append(leftNet)
            leftNet.endTerminal = 1
            leftNet.endComponent = conn

            self.addItem(leftNet)

            # prava strana - inicializacia noveho netu
            rightNet = Net(self)

            # ak je nove prepojenie je umiestnene na mieste vertexu
            # povodneho vertexu nepridavane novu pociatocnu polohu
            if QPointF(x, y) != net.vertexList[index + 1].position():
                rightNet.addVertex(x, y)

            for v in net.vertexList[(index + 1):]:
                rightNet.addVertex(v.position().x(), v.position().y())

            rightNet.startTerminal = 1
            rightNet.startComponent = conn
            rightNet.endTerminal = net.endTerminal
            rightNet.endComponent = net.endComponent

            rightNet.endComponent.terminal[
                net.endTerminal].connect.append(rightNet)

            # inicializacia zoznamu sieti v prepojovacom objekte
            conn.terminal[1].connect = [leftNet, rightNet]

            # zaradenie inicializovanych objektov siete do kontainerov
            self.netList.append(leftNet)
            self.netList.append(rightNet)
            self.addItem(rightNet)
            self.deleteNet(net)

    def deleteConnection(self, comp):
        '''!
        @if English

        @endif

        @if Slovak

        Odstranenie prepojenia z netu. Mozne pripady konfiguracie prepojenia:

        Rozlisuje pripady:
        1.  prepojenie spaja viac ako 2 net-y
            prepojenie sa nedstrani

        2.  prepojenie spaja 2 net-y
            prepojenie sa nahradi vertexom na novom net-e

        3.  prepojenie ma len 1 net
            odstaranie sa prepojenie spolu s net-om

        4.  prepojenie nema ziaden pripojenu net
            odstrani sa prepojenie ako standardny objekt

        @endif
        '''

        if isinstance(comp, Connection) is True:
            conn = comp.terminal[1].connect
            if len(conn) == 2:

                left = conn[0]
                right = conn[1]

                # urcenie lavej a pravej strany prepojenia
                # nove prepojenie zlozene z predchadzajucich dvoch musi
                # na seba nadvazovat
                if left.vertexList[-1] == right.vertexList[0]:
                    left = conn[1]
                    right = conn[0]
                else:
                    left = conn[0]
                    right = conn[1]

                # konstrukcia noveho prepojenia
                net = Net(self)
                for q in left.vertexList:
                    # v = net.addVertex(q.position().x(), q.position().y())
                    net.addVertex(q.position().x(), q.position().y())

                for q in right.vertexList[1:]:
                    # v = net.addVertex(q.position().x(), q.position().y())
                    net.addVertex(q.position().x(), q.position().y())

                net.startTerminal = left.startTerminal
                net.startComponent = left.startComponent

                net.startComponent.terminal[
                    net.startTerminal].connect.append(net)

                net.endTerminal = right.endTerminal
                net.endComponent = right.endComponent

                net.endComponent.terminal[net.endTerminal].connect.append(net)

                self.netList.append(net)
                self.addItem(net)

                # odstranenie povodneho objektu prepojenia aj s net-mi k nemu
                # pripojenymi
                self.deleteComponentWithNets(comp)

            elif len(conn) == 0:
                comp.setVisible(False)
                self.removeItem(comp)
                self.componentList.remove(comp)
                comp.deleteShape()
                del comp

            elif len(conn) == 1:
                self.deleteComponentWithNets(comp)

    def rotateComponentRight(self):
        '''!
        '''
        comp = self.activeComponent
        if comp is not None:
            comp.setRotation(comp.rotation() + self.rotAngle)

            if isinstance(self.activeComponent, Parameter) is True:
                return

            if self.rotParam is False:
                # zrusenie transformacie pre parametre
                for k in comp.parameter.keys():
                    comp.parameter[k].setRotation(
                        comp.parameter[k].rotation() - self.rotAngle)
        self.update()

    def rotateComponentLeft(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        comp = self.activeComponent
        if comp is not None:
            comp.setRotation(comp.rotation() - self.rotAngle)

            if isinstance(self.activeComponent, Parameter) is True:
                return

            if self.rotParam is False:
                # zrusenie transformacie pre parametre
                for k in comp.parameter.keys():
                    comp.parameter[k].setRotation(
                        comp.parameter[k].rotation() + self.rotAngle)

        self.update()

    def flipComponentHorizontal(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        comp = self.activeComponent
        if comp is not None:
            t = comp.transform()

            m11 = t.m11()    # Horizontal scaling
            m12 = t.m12()    # Vertical shearing
            m13 = t.m13()    # Horizontal Projection
            m21 = t.m21()    # Horizontal shearing
            m22 = t.m22()    # vertical scaling
            m23 = t.m23()    # Vertical Projection
            m31 = t.m31()    # Horizontal Position (DX)
            m32 = t.m32()    # Vertical Position (DY)
            m33 = t.m33()    # Addtional Projection Factor

            m11 = -m11

            t.setMatrix(m11, m12, m13, m21, m22, m23, m31, m32, m33)
            comp.setTransform(t)

            # preklopenie priznaku
            comp.flippedHorizontal = not comp.flippedHorizontal

            # zrusenie transformacie pre parametre
            for k in comp.parameter.keys():
                comp.parameter[k].setTransform(t)

    def flipComponentVertical(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        comp = self.activeComponent
        if comp is not None:
            t = comp.transform()

            m11 = t.m11()
            m12 = t.m12()
            m13 = t.m13()
            m21 = t.m21()
            m22 = t.m22()
            m23 = t.m23()
            m31 = t.m31()
            m32 = t.m32()
            m33 = t.m33()

            m22 = -m22

            t.setMatrix(m11, m12, m13, m21, m22, m23, m31, m32, m33)
            comp.setTransform(t)

            # preklopenie priznaku
            comp.flippedVertical = not comp.flippedVertical

            # zrusenie transformacie pre parametre
            for k in comp.parameter.keys():
                comp.parameter[k].setTransform(t)

    def diagramSave(self, filename):
        '''!
        @if English

        @endif

        @if Slovak

        @todo - doplnit ulozenie farieb a fontov
        @todo - doplnit ulozenie parametrov editora (grid, poloha okna, pozicia, velkost)

        @endif
        '''
        if DEBUG:
            print('>>> FUNC Diagram.diagramSave arg:', filename)

        # zmazanie vsetkych virtualnych spojov a prepojeni, ktore boli povytvarane v procese
        # simulacie
        tempList = []
        for comp in self.componentList:
            if comp.compType == TYPE_CONN_VIRTUAL:
                tempList.append(comp)
        for q in tempList:
            self.deleteComponentWithNets(q)

        self.fileName = filename

        q = [self.compCounter,
             self.netCounter,
             self.componentList,
             self.netList]

        s = json.dumps(q, default=self.jsonExport)  # sort_keys=True, indent=4)

        with open(filename, 'w') as output_file:
            output_file.write(s)
            output_file.write('\n')

    def diagramLoad(self, filename):
        '''!
        @if English

        @endif

        @if Slovak

        Nacitanie objektov a prepojeni zo suboru, konverzie a inicializacia
        pocitadiel.

        @endif
        '''
        if DEBUG:
            print('>>> FUNF Diagram.diagramLoad arg: ', filename)

        self.fileName = filename
        s = ''
        with open(self.fileName, 'r') as input_file:
            s = input_file.readlines()

        # nacitanie zapojenia
        readData = json.loads(s[0], object_hook=self.jsonImport)

        # compCounter = readData[0]
        # netCounter = readData[1]
        compList = readData[2]
        netList = readData[3]

        # inicializacia komponentov z nacitaneho zoznamu
        compDict = {}
            # slovnik priradenia uid a refrencie na objekt, treba pri
            # vytvaranie inicializacie sieti

        for data in compList:
            uid = data[0]
            className = data[1]
            [x, y] = data[2]
            paramDict = data[3]

            # spatna kompatibilita so starymi verziami, nemali ulozene
            # transformacie komponentov
            trList = []
            try:
                trList = data[4]
            except:
                pass

            comp = self.addComponent(className, x, y)
            comp.uid = uid
            compDict[uid] = comp

            # nastavenie UID pocitadla na max. hodnotu, uid objektov zo suboru
            # mozu byt vyssie ako hodnota interneho pocitadla, riesi
            # potencialny konflikt pri pridavani komponentov po nahrati diagramu
            # zo suboru
            self.compCounter = max(uid, self.compCounter)

            for k in paramDict.keys():
                try:
                    pdata = paramDict[k]

                    [qx, qy] = pdata[0]
                    value = pdata[1]
                    visibleValue = pdata[2]
                    visibleName = pdata[3]
                    [px, py, pw, ph] = pdata[4]
                    [cr, cg, cb, ca] = pdata[5]

                    comp.parameter[k].position = QPoint(qx, qy)
                    comp.parameter[k].value = value
                    comp.parameter[k].visibleValue = visibleValue
                    comp.parameter[k].visibleName = visibleName
                    comp.parameter[k].box = QRectF(px, py, pw, ph)
                    comp.parameter[k].color = QColor(cr, cg, cb, ca)
                except:
                    # print('>>> WARNING Diagram.diagramLoad - Komponent UID:' + str(uid) + ' neobsahuje parameter ' + str(k))
                    emsg = "Component UID: %s " % uid
                    emsg += "does't contain parameter: %s" % k
                    LOG.error(emsg)

            # rotacia a mirror komponentov
            if trList != []:
                t = comp.transform()

                m11 = t.m11()
                m12 = t.m12()
                m13 = t.m13()
                m21 = t.m21()
                m22 = t.m22()
                m23 = t.m23()
                m31 = t.m31()
                m32 = t.m32()
                m33 = t.m33()

                m11 = trList[1]
                m22 = trList[2]
                t.setMatrix(m11, m12, m13, m21, m22, m23, m31, m32, m33)

                comp.setTransform(t)
                comp.setRotation(trList[0])

                if m11 < 0:
                    comp.flippedHorizontal = True

                if m22 < 0:
                    comp.flippedVertical = True

                # zrusenie mirroru pre parametre komponentu
                if m11 < 0 or m22 < 0:
                    t.setMatrix(m11, m12, m13, m21, m22, m23, m31, m32, m33)
                    for k in comp.parameter.keys():
                        comp.parameter[k].setTransform(t)

            # refresh komponentu podla nahranych parametrov
            comp.updateShape()

        for data in netList:
            netType = data[2]
            if netType == 1:
                uid = data[0]
                name = data[1]

                vertexList = data[3]
                startTerminal = data[4]
                startComponent_uid = data[5]
                endTerminal = data[6]
                endComponent_uid = data[7]

                net = Net(self)
                self.addItem(net)
                net.uid = uid
                net.name = name
                net.netType = netType
                net.startTerminal = startTerminal
                net.endTerminal = endTerminal
                net.vertexList = []

                for q in vertexList:
                    net.addVertex(q[0], q[1])

                try:
                    # inicializacia koncovych bodov
                    net.startComponent = compDict[startComponent_uid]
                    net.endComponent = compDict[endComponent_uid]

                    # inicializacia terminalov
                    net.startComponent.terminal[net.startTerminal].connect.append(net)
                    net.endComponent.terminal[net.endTerminal].connect.append(net)

                    self.netList.append(net)
                except:
                    # ignorovanie prepojeni s neexistujucimi komponentami
                    # po ulozeni simulovaneho diagramu - obsahuje generovane virtualne spoje
                    LOG.warn('ignored diagram connection (due to componet missing)')
                    # print('>>> WARNING Diagram.diagramLoad - ignorovane chybne prepojenie v diagrame')
                    #print('    net name, type  ', data[1], data[2])
                    #print('    start comp , terminal', data[5], data[4])
                    #print('    end comp , terminal  ', data[7], data[4])

                self.netCounter = max(uid, self.netCounter)
        self.update()

    def jsonExport(self, obj):
        '''
        '''

        #if isinstance(obj, complex):
        #    return str(obj)

        if isinstance(obj, Component):
            # vytvorenie slovnika parametrov
            param = {}
            for k in obj.parameter.keys():
                p = obj.parameter[k]

                param[p.name] = [
                    p.position,
                    p.value,
                    p.visibleValue,
                    p.visibleName,
                    p.box,
                    p.color]

            # transformacna matica komponentu
            t = obj.transform()

            # format komponentu
            d = [obj.uid,
                 obj.className,
                 obj.position,
                 param,
                [obj.rotation(), t.m11(), t.m22()]
                 # rotacia a mirror komponentu
                 ]
            return d

        if isinstance(obj, QRectF):
            return [obj.x(), obj.y(), obj.width(), obj.height()]

        if isinstance(obj, QPoint):
            return [obj.x(), obj.y()]

        if isinstance(obj, QPointF):
            return [obj.x(), obj.y()]

        if isinstance(obj, Vertex):
            return [obj.pos.x(), obj.pos.y()]

        if isinstance(obj, Net):
            d = [
                obj.uid,
                obj.name,
                obj.netType,
                obj.vertexList,
                obj.startTerminal,
                obj.startComponent.uid,
                obj.endTerminal,
                obj.endComponent.uid
            ]
            return d

        if isinstance(obj, QColor):
            d = [
                obj.red(),
                obj.green(),
                obj.blue(),
                obj.alpha()
            ]
            return d

        return obj

    def jsonImport(self, dct):
        return dct


class RefreshThread(QThread):
    '''
    @if English

    @endif

    @if Slovak

    Periodicke obnovovanie objektov na ploche editora.

    @endif
    '''

    def __init__(self, diagram):
        super(RefreshThread, self).__init__()
        self.diagram = diagram
        self.runThread = True
        self.start()

    def stop(self):
        self.runThread = False

    def run(self):
        '''
        @if English

        @endif

        @if Slovak

        Periodicky refresh komponentov diagramu 1x za sekundu, obnovenie stavu obrazovky.

        @endif
        '''
        while self.runThread:
            self.sleep(1)
            self.diagram.update()
