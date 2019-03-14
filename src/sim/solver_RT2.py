# -*- coding: utf-8 -*-

import time

import six

from componenttypes import *  # @UnusedWildImport
from diagram import MODE


if six.PY2:
    from PyQt4.QtCore import QThread
else:
    from PyQt5.QtCore import QThread


class SolverRealTime2(QThread):

    '''
    Runge Kutt 2 - solver, synchronizovany na realny cas.
    '''

    def __init__(self, simEngine):
        '''
        Nastavenie parametrov simulacie z objektu agregujucej triedy.
        '''
        QThread.__init__(self)

        self.simEngine = simEngine

        self.time = 0.0				# aktualny vas simulacie
        self.step = simEngine.step
        self.final = simEngine.final
        self.max_iter = simEngine.max_iter
        self.error = simEngine.error
        self.clock = simEngine.clock

        self.startTime = 0.0	        # (realny) cas startu simulacie
        self.stopTime = 0.0		        # (realny) cas ukoncenia simulacie

    def stop(self):
        '''
        Zastavenie simulacie - nastaveni casu ukoncenia na aktualny cas
        '''
        self.final = self.time

    def run(self):
        '''
        Spustenie simulacie podla metody RK2.
        TODO - doplnit ukoncenie slucky na zaklade externej udalosti
        '''

        print('>>> State SIMULATION REAL TIME RK2 - Start')

        # roztriedenie komponentov do zoznamov podla typov
        simComp = []		# zoznam spojitych komponentov
        simDisc = []		# zoznam diskretnych komponentov
        simClock = []		# zoznam hodinovych a synchronizovanych komponentov
        simIntegral = []  # zoznam integracnych komponentov

        # 1. triedenie do samostatnych zoznamov a inicializacia simulacnych komponentov
        #    pre integracne komponenty je doplneny vektor stavovych premennych
        # for comp in self.simEngine.diagram.componentList:
        for comp in self.simEngine.simCompList:
            if comp.compType == TYPE_SIM_DISCRETE:
                simDisc.append(comp)

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

        # self.simEngine.transferValue()
        # 1.1 nastavenie pociaticnych podmienok v case T=0.0
        #     pocet cyklov by mal byt rovny max. oneskoreniu elementu
        #     slucka inicializuje vnutorny buffer v komponentoch typu delay
        for q in range(8):
            #for comp in self.simEngine.diagram.componentList:
            for comp in self.simEngine.simCompList:
                comp.sim(SIM_INIT, 0, self.time, self.step)
            self.simEngine.transferValue()

        # 2. vlastna slucka simulacie
        self.startTime = time.time()  # realny cas spustenia simulacie
        while True:

            #-----------------------------------------------------------
            # 2.1 nastavenie vystupov komponentov na zaciatku kroku
            for comp in simClock:  # hodiny a synchronizacia
                comp.sim(SIM_STEP, 0, self.time, self.step)

            self.simEngine.transferValue()

            for comp in simDisc:  # diskretne komponenty
                comp.sim(SIM_STEP, 0, self.time, self.step)

            self.simEngine.transferValue()

            for comp in simComp:  # linearne komponenty, prepocitanie a nastavenie vystupov
                comp.sim(SIM_STEP, 0, self.time, self.step)

            self.simEngine.transferValue()
            #-----------------------------------------------------------
            # 3. nacitanie hodnoty siete k1=f(yk, tk)
            for comp in simIntegral:
                comp.contState[1] = comp.sim(
                    SIM_DERIVE, 0, self.time, self.step)

            # 3.1 nastavenie hodnoty (yk+k1/2*step)
            # itegracia systemu do stabilneho stavu odozvy na zmenu vystupnych
            # hodnot
            for j in range(10):

                for comp in simIntegral:
                    comp.sim(SIM_STEP, comp.contState[0] + comp.contState[
                             1] / 2.0 * self.step, self.time + self.step / 2.0, self.step / 2.0)
                    comp.contState[3] = comp.sim(
                        SIM_DERIVE, 0, self.time, self.step)

                for comp in simComp:
                    comp.sim(SIM_STEP, 0, self.time, self.step)

                self.simEngine.transferValue()

                # 3.2 urcenie hodnotu maximalnej chyby - kontrola ustaleneho
                # stavu
                err = 0.0
                for comp in simIntegral:
                    val = abs(comp.contState[3] - comp.sim(
                        SIM_DERIVE, 0, self.time, self.step))
                    if val > err:
                        err = val

                if j > 0 and err < 0.001:
                    break

            #-----------------------------------------------------------
            # 4. vypocet vyslednej hodnoty yk+1=yk+k2
            for comp in simIntegral:
                comp.contState[2] = comp.sim(
                    SIM_DERIVE, 0, self.time, self.step)
                comp.contState[0] = comp.contState[
                    0] + comp.contState[2] * self.step

            for j in range(10):

                for comp in simIntegral:		# prepocet vystupnych stavov vsetkych komponentov
                    comp.sim(SIM_STEP, comp.contState[
                             0], self.time + self.step, self.step)
                    comp.contState[3] = comp.sim(
                        SIM_DERIVE, 0, self.time, self.step)

                for comp in simComp:			# prepocet vystupnych stavov vsetkych komponentov
                    comp.sim(SIM_STEP, 0, self.time, self.step)

                self.simEngine.transferValue()  # presun hodnot

                err = 0.0							# kontrola ustaleneho stavu
                for comp in simIntegral:
                    val = abs(comp.contState[3] - comp.sim(
                        SIM_DERIVE, 0, self.time, self.step))
                    if val > err:
                        err = val

                if j > 0 and err < 0.001:
                    break

            #-----------------------------------------------------------
            # refresh vizualnych komponentov
            #-----------------------------------------------------------
            for comp in simComp:  # linearne komponenty
                comp.sim(SIM_UPDATE, 0, self.time, self.step)

            for comp in simDisc:  # diskretne komponenty
                comp.sim(SIM_UPDATE, 0, self.time, self.step)

            # nasledujuci krok a kontrola na ukoncenie simulacie
            self.time = self.time + self.step
            if self.time > self.final:
                break

            #-----------------------------------------------------------
            # synchronizacia na realny cas, cakanie na dalsi krok
            #-----------------------------------------------------------
            while True:
                self.simEngine.diagram.update()
                tstep = self.startTime + self.time  # +self.step
                tmact = time.time()
                if tmact >= tstep:
                    break
                self.msleep(int(self.step / 5. * 1000.))

        self.stopTime = time.time()  # realny cas ukoncenia simulacie

        print ('>>> State SIMULATION REAL TIME RK2 - Finish')

        for comp in self.simEngine.simCompList:
            comp.sim(SIM_FINISH, 0, self.time, self.step)

        td = self.stopTime - self.startTime
        ns = self.final / self.step

        print ('    Total time [sec]     :', '{:.5f}'.format(td))
        print ('    Step time  [sec]     :', '{:07.5f}'.format(td / ns))
        print ('    Number of int. steps :', int(ns))

        self.simEngine.flagSimActive = False		# povolenie dalsej simulacie
        # povolenie editovania diagramu
        # todo - upravit cez metodu - zakaz a povolenie editovanie pre (vsetky) diagram(y) simulacie
        self.simEngine.diagram.mode = MODE.MOVE

        self.msleep(200)
