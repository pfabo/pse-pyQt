# -*- coding: utf-8 -*-

import logging
import time

import six

from componenttypes import *  # @UnusedWildImport
from diagram import MODE

if six.PY2:
    from PyQt4.QtCore import QThread
else:
    from PyQt5.QtCore import QThread


class SolverRungeKutt2(QThread):

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
        @if English

        Simulation start.

        @endif

        @if Slovak

        Spustenie simulacie.

        Spustenie simulacie podla metody RK2.
        @todo - doplnit ukoncenie slucky na zaklade externej udalosti (stav specialneho komponentu)

        @endif
        '''

        logging.info('Simulation RK2 start')

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
            # 2.1 nastavenie vystupov komponentov na zaciatku kroku
            for comp in simClock:  # hodiny a synchronizacia
                comp.sim(SIM_STEP, 0, self.time, self.step)

            for comp in simComp:  # linearne komponenty, prepocitanie a nastavenie vystupov
                comp.sim(SIM_STEP, 0, self.time, self.step)

                # @todo - optimalizacia ...
                self.simEngine.transferValue()

            #-----------------------------------------------------------
            # 3. nacitanie hodnoty siete k1=f(yk, tk)
            for comp in simIntegral:
                comp.contState[1] = comp.sim(SIM_DERIVE, 0, self.time, self.step)

            # 3.1 nastavenie hodnoty (yk+k1/2*step)
            # itegracia systemu do stabilneho stavu odozvy na zmenu vystupnych hodnot
            for j in range(10):

                for comp in simIntegral:
                    comp.sim(SIM_STEP, comp.contState[0] + comp.contState[1] / 2.0 * self.step, self.time + self.step / 2.0, self.step / 2.0)
                    comp.contState[3] = comp.sim(SIM_DERIVE, 0, self.time, self.step)

                for comp in simComp:
                    comp.sim(SIM_STEP, 0, self.time, self.step)

                self.simEngine.transferValue()

                # 3.2 urcenie hodnotu maximalnej chyby - kontrola ustaleneho
                # stavu
                err = 0.0
                for comp in simIntegral:
                    val = abs(comp.contState[3] - comp.sim(SIM_DERIVE, 0, self.time, self.step))
                    if val > err:
                        err = val

                if j > 0 and err < 0.001:            # kontrola chyby
                    break

            #-----------------------------------------------------------
            # 4. vypocet vyslednej hodnoty yk+1=yk+k2
            for comp in simIntegral:
                comp.contState[2] = comp.sim(SIM_DERIVE, 0, self.time, self.step)
                comp.contState[0] = comp.contState[0] + comp.contState[2] * self.step

            for j in range(10):

                for comp in simIntegral:            # prepocet vystupnych stavov vsetkych komponentov
                    comp.sim(SIM_STEP, comp.contState[0], self.time + self.step, self.step)
                    comp.contState[3] = comp.sim(SIM_DERIVE, 0, self.time, self.step)

                for comp in simComp:                # prepocet vystupnych stavov vsetkych komponentov
                    comp.sim(SIM_STEP, 0, self.time, self.step)

                self.simEngine.transferValue()      # presun hodnot

                err = 0.0                           # kontrola ustaleneho stavu
                for comp in simIntegral:
                    val = abs(comp.contState[3] - comp.sim(
                        SIM_DERIVE, 0, self.time, self.step))
                    if val > err:
                        err = val

                if j > 0 and err < 0.001:            # kontrola chyby
                    break

            for comp in simComp:  # linearne komponenty, prepocitanie a nastavenie vystupov
                comp.sim(SIM_UPDATE, 0, self.time, self.step)

            for comp in simDisc:  # diskretne komponenty
                comp.sim(SIM_UPDATE, 0, self.time, self.step)

            for comp in simControl:  # riadiace komponenty
                comp.sim(SIM_UPDATE, 0, self.time, self.step)

            # nasledujuci krok a kontrola na ukoncenie simulacie
            self.time = self.time + self.step
            if self.time > self.final:
                break

        self.stopTime = time.time()  # realny cas ukoncenia simulacie

        logging.info('Simulation RK2 finish %s', ' ')
        for comp in self.simEngine.simCompList:
            comp.sim(SIM_FINISH, 0, self.time, self.step)

        self.simEngine.diagram.update()

        td = self.stopTime - self.startTime
        ns = self.final / self.step

        ns = ns + 1

        logging.info('    total time [sec]     : %s', '{:.5f}'.format(td))
        logging.info('    step time  [sec]     : %s', '{:07.5f}'.format(td / ns))
        logging.info('    number of int. steps : %s', int(ns))

        self.simEngine.flagSimActive = False		# povolenie dalsej simulacie
        # povolenie editovania diagramu
        # todo - upravit cez metodu - zakaz a povolenie editovanie pre (vsetky) diagram(y) simulacie
        self.simEngine.diagram.mode = MODE.MOVE

        self.msleep(200)
