# -*- coding: utf-8 -*-

#
# !!! UPRAVIT ITERACNU SCHEMU PODLA RK2 !!!
#

import six

from diagram import *
from component import *
from terminal import *
from scipy import *
import time

if six.PY2 is True:
    from PyQt4.QtCore import *


class Sim_RungeKutt_23(QThread):

    '''
    ODE23 - Solver, Konstantna dlzka kroku
    '''

    def __init__(self, simEngine):
        '''
        @if English

        @endif

        @if Slovak

        Nastavenie parametrov simulacie z objektu agregujucej triedy.

        @endif
        '''
        QThread.__init__(self)

        self.simEngine = simEngine

        self.time = 0.0                 # aktualny cas simulacie
        self.step = simEngine.step
        self.final = simEngine.final
        self.max_iter = simEngine.max_iter
        self.error = simEngine.error
        self.clock = simEngine.clock

        self.startTime = 0.0            # (realny) cas startu simulacie
        self.stopTime = 0.0             # (realny) cas ukoncenia simulacie
        self.start()                    # spustenie thread-u simulacie

    def stop(self):
        '''
        @if English

        Simulation stop.

        @endif

        @if Slovak

        Zastavenie simulacie.

        Zastavenie simulacie je pomocou nastavenia casu ukoncenia na aktualny cas.

        @endif
        '''
        self.final = self.time

    def run(self):
        '''
        Spustenie simulacie
        '''

        # roztriedenie komponentov do zoznamov podla typov
        simComp = []            # zoznam spojitych komponentov
        simDisc = []            # zoznam diskretnych komponentov
        simClock = []           # zoznam hodinovych a synchronizovanych komponentov
        simIntegral = []        # zoznam integracnych komponentov
        simControl = []         # zoznam riadiacich komponentov

        # 1. triedenie do samostatnych zoznamov a inicializacia simulacnych komponentov,
        #    pre integracne komponenty je doplneny vektor stavovych premennych

        # for comp in self.simEngine.diagram.componentList:
        for comp in self.simEngine.simCompList:
            if comp.compType == TYPE_SIM_DISCRETE:
                simDisc.append(comp)

            if comp.compType == TYPE_SIM_CONTROL:
                simControl.append(comp)

            if comp.compType == TYPE_SIM_CLOCK:
                simClock.append(comp)

            if comp.compType == TYPE_SIM_CONTINUOUS:
                simComp.append(comp)

            if comp.compType == TYPE_SIM_INTEGRAL:
                comp.contState = [0.0, 0.0, 0.0, 0.0]
                # parametre vektora stavovych premennych
                # [0] - yk, yk+1
                # [1] - k1
                # [2] - k2
                # [3] - in - aktualizovana hodnota vstupu
                simIntegral.append(comp)

        # 1.1 nastavenie pociatocnych podmienok v case T=0.0
        #     pocet cyklov by mal byt rovny max. oneskoreniu elementu
        #     slucka inicializuje vnutorne buffery v komponentoch typu delay
        # TODO - dlzka slucky podla max. dlzky oneskovacieho buffra
        # TODO - inicializacia/reset hodnot terminalov
        #for q in range(10):
        for comp in self.simEngine.simCompList:
            comp.sim(SIM_INIT, 0, self.time, self.step)

            self.simEngine.transferValue()

        # 2. hlavna slucka simulacie
        self.startTime = time.time()  # realny cas spustenia simulacie

        while True:
            #-----------------------------------------------------------
            # nastavenie vystupov diskretnych komponentov
            #-----------------------------------------------------------
            # q=int(self.time/self.step)
            # w=int(self.clock/self.step)
            # if (q % w) == 0:

            for c in simDisc:
                c.compute(SIM_OUTPUT, 0, self.time, self.step)

            self.sim.transferValue()

            #-----------------------------------------------------------
            # Runge-Kutt 23 metoda - jednokrokova iteracia
            # k1 = f(tn,yn)
            #-----------------------------------------------------------
            for c in simComp:
                c.contState[1] = c.compute(SIM_DERIVE)

            for j in range(10):
                # prepocet vystupnych stavov vsetkych komponentov
                for c in simComp:
                    c.compute(SIM_OUTPUT, c.contState[0] + c.contState[
                              1] * self.step / 2.0, self.time + self.step / 2.0)
                # presun hodnot
                self.sim.transferValue()
                # kontrola ustaleneho stavu
                err = 0.0
                for c in simComp:
                    val = abs(c.compute(SIM_ERROR) - c.compute(SIM_DERIVE))
                    if val > err:
                        err = val

                if j > 0 and err < 0.001:
                    break

            #-----------------------------------------------------------
            # k2 = f(tn+1/2*step, yn+1/2*step*k1)
            #-----------------------------------------------------------
            for c in simComp:
                c.contState[2] = c.compute(SIM_DERIVE)

            for j in range(10):
                for c in simComp:
                    c.compute(SIM_OUTPUT, c.contState[0] + c.contState[
                              2] * self.step * 3.0 / 4.0, self.time + self.step * 3.0 / 4.0)

                self.sim.transferValue()

                err = 0.0
                for c in simComp:
                    val = abs(c.compute(SIM_ERROR) - c.compute(SIM_DERIVE))
                    if val > err:
                        err = val

                if j > 0 and err < 0.001:
                    break

            #-----------------------------------------------------------
            # k3 = f(tn+3/4*step, yn+3/4*step*k1)
            #-----------------------------------------------------------
            for c in simComp:
                c.contState[3] = c.compute(SIM_DERIVE)
                c.contState[0] = c.contState[0] + (
                    2.0 / 9.0 * c.contState[1] + c.contState[2] / 3.0 + 4.0 / 9.0 * c.contState[3]) * self.step

            for j in range(10):
                for c in simComp:
                    c.compute(
                        SIM_OUTPUT, c.contState[0], self.time + self.step)

                self.sim.transferValue()

                err = 0.0
                for c in simComp:
                    val = abs(c.compute(SIM_ERROR) - c.compute(SIM_DERIVE))
                    if val > err:
                        err = val

                if j > 0 and err < 0.001:
                    break

            #-----------------------------------------------------------
            # nastavenie hodin pre diskretne komponenty
            #-----------------------------------------------------------
            for c in simClock:
                c.compute(SIM_OUTPUT, 0, self.time, self.step)

            self.sim.transferValue()

            #-----------------------------------------------------------
            # nastavenie vystupov diskretnych komponentov
            #-----------------------------------------------------------
            # q=int(self.time/self.step)
            # w=int(self.clock/self.step)
            # if (q % w) == 0:
            #	for c in simDisc:
            #		c.compute(SIM_OUTPUT, 0 , self.time, self.step)
            #
            # self.sim.transferValue()

            #-----------------------------------------------------------
            # nastvenie stavu nesimulovanych komponentov
            #-----------------------------------------------------------
            for c in simComp:
                c.compute(SIM_UPDATE, c.contState[0], self.time, self.step)

            self.time = self.time + self.step

            # kontrola na ukoncenie simulacie
            if self.time >= self.final:
                break

        self.stopTime = time.time()  # realny cas ukoncenia simulacie

        print ('>>> State SIMULATION RK2 - Finish')

        for comp in self.simEngine.simCompList:
            comp.sim(SIM_FINISH, 0, self.time, self.step)

        self.simEngine.diagram.update()

        td = self.stopTime - self.startTime
        ns = self.final / self.step

        ns = ns + 1

        print ('    Total time [sec]     :', '{:.5f}'.format(td))
        print ('    Step time  [sec]     :', '{:07.5f}'.format(td / ns))
        print ('    Number of int. steps :', int(ns))

        self.simEngine.flagSimActive = False		# povolenie dalsej simulacie
        # povolenie editovania diagramu
        # todo - upravit cez metodu - zakaz a povolenie editovanie pre (vsetky) diagram(y) simulacie
        self.simEngine.diagram.mode = MODE.MOVE

        self.msleep(200)
