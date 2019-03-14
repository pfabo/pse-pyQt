# -*- coding: utf-8 -*-

from numpy import ndarray
import six

if six.PY2:
    from PyQt4.QtGui import *  # @UnusedWildImport
    from PyQt4.QtCore import *  # @UnusedWildImport
else:
    from PyQt5.QtWidgets import *  # @UnusedWildImport
    from PyQt5.QtGui import *  # @UnusedWildImport
    from PyQt5.QtCore import *  # @UnusedWildImport


NET_STANDARD = 1  # standardne prepojenie
NET_VIRTUAL = 2   # neviditelne prepojenie pouzite na prepojenie blokov a terminalov siete


class Vertex(QGraphicsItem):

    def __init__(self, pos, net, parent=None):
        super(Vertex, self).__init__(parent)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.pos = pos			# aktualna poloha vertexu
        self.net = net			# net, ku ktorej vertex patri

        self.setPos(pos)
        self.box = QRectF(-4, -4, 8, 8)
        self.setZValue(5)

    def __str__(self):
        '''
        '''
        s = 'Vertex : px=' + str(self.pos.x()) + '\t py=' + str(self.pos.y())
        return s

    def setPosition(self, position):
        self.pos = position
        self.setPos(position)

    def position(self):
        return self.pos

    def boundingRect(self):
        return self.box

    def paint(self, painter, option, widget=None):
        pass


class Net(QGraphicsItem):
    '''
    @if English


    @endif

    @if Slovak

    Trieda prepojeni medzi komponentami.

    @endif
    '''

    def __init__(self, diagram, parent=None):
        super(Net, self).__init__(parent)

        self.diagram = diagram			# plocha na ktorej je vykresleny net
        diagram.netCounter = diagram.netCounter + 1

        # zakladne parametre siete
        self.uid = diagram.netCounter
        self.name = 'N' + str(diagram.netCounter)  # meno net-u
        self.netType = NET_STANDARD

        # nastavenie farieb
        self.netColor = Qt.darkGreen
        self.netColorSelected = Qt.red

        # zobrazenie siete
        self.width = 1		# sirka obycajneho prepojenia
        self.busWidth = 3		# sirka zbernice
        self.showNetName = False
        self.showNetArrow = False
        self.showNetVertex = False

        self.isNewNet = False		# vytvarany net, nezaradeny do zoznamu
        self.vertexList = []			# zoznam vrcholov

        # pociatocny bod prepojenia
        self.startTerminal = None  # poradove cislo pociatocneho terminalu
        self.startComponent = None  # pripojeny pociatocny objekt

        # koncovy bod prepojenia
        self.endTerminal = None  # poradove cislo koncoveho terminalu
        self.endComponent = None  # pripojeny koncovy objekt

        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setZValue(0)

        self.xmin = 0
        self.ymin = 0
        self.xmax = 0
        self.ymax = 0

    def __str__(self):
        '''
        '''
        s = ''
        s = s + '<N> Net name : ' + str(self.name) + '\n'
        s = s + '    Net uid  : ' + str(self.uid) + '\n'
        s = s + '    Net type : ' + str(self.netType) + '\n'
        s = s + \
            '          Start : (comp uid ' + str(self.startComponent.uid) + ')' + \
                                       'term [' + str(self.startTerminal) + ']' +       \
                                   ' typ:' + str(self.startComponent.terminal[self.startTerminal].termType) + '\n'
        s = s + \
            '          End   : (comp uid ' + str(self.endComponent.uid) + ')' + \
                                       ' term [' + str(self.endTerminal) + ']' + \
                                   ' typ:' + str(self.endComponent.terminal[self.endTerminal].termType) + '\n'
        return s

    def paint(self, painter, option, widget=None):
        '''
        '''
        painter.setRenderHint(QPainter.Antialiasing)
        self.drawNet(painter)

    def boundingRect(self):
        '''
        '''
        return QRectF(self.xmin, self.ymin, self.xmax - self.xmin, self.ymax - self.ymin)

    def updateBoundingRect(self):
        '''
        @if English


        @endif

        @if Slovak

        Prepocet hodnot bounding rectangle. Spravna hodnota je dolezita pre spravne
        vykreslovanie na grafickej scene, pri nespravnych hodnotach sa net
        pri scrolovanie neprekresloval pri polohe mimo zobrazovanej oblasti.

        Pretoze net sa vybera len pomocou metody vyhladania hrany, je potrebne
        pri pouziti metody itemAt (automaticky) selektovany net deselektovat.

        @endif
        '''
        # prepocet novych hranic net-u
        self.xmin = 10000
        self.ymin = 10000
        self.xmax = -10000
        self.ymax = -10000

        for p in self.vertexList:
            px = p.pos.x()
            py = p.pos.y()
            if px > self.xmax:
                self.xmax = px
            if px < self.xmin:
                self.xmin = px
            if py > self.ymax:
                self.ymax = py
            if py < self.ymin:
                self.ymin = py

    def drawNet(self, gc):
        '''
        @if English

        @endif

        @if Slovak

        Prekreslenie net-u podla jeho aktualneho stavu. Nastavenie sirky netu
        podla aktualnej typu aktualnej hodnoty urcenej z dlzky vektora
        hodnot terminalu. Ak je vektor > 1, net je kresleny hrubsou ciarou
        ako zbernica.

        @endif
        '''

        if self.netType == NET_VIRTUAL:
            return

        #----------------------------------------------------------------
        # Nastavenie sirky ciary podla typu terminalu
        #----------------------------------------------------------------
        netWidth = self.width

        if self.isNewNet is False:
            # novy net je kresleny standardnou sirkou, nie je priradena poloha terminalov
            # neda sa urcit typ netu/zbernice
            start_value = self.startComponent.terminal[self.startTerminal].value
            end_value = self.endComponent.terminal[self.endTerminal].value

            if type(start_value) in [ndarray, list] or \
               type(end_value) in [ndarray, list]:
                netWidth = self.busWidth

        #----------------------------------------------------------------
        # Nastavenie farby ciary podla vyberu
        #----------------------------------------------------------------
        netColor = self.netColor
        if self.isSelected() is True:
            netColor = self.netColorSelected

        gc.setPen(QPen(netColor, netWidth))

        # refresh polohy prveho vertexu podla polohy terminalu - kazdy net MUSI
        # zacinat terminalom
        (x, y) = self.startPoint()

        path = QPainterPath()
        path.moveTo(x, y)
        # vykreslenie net-u po posledny vertex
        for q in self.vertexList[1:]:
            x = q.position().x()
            y = q.position().y()
            path.lineTo(x, y)

        # refresh polohy posledneho vertexu, podla aktualne plohy mysi pri
        # vytvarani noveho prepojenia alebo podla polohy terminalu pripojeneho
        # objektu
        if self.isNewNet is True:
            if self.diagram.newVertexPosition is not None:
                (x,
                 y) = self.diagram.newVertexPosition  # buduca poloha, este neodkliknuta
                path.lineTo(x, y)
        else:
            (x, y) = self.endPoint()
            path.lineTo(x, y)
        gc.drawPath(path)

        # pridanie oznacenia vertexov pre aktivny net
        if self.isSelected() is True:
            path = QPainterPath()
            gc.setPen(QPen(netColor, netWidth))
            gc.setBrush(QBrush(Qt.yellow))

            # pri zapojenych netoch nekreslime oznacenie posledneho vertexu,
            # je zapojeny do terminalu
            if self.isNewNet is False:
                vl = self.vertexList[1:-1]
            else:
                vl = self.vertexList[1:]

            # vykreslenie oznacenia
            for q in vl:
                x = q.position().x()
                y = q.position().y()
                gc.drawRect(x - 3, y - 3, 6, 6,)

            gc.drawPath(path)

    def addVertex(self, x, y):
        '''
        @if English

        @endif

        @if Slovak

        @brief Pridanie noveho vertexu

        Vertex sa prida za posledny vertex v poradi.

        @param x suradnice noveho vertexu
        @param y suradnice noveho vertexu

        @todo
        - kontrola na dulpicitu (2x zadany ten isty vertex)
        - kontrola na slucku - nesmie byt zadana poloha startovacieho vertexu

        @ endif
        '''
        vertex = Vertex(QPointF(x, y), self)
        self.diagram.addItem(vertex)

        self.vertexList.append(vertex)

        self.updateBoundingRect()

        return vertex

    def deleteVertex(self, vertex):
        '''
        @ Zmazanie vertexu.
        '''
        self.vertexList.remove(vertex)
        self.diagram.removeItem(vertex)

        self.updateBoundingRect()

        del vertex

    def insertVertex(self, index, x, y):
        '''
        @ Vytvori a vlozi novy vertex do zoznamu za aktualnu poziciu
        '''
        vertex = Vertex(QPointF(x, y), self)
        self.diagram.addItem(vertex)
        self.vertexList.insert(index, vertex)

        self.updateBoundingRect()

        return vertex

    def startPoint(self):
        '''
        @if English

        @endif

        @if Slovak

        Vrati polohu startovacieho bodu prepojenia.

        Poloha sa meni pri pohybe komponentu. Po kazdom pohybe komponentu
        treba obnovit polohu pociatocneho a koncoveho vertexu.

        @endif
        '''
         # relativna poloha terminalu v komponente
        pos = self.startComponent.terminal[self.startTerminal].position

         # vypocet absolutnej polohy terminalu vzhladom na plochu editora
        q = self.startComponent.mapToScene(pos)
        px = q.x()
        py = q.y()

        # update polohy vertexu pri zmene polohy terminalu
        self.vertexList[0].setPosition(QPointF(px, py))

        return (px, py)

    def endPoint(self):
        '''
        @if English

        @endif

        @if Slovak

        Vrati polohu koncoveho bodu prepojenia.

        Poloha sa meni pri pohybe komponentu. Po kazdom pohybe komponentu
        treba obnovit polohu pociatocneho a koncoveho vertexu.

        @endif
        '''
        pos = self.endComponent.terminal[self.endTerminal].position
        q = self.endComponent.mapToScene(pos)
        px = q.x()
        py = q.y()

        # update polohy vertexu
        self.vertexList[-1].setPosition(QPointF(px, py))

        return (px, py)


class VirtualNet():
    '''!
    @if English


    @endif

    @if Slovak

    Virtualne prepojenie medzi komponentami diagramu.

    Používa sa na štandardné prepojenie vnorených virtuálnych komponentov
    a pri prepojení v rámci bloku na spojenie termiálov bloku a portov diagramu bloku.

    @endif
    '''

    def __init__(self, comp1, term1, comp2, term2):

        self.netType = NET_VIRTUAL
        self.uid = 0
        self.name = ''                       # inicializuje sa menom siete len pri pouziti v bloku

        self.startTerminal = term1		# poradove cislo pociatocneho terminalu
        self.startComponent = comp1		# pripojeny pociatocny objekt
        comp1.terminal[term1].connect.append(self)

        self.endTerminal = term2		# poradove cislo koncoveho terminalu
        self.endComponent = comp2		# pripojeny koncovy objekt
        comp2.terminal[term2].connect.append(self)

    def setSelected(self, state):
        pass

    def __str__(self):
        '''
        '''
        s = ''
        s = s + '<VN>Net name : ' + str(self.name) + '\n'
        s = s + '    Net uid  : ' + str(self.uid) + '\n'
        s = s + '    Net type : ' + str(self.netType) + '\n'
        s = s + \
            '          Start : (comp uid ' + str(self.startComponent.uid) + ')' + \
                                   ' term[' + str(self.startTerminal) + ']' +       \
                                   ' typ:' + str(self.startComponent.terminal[self.startTerminal].termType) + '\n'
        s = s + \
            '          End   : (comp uid ' + str(self.endComponent.uid) + ')' + \
                                   'term [' + str(self.endTerminal) + ']' + \
                                   ' typ:' + str(self.endComponent.terminal[self.endTerminal].termType) + '\n'
        return s
