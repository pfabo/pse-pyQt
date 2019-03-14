# -*- coding: utf-8 -*-
import  six

from componenttypes import TYPE_CONN_VIRTUAL, TYPE_SIM_AGREGAT, TYPE_NET_TERM, \
    TYPE_SIM_CONTROL
from connection import VirtualConnection
from diagram import MODE
from net import Net, NET_VIRTUAL
from sim.solver_RK2 import SolverRungeKutt2
from sim.solver_RT2 import SolverRealTime2
from terminal import TERM


if six.PY2:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import QRectF, QPointF, Qt, QPoint, QThread
    from PyQt4.QtSvg import QSvgWidget
else:
    from PyQt5.QtSvg import QSvgWidget
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *


#from copy import *
# Typy simulatorov a generatorov
SIM_SOLVER_RK2 = 1  # jednokrokovy solver Runge Kutt 2
SIM_SOLVER_RK23 = 2  # jednokrokovy solever RungeKutt 23
SIM_SOLVER_RT2 = 3  # solver RK2 synchronizovany na realny cas
SIM_SPICE = 10
SIM_MODELICA = 11


class SimulatorEngine():
    '''
    Trieda logickych prepojeni medzi komponentami.
    Kontroluje prepojenia v diagrame.
    Vytvara strom prepojeni vystup->vstupu a transformuje infomacie medzi blokmi.

    @todo - uprava algoritmu spravy virtualnych prepojeni
            Pri kontrole prepojeni sa vytvaraju pomocne prepojovacie komponenty a virtualne
            spoje medzi komponentami NetTerm, aktulne sa kontroluju a mazu pred kazdou simulaciou.
            Uprava algoritmu - doplnit metodu, ktora zmaze vsetky pomocne spoje a prepojenia
            po ukonceni simulacie zo zoznamov simNetList a simCompList
    '''

    def __init__(self, diagram):
        '''
        '''
        self.diagram = diagram
        self.wiredNets = []                # zoznam prepojeni terminalov

        self.simNetList = []               # lokalne zoznamy pouzite pre simulaciu
        self.simCompList = []              # obsahuju kopie zoznamu z diagramu a virtualnych komponentov

        self.flagSimActive = False         # priznak spustenej simulacie

        # default parametre simulacie
        self.step = 0.001                  # krok casoveho rozlisenia
        self.final = 10                    # ukoncenie simulacie
        self.max_iter = 100                # max. pocet iteracii v jednom kroku
        self.error = 1e-3

        self.clock = 0.01                  # hodiny pre diskretne komponenty
        self.update = 0.25                 # interval update vizualnych komponentov

        self.thread = None

        self.recursiveCount = 0            # aktualna hlbka rekurzia pri kontrole
                                           # prepojeni

    def checkNetwork(self):
        '''
        Kontrola prepojeni a vygenerovanie zoznamu vystupny terminal -> vstupne terminaly.

        '''
        # @todo - uprava algoritmu spravy virtualnych prepojeni
        #         Odstranenie vsetkych pomocnych prvkov simulacie - virtualnych
        #         net-ov medzi prepojovacimi portami a virtualnych objektov prepojenia,
        #         ktore boli vytvarane v predchadzajucej simulacii
        tempList = []
        for comp in self.diagram.componentList:
            if comp.compType == TYPE_CONN_VIRTUAL:
                tempList.append(comp)

        for q in tempList:
            self.diagram.deleteComponentWithNets(q)

        #print(' *** CLEAN *** ')
        # @todo upravit mazanie virtualnych sieti tak, aby sa vyhodili ich referencie z terminalu
        for comp in self.diagram.componentList:
            k = comp.terminal.keys()
            for term in k:  # comp.terminal:
                for net in comp.terminal[term].connect:
                    if net.netType == NET_VIRTUAL:
                        # print('delete VN ', net)
                        self.diagram.deleteNet(net)

        #print(' *** CLEAN END *** ')

        #----------------------------------------------
        # A1. Kopie zoznamov komponentov a prepojeni z vnutornych diagramov virtualnych
        #     komponentov a blokov do lokalnych simulacnych zoznamov

        self.wiredNets = []        # inicializacia lokalnych zoznamov
        self.simCompList = []
        self.simNetList = []

        # inicializacia z primarneho diagramu
        self.simCompList = self.diagram.componentList
        self.simNetList = self.diagram.netList

        # zlucenie struktury virtualnych diagramov z agregovanych komponentov
        # diagramov z bokov do lokalnych zoznamov simulatora
        for comp in self.diagram.componentList:
            if comp.compType == TYPE_SIM_AGREGAT:
                # reset blokovych komponentu, inicilizacia prepojeni
                # k zmene vnutornej struktury bloku mohlo dojst aj editovanim bloku
                # v inom okne programu
                #comp.updateShape()
                comp.loadDiagram()
                self.simCompList = self.simCompList + comp.componentList
                self.simNetList = self.simNetList + comp.netList

        # A2. vytvorenie virtualnych komponentov pre prepojenie sieti, maju rovnaku funkciu ako
        #     objekty Junction, ale bez vykreslenia
        #     spajaju sa vsetky objektu s rovnakym menom siete

        # slovnik vsetkych prepojeni podla mena prepojovacich terminalov
        # meno:zoznam vsetkych prepojeni priradenych k danemu menu
        dictConn = {}

        # vyhladanie vsetkych portov - prepojovacich komponentov siete
        for comp in self.simCompList:
            if (comp.compType == TYPE_NET_TERM):
                #  or (comp.compType == TYPE_BLOCK_TERM):
                # meno terminalu
                # TODO - kontrola existencie kluca 'Port', chybove hlasenie
                name = comp.parameter['Port'].value

                # zaradenie terminalu siete do slovnika spolocnych prepojeni
                # ak kluc existuje, pridanie k existujucemu zoznamu
                if (name in dictConn) is True:

                    dictConn[name].append(comp)
                else:
                    # inak vytvorenie noveho kluca
                    dictConn[name] = [comp]

        # A3. Vytvorenie virtualnych prepojovacich spojov podla nacitaneho zoznamu
        #     prepojeni dictConn
        for key in dictConn:
            # vytorenie virtualneho prepojovacieho bodu a nastavenie parametrov
            connComp = VirtualConnection()
            self.diagram.compCounter = self.diagram.compCounter + 1
            connComp.uid = self.diagram.compCounter
            connComp.parameter['Ref'].value = connComp.parameter['Ref'].value + str(connComp.uid)

            # zaradenie prepojovacieho komponentu do zoznamu
            self.simCompList.append(connComp)

            # @todo - uprava algoritmu spravy virtualnych prepojeni
            #         zaradenie virtualneho komponentu do standardneho zoznamu komponentov
            #         pre jeho bezpecne odstranenie pred dalsou simulaciou
            # ???? self.diagram.componentList.append(connComp)

            # vytvorenie prepojeni medzi virtualnym bodom a terminalmi siete
            # prepojenie je bez vertexov - nezobrazuje sa
            # todo - pouzit virtualne prepojenie
            for connEnd in dictConn[key]:          # iteracia po zozname komponentov patriacich do rovnakeho prepojenia
                vnet = Net(self.diagram)
                vnet.netType = NET_VIRTUAL

                vnet.startTerminal = 1            # poradove cislo pociatocneho terminalu
                vnet.startComponent = connComp    # pripojeny pociatocny objekt

                vnet.endTerminal = 1              # poradove cislo koncoveho terminalu
                vnet.endComponent = connEnd       # pripojeny koncovy objekt

                self.simNetList.append(vnet)

                # @todo - uprava algoritmu spravy virtualnych prepojeni
                #         zaradenie virtualneho prepojenia do standardneho zoznamu prepojeni
                #         pre jeho bezpecne odstranenie pred dalsou simulaciou

                # ??? upravit mazanie CLEAN tak, aby nepouzivalo netList
                self.diagram.netList.append(vnet)

                vnet.endComponent.terminal[1].connect.append(vnet)
                vnet.startComponent.terminal[1].connect.append(vnet)

        # A4. TODO - kontrola siete ukoncene len jednym terminalon

        # A5. Kontrola expandovaneho diagramu, vypis pred kontrolou prepojeni
        #print(' START=================================================')
        #print(' Components ...........................................')
        #for c in self.simCompList:
        #    print(c)
        #print(' Nets .................................................')
        #for n in self.simNetList:
        #    print(n)
        #print(' ===================================================END')

        # B. Finalna kontrola prepojenia
        # B1. na jednej sieti moze byt len jeden vystupny terminal a aspon jeden vstupny terminal
        # B2. vytvorenie zoznamu prepojenni - vystup -> vstupy
        # for n in self.diagram.netList:

        for n in self.simNetList:

            self.recursiveCount = 0

            sTerm = n.startComponent.terminal[n.startTerminal]
            eTerm = n.endComponent.terminal[n.endTerminal]

            outTerm = None
            self.tempTerm = []

            # prehladavame len tie siete, ktore maju jeden z terminalov vystupny
            # zahrna to aj vystupne terminaly s viacerymi pripojenia
            if sTerm.termType == TERM.OUT:
                outTerm = sTerm
                retVal = self.parseWire(n, eTerm)
                if retVal is False:
                    print('>>> Error - Simulator.checkNetwork (1):')
                    print('    ', n.startComponent.className, n.startComponent.parameter['Ref'].value)
                    print('    ', n.endComponent.className, n.endComponent.parameter['Ref'].value)
                    return False

            elif eTerm.termType == TERM.OUT:
                outTerm = eTerm
                retVal = self.parseWire(n, sTerm)
                if retVal is False:
                    print('>>> Error - Simulator.checkNetwork (2):')
                    print(n.startComponent.className, n.startComponent.parameter['Ref'].value)
                    print(n.endComponent.className, n.endComponent.parameter['Ref'].value)
                    return False

            if outTerm is not  None:
                self.wiredNets.append((outTerm, self.tempTerm))

        return True

    def parseWire(self, net, term):
        '''
        Rekurzivne prehladanie prepojeni, vygenerovanie zoznamu vstupnych terminalov.
        Funkcia vrati True, ak siet obsahuje jeden vystupny terminal a n vstupnych
        terminalov.
        Ak siet obsahuje niekolko vystupnych terminalov, funkcia vrati False
        a oznaci chybnu siet.
        '''
        retVal = False

        self.recursiveCount = self.recursiveCount + 1
        if self.recursiveCount > 100:
            net.isSelected(True)
            print('>>> ERROR SimulatorEngine.parseWire:')
            print('    Loop in net', net.name)
            return False

        if term.termType == TERM.IN:            # najdeny koncovy terminal typu IN
            self.tempTerm.append(term)          # zaradenie do zoznamu vymen
            return True

        elif term.termType == TERM.OUT:            # najdeny koncovy terminal typu OUT
            net.setSelected(True)                # oznacenie chybnej siete
            print('>>> ERROR SimulatorEngine.parseWire:')
            print('    Dva terminaly typu OUT na jednej sieti')
            print(net)
            return False                      # chyba - siet obsahuje dva terminaly OUT

        elif term.termType == TERM.CONN:        # najdeny terminal CONN, rekurzivne hladanie
            # zaradenie prepojovacieho terminalu (ako IN-terminal)
            # do zoznamu vymen - pre riadenie sirky zbernice a pod.
            self.tempTerm.append(term)

            # zoznam netov pripojenych k prepojovaciemu terminalu
            net_list = term.connect
            for n in net_list:
                # prehladanie podla koncovych terminalov sieti pripojenych k
                # CONN
                if n == net:
                    pass
                else:
                    sT = n.startComponent.terminal[n.startTerminal]
                    eT = n.endComponent.terminal[n.endTerminal]
                    # rekurzivne prehladanie dalsich vetiev pripojenych k CONN
                    # vyber 'druheho' konca siete, terminal, z ktoreho vychadzame
                    # moze byt pre niektore siete vstupny a/alebo vystupny
                    if term == sT:
                        retVal = self.parseWire(n, eT)
                    else:
                        retVal = self.parseWire(n, sT)

            return retVal

        print('ERROR in parseWire - neznamy typ terminalu')
        print('Vstupne parametre net, term :')
        print(net)
        print(term)
        return False

    def stopSimulation(self):
        '''
        '''
        if self.thread is not None:
            self.thread.stop()

    def startSimulation(self):
        '''
        Spustenie simulacneho threadu.

        Spustenie simulacie pozostava z:
                - kontroly prepojeni medzi komponentami
                - vyhladanie komponentu s parametrami simulacie
                  a inicializacia similacnych parametrov
                - vytvorenie simulacneho objektu a jeho spustenie

        @todo:
                - zablokovanie uprav komponentov editora pocas simulacie.
                - zabranenie viaceremu spusteniu simulatorov
                - chybove vystupy do samostatneho okna s upozornenim
        '''
        if self.checkNetwork() is False:
            print('>>> ERROR <<<')
            print('    Chyba v prepojeni medzi komponentami')
            return

        # vyhladanie riadiaceho komponentu

        if not self.flagSimActive:
            foundControl = False
            for c in self.diagram.componentList:
                if c.compType == TYPE_SIM_CONTROL:
                    foundControl = True
                    if c.solver == SIM_SOLVER_RK2:
                        self.step = c.parameter['Step'].value
                        self.final = c.parameter['Stop Time'].value
                        c.engine = self
                        self.thread = SolverRungeKutt2(self)

                    elif c.solver == SIM_SOLVER_RT2:
                        self.step = c.parameter['Step'].value
                        self.final = c.parameter['Stop Time'].value
                        c.engine = self
                        if self.final == -1:
                            self.final = 1e10
                        self.thread = SolverRealTime2(self)
                    else:
                        raise ValueError(c.solver)

                    # spustenie thread-u simulacie
                    self.thread.start()

            if not foundControl:
                print('>>> Simulation Error')
                print('    Missing control component in diagram (RK2, RK23 ..)')

                # prepnutie do editovacieho modu, povolenie editovania a presuvania komponentov
                self.diagram.mode = MODE.MOVE
                return

            self.flagSimActive = True
        else:
            print('>>> Simulation in progress')
            print('    Stop simulation ')
            return

    def setStep(self, step):
        '''
        Uprava parametru simulacie.
        '''
        if self.thread is not None:
            self.thread.step = step

    def setStopTime(self, final):
        '''
        Uprava parametru simulacie
        '''
        if self.thread is not None:
            self.thread.final = final

    def transferValue(self):
        '''
        Kopia hodnoty vystupneho terminalu do vsetkych vstupnych terminalov netu.
        '''
        for i in self.wiredNets:
            value = i[0].value
            for j in i[1]:
                j.value = value
