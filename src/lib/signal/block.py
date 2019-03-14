# -*- coding: utf-8 -*-
import json
import os

from component import Component, PARAM
from componenttypes import TYPE_SIM_AGREGAT, TYPE_NET_TERM, TYPE_BLOCK_TERM
from net import VirtualNet
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM, TEXT
from connection import Connection  # @UnusedImport needed for diagram in block


class Block(Component):
    """!
    @if English

    @endif

    @if Slovak

    \brief <H3><B>Block - Externý diagram</B></H3>

    Komponent agregujúci externý diagram, mená terminálov musia korešpondovať s vnútornými portami
    externého diagramu. Diagram je expandovaný v simulácii ako makro.

    Postup pri vytváraní bloku:

    1. Diagram sa načíta zo štandardného súboru *.pse, diagram musí obsahovať prepojovacie
       porty, ktorých mená budú korešpondovať s menami terminálov bloku.
       Komponenty a nety diagramu sa zaraďujú do vnútorných zoznamov bloku, nepridávajú sa do grafického
       sub-systému, grafická časť komponentov sa neupdatuje.

    2. Referencie komponentov sú upravené na tvar <ref bloku>_<ref komp>
       uid komponentov su upravene na tvar <uid bloku> * 10000 + <uid komp>,
       mena net-ov su upravené na tvar <ref bloku>_<meno net>

    3. Vytvorenie prepojení medzi terminálmi komponentu a portami diagramu,
       prepojenia maju meno <ref bloku>_<cislo terminalu> <meno portu>

    @todo - vymazanie virtualnych prepojeni pred nahratím bloku, zoatanú v diagrame po skončení simulácie
            úprave bloku a jeho následnom uložení.
            Dočasná úprava - ignorovanie virtuálnych spojov pri nahratí bloku

    <B><I>Parametre komponentu</I></B>

    <I>Inputs</I>

    Zoznam mien vstupných terminálov bloku.

    <I>Outputs</I>

    Zoznam mien výstupných terminálob bloku.

    <I>Diagram</I>

    Meno externého diagramu.

    <I>Icon</I>

    Ikona bloku.


    @todo automaticke vygenerovanie zoznamu vstupnycha vystupnych terminalov bloku pri zadani mena bloku
          podla komponentov TYPE_NET_TERM

    @todo kontrola integrity bloku, zhoda medzi menami terminalov a vnutornymi portami bloku,
          nepripojene terminaly ...

    @endif
    """

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.componentList = []		   # lokalny zoznam komponentov bloku
        self.netList = []		            # lokalny zoznam prepojeni bloku

        self.compType = TYPE_SIM_AGREGAT

        self.compCounter = self.uid * 1000      # lokalny counter odvodeny od UID komponentu
        self.netCounter = self.uid * 1000       # pouzivaju sa pre UID dodatocne vytvaranych
                                                # komponentov a prepojeni

        self.box = QRectF(-10, -15, 20, 50)

        # uprava referencie bloku - standardne v tvare Bxx
        self.parameter['Ref'].value = 'B'

        self.addParameter('Inputs', 'A, B')
        self.addParameter('Outputs', 'X')
        self.addParameter('Diagram', '', paramType=PARAM.FILE)
        self.addParameter('Icon', '', paramType=PARAM.IMAGE)

        # premenne pouzivane pri kontrole zmeny konfiguracie bloku
        self.numInputs = 0                       # pocet vstupnych terminalov
        self.numOutputs = 0                      # pocet vystupnych terminalov
        self.inputs = ''                         # retazec s popisom vstupov
        self.outputs = ''                        # retazec s popisom vystupov

    def drawShape(self, gc):

        n = self.numOutputs
        if self.numInputs >= self.numOutputs:
            n = self.numInputs

        if (n % 2) == 0:  # kontrola parne/neparne cislo
            y = (n // 2) * 20 - 10
        else:
            y = (n // 2) * 20

        gc.drawRoundedRect(-35, -y - 10, 70, 2 * y + 20, 5, 5)

        self.box = QRectF(-35 - 5, -y - 10 - 5, 80, 2 * y + 20 + 10)

        if self.svg is not None:
            # uprava zobrazenia, priesvitne pozadie ikony
            pal = QPalette(self.svg.palette()) 	             # kopia existujucej palety
            pal.setColor(QPalette.Window, QColor(Qt.transparent))   # nastavenie farby - vyber podla vlastnosti
            self.svg.setPalette(pal)

            size = self.svg.sizeHint()
            w = size.width()
            h = size.height()
            self.svg.render(gc, targetOffset=QPoint(-w / 2, -h / 2))

    def updateShape(self):
        """!
        @if English

        @endif

        @if Slovak

        1. Kontrola zmeny konfiguracie bloku, v pripade zmeny sa vytvori novy zoznam
           terminalov a zoznamy vstupov a vystupov bloku
           Zmena poctu terminalov sa moze robit len v pripade, ak su vsetky terminaly odpojene.
           Vsetku terminaly bloku su typu TERM.CONN bez ohladu na to, ci su vstupne
           alebo vystupne, pretoze sluzia na prepojenie medzi vnutornymi portami digramu
           bloku a vonkajsimi komponentami.

        2. Nacitanie vnutornej struktury bloku a prepojenie medzi terminalmi bloku a
           portami diagramu.

        @endif
        """

        # update ikony
        super(Block, self).updateShape()

        # 1. nacitanie zoznamov vstupnych terminalov
        inString = self.parameter['Inputs'].value
        outString = self.parameter['Outputs'].value

        # 1.1 Odpojenie vsetkych vnutornych prepojeni od terminalov
        #     @todo optinalizovat, brute force algoritmus
        for t in self.terminal:
            for n in self.netList:    # zoznam LOKALNYCH prepojenie v bloku
                if n in self.terminal[t].connect:
                    self.terminal[t].connect.remove(n)

        # 1.2 kontrola zhody zoznamu terminalov so zoznamom v parametroch
        if (self.inputs != inString) or (self.outputs != outString):
            # reinicializacia predchadzajuceho stavu
            self.inputs = inString
            self.outputs = outString

            # 1.3 kontrola pripojenia terminalov
            #     je mozne modifikovat len blok, ktory ma odpojenen terminaly
            #     @todo doplnit pre moznost zmeny konfiguracie pripojeneho bloku

            t = self.terminal.keys()
            for k in t:
                if self.terminal[k].connect != []:
                    print (">>> WARNING: Block", self.parameter['Ref'].value)
                    print ("    Block with connected terminal(s)")
                    print ("    Disconnect all block terminals before configuration change")
                    return

            # 1.4 zmazanie a vytvorenie novych terminalov bloku
            self.terminal = {}

            # nacitanie a parsovanie zoznamu vstupnych terminalov
            inString = inString.replace(' ', '')
            inArr = inString.split(',')
            self.numInputs = len(inArr)

            # vypocet polohy
            y = 0
            if (self.numInputs % 2) == 0:  # kontrola parne/neparne cislo
                y = -(self.numInputs // 2) * 20 + 10
            else:
                y = -(self.numInputs // 2) * 20

            # generovanie terminalov, definovanie vlastnosti a popisu
            for i in range(self.numInputs):
                term_in = self.addTerminal(inArr[i], (i + 1), TERM.CONN, QPointF(-40, y), TERM.DIR_EAST, TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
                term_in.termNameShow = True
                term_in.posName = QPoint(7, 5)
                y = y + 20

            # nacitanie a parsovanie zoznamu vystupnych terminalov
            outString = outString.replace(' ', '')
            outArr = outString.split(',')
            self.numOutputs = len(outArr)

            # vypocet polohy
            y = 0
            if (self.numOutputs % 2) == 0:  # kontrola parne/neparne cislo
                y = -(self.numOutputs // 2) * 20 + 10
            else:
                y = -(self.numOutputs // 2) * 20

            # generovanie terminalov, definovanie vlastnosti a popisu
            for i in range(self.numOutputs):
                term_out = self.addTerminal(outArr[i], (i + 100), TERM.CONN, QPointF(40, y), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
                term_out.termNameShow = True
                term_out.posName = QPoint(-7, 5)
                term_out.termNameAlign = TEXT.RIGHT
                y = y + 20

        # 3. nacitanie ikony - ak je definovana
        path = self.parameter['Icon'].value
        if os.path.exists(path):
            self.svg = QSvgWidget(path)
        else:
            self.svg = None

    def loadDiagram(self):
        '''
        Blok sa nacita pred simulaciou
        '''

        # 2. Nacitanie vnutornej struktury bloku
        #    Terminaly su odpojene v kroku 1.1

        # 2.1 Vynulovanie lokalnych zoznamov komponentov a prepojeni
        #     zmazanie vsetkych prepojeni (podla self.netList) od terminalov bloku do vnutornej struktury bloku
        #     prepojenia terminalov zvonka bloku sa nemenia
        #print('--------- Clean block ...')
        for t in self.terminal:
            for n in self.netList:    # zoznam LOKALNYCH prepojenie v bloku
                if n in self.terminal[t].connect:
                    #print('Clean net ', n)
                    self.terminal[t].connect.remove(n)
        #print('---------- hotovo ...')

        self.componentList = []
        self.netList = []

        # 2.2 Nacitanie bloku a vytvorenie struktury prepojeni - vnutorneho bloku a prepojeni k terminalom
        self.loadBlock()

        # 2.3 Zaradenie agregovanych komponentov
        for comp in self.componentList:
            if comp.compType == TYPE_SIM_AGREGAT:
                #comp.uid = comp.uid * 10
                # inicilizacia prepojeni, expanzia dalsich vnorenych blokov
                self.componentList = self.componentList + comp.componentList
                self.netList = self.netList + comp.netList

        # 3. nacitanie ikony - ak je definovana
        # path = self.parameter['Icon'].value
        #if os.path.exists(path):
        #    self.svg = QSvgWidget(path)
        #else:
        #    self.svg = None

    def addComponent(self, compClassName):
        '''!
        @if English

        @endif

        @if Slovak

        Vytvorenie noveho komponentu na zaklade mena triedy
        a zaradi ho do lokalneho zoznamu komponentov bloku.

        @endif
        '''

        # doplnenie pre PYTHON 2 - compClassName je typu QString, konverzia na str
        compClassName = str(compClassName)

        # constructor = globals()[compClassName]
        import lib
        try:
            constructor = getattr(lib, compClassName)
        except AttributeError:
            constructor = globals()[compClassName]
        component = constructor(compClassName, QPoint(0, 0))

        self.compCounter = self.compCounter + 1

        # inicializacia a uprava parametrov komponentu, komponenty sa nesobrazuju
        component.diagram = None
        self.componentList.append(component)
        return component

    def jsonImport(self, dct):
        return dct

    def loadBlock(self):
        '''!
        @if English

        @endif

        @if Slovak

        Nacitanie objektov a prepojeni zo suboru bloku.

        Nacitanie a vytvorenie komponentov a prepojeni zo suboru bloku.
        Vytorenie novych vnutornych komponentov a prepojeni medzi terminalmi
        komponentu a vnutornymi sietovymi terminalmi bloku.

        @endif
        '''

        fileName = self.parameter['Diagram'].value

        if os.path.isfile(fileName) is not True:
            return

        # 1. Kontrola mena suboru, existencia diagramu
        try:
            s = ''
            with open(fileName, 'r') as input_file:
                s = input_file.readlines()
        except:
            print('>>> ERROR Block.loadBlock, Ref =' + self.parameter['Ref'].value)
            print('    Chyba pri otvarani suboru bloku ' + fileName)
            return

        try:
            # 2. Nacitanie diagramu zo standardneho suboru *.pse
            readData = json.loads(s[0], object_hook=self.jsonImport)
            cList = readData[2]        # nacitany textovy zoznam komponentov
            nList = readData[3]        # nacitany textovy zoznam prepojeni
        except:
            print('>>> ERROR Block.loadBlock, Ref =' + self.parameter['Ref'].value)
            print('    Chyba vo formate suboru ' + fileName)
            return

        # 3. Vytvorenie komponentov z nacitaneho zoznamu
        # docasny slovnik priradenia uid a refrencie na objekt, potrebnu pri inicializacii
        # prepojenia terminalov, toto je ulozene len v parametroch kazdeho Net-u
        compDict = {}

        for data in cList:
            #print('compList = ',data)
            comp_uid = data[0]
            className = data[1]
            paramDict = data[3]

            # vytvorenie noveho komponentu
            comp = self.addComponent(className)

            # inicializacia hodnot parametrov komponentov
            for k in paramDict.keys():
                pdata = paramDict[k]
                value = pdata[1]
                comp.parameter[k].value = value

            # uprava referencie komponentu a inicializacia vnutornej struktury
            # komponentu na zaklade hodnot parametrov (updateShape)
            comp.parameter['Ref'].value = self.parameter['Ref'].value + '_' + comp.parameter['Ref'].value
            comp.uid = self.uid * 1000 + comp_uid
            comp.updateShape()
            # v pripade vnoreneho bloku - vytvorenie a prepojenie vnutornej struktury
            if comp.compType == TYPE_SIM_AGREGAT:
                comp.loadDiagram()
            compDict[comp.uid] = comp

        # 4. Vytvorenie prepojeni z nacitaneho zoznamu
        for data in nList:
            netType = data[2]
            # ignorovane stare virtualne prepojenia v bloku
            if netType == 1:
                netName = data[1]
                startTerminal = data[4]
                startComponent_uid = self.uid * 1000 + data[5]
                endTerminal = data[6]
                endComponent_uid = self.uid * 1000 + data[7]

                try:
                    # referencia na pociatocny a koncovy komponent siete - vyber zo slovnika komponentov
                    startComponent = compDict[startComponent_uid]
                    endComponent = compDict[endComponent_uid]

                    # vytvorenie prepojenia medzi komponentami
                    net = VirtualNet(startComponent, startTerminal, endComponent, endTerminal)

                    net.uid = self.netCounter
                    net.name = self.parameter['Ref'].value + '_' + netName
                    self.netCounter = self.netCounter + 1

                    self.netList.append(net)
                except:
                    print('>>> WARNING Block.loadBlock Ref =' + self.parameter['Ref'].value)
                    print('    Ignorovane chybne prepojenie v diagrame, type=1 standard, type=2 virtual')
                    print('    net name, type       ', data[1], data[2])
                    print('    start comp , terminal', data[5], data[4])
                    print('    end comp , terminal  ', data[7], data[6])

        # 5. Vytvorenie prepojeni medzi terminalmi a vnutornymi portami bloku
        #    iteracia cez zoznam terminalov bloku, vyhladanie vnutornych sietovych terminalov
        #    so zhodnym menom,
        #    @todo - metoda typu brute force, optimalizovat
        for tNum in self.terminal:
            termName = self.terminal[tNum].name

            # pre kazdy terminal hladame zhodu v komponentoch typu NetTerm
            # typ terminalu, ktoreho meno portu sa zhoduje s menom terminalu bloku
            # bude zmeneny na TYPE_BLOCK_TERM
            for c in self.componentList:
                if c.compType == TYPE_NET_TERM:
                    portName = c.parameter['Port'].value        # meno vnutorneho portu
                    #print('loadBlock - Port', portName)
                    if termName == portName:
                        # zhoda, k terminalu bloku existuje vnutorny port so zhodnym menom
                        # zmena typu sietoveho terminalu na prepojenie, zabrani generovaniu prepojeni
                        # pri inicializacii simulacie

                        c.compType = TYPE_BLOCK_TERM

                        # vytvorenie prepojenia medzi terminalom bloku a vnutornym portom
                        # meno prepojovacieho netu ma tvar
                        # <ref bloku> _ <cislo terminalu> <meno portu>
                        net = VirtualNet(self, tNum, c, 1)
                        net.name = self.parameter['Ref'].value + '_' + str(tNum) + portName
                        net.uid = self.netCounter
                        self.netList.append(net)
                        self.netCounter = self.netCounter + 1
                        break

        # 6. Mena portov komponentov NetTerm, ktore nie su prepojene s terminalmi bloku budu premenovane,
        #    pre zabranenie kolizie so zhodnymi menami portov v inych blokoch -> namespace makra
        for c in self.componentList:
            if c.compType == TYPE_NET_TERM:
                c.parameter['Port'].value = self.parameter['Ref'].value + '_' + c.parameter['Port'].value
