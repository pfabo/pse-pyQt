# -*- coding: utf-8 -*-

from component import Component
from terminal import TERM as term
from color import Color
import time

from lib.external.vxi11 import vxi11
from lib.control.rk2 import *


class ScopeRigol(Component):
    '''
    @if English

    @endif

    @if Slovak

    Nacitanie dat z osciloskopu RIGOL DS6000.

    Komponent má vlastnosti riadiaceho komponentu, podľa parametrov nastavenie osciloskopu určuje krok a čas
    ukončenia simulácie.

    Dátovy blok z osciloskopu sa načíta pri inicializácii simulácie a je konvertovaný na sekvenčný zdroj dát.
    Stav čítania dát z osciloskopu je indikovaný farbou komponentu (žltá-čítanie, červená-chyba, modrá-ok)

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.shapeImage = 'scope_3.svg'
        self.compType = TYPE_SIM_CONTROL
        self.shapeColor = Color.black
        self.shapeFillColor = Color.mediumAquamarine
        self.box = QRectF(-40, -40, 80, 80)

        ta = self.addTerminal('C1', 1, TERM.OUT, QPointF(40, -10), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        ta.termNameShow = True
        ta.posName = QPoint(-7, 5)
        ta.termNameAlign = TEXT_RIGHT

        tb = self.addTerminal('C2', 2, TERM.OUT, QPointF(40, 10), TERM.DIR_EAST, TERM.OUT_ARROW_SMALL_FILL, TERM.OUT_ARROW_SMALL)
        tb.termNameShow = True
        tb.posName = QPoint(-7, 5)
        tb.termNameAlign = TEXT_RIGHT

        self.addParameter('IP', '192.168.1.15')                  # IP adresa zariadenia
        self.addParameter('Step', 1e-6, visibleName=True)        # informacne parametre - nepouzite v simulacii
        self.addParameter('Stop Time', 1.0, visibleName=True)    # hodnoty sa nastavuju podla parametrov osciloskopu

        self.flag_data_read = False            # priznak nacitania dat pri inicializacii, zabrani opakovanemu citaniu
        self.flag_scope_ready = False          # priznak pripojeneho a inicializovaneho osciloskopu
        #self.flag_control = False              # priznak vytvoreneho virtualneho riadiaceho komponentu
        self.data_ch1 = []                     # datove bloky pre kanaly osciloskopu
        self.data_ch2 = []
        self.data_length = 0                   # dlzka datoveho bloku
        self.data_counter = 0                  # inkrementalny citac pre citanie dat z blokov
        self.sample_rate = 1e6
        self.step = 1.0 / self.sample_rate
        self.buff_size = 7000                  # pozadovana dlzka dat v osciloskope

        self.engine = None                     # referencia na simulator, inicializuje sa na zaciatku simulacie
                                               # v SimulatorEngine:startSimulation, umoznuje modifikaciu parametrov simulacie pocas behu
        self.solver = SIM_SOLVER_RK2

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, self.shapeFillColor)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-35, -35, 70, 70, 5, 5)

        self.drawIcon(gc, -30, -20)

    def sim(self, flag, value, tm, step):

        if flag == SIM_INIT:
            self.data_ch1 = []       # vynulovanie datovych buffrov
            self.data_ch2 = []

            self.data_length = 0     # dlzka datoveho bloku
            self.data_counter = 0

            self.terminal[1].value = 0
            self.terminal[2].value = 0

            if self.flag_data_read is False:

                self.shapeFillColor = Color.yellow
                try:
                    ip = str(self.parameter['IP'].value)
                    instr = vxi11.Instrument("TCPIP::" + ip + "::INSTR")
                    instr.lock_timeout = 0
                    print ('Device :', str(instr.ask("*IDN?")))
                    print ('Addr   :', str(instr.ask(":LAN:VISA?")))
                    self.flag_scope_ready = True
                except:
                    self.shapeFillColor = Color.red
                    self.flag_scope_ready = False

                    print("Zariadenie IP = " + ip + " nekomunikuje, skontroluj IP adresu ")

                    if self.engine is not None:
                        self.engine.stopSimulation()
                        time.sleep(0.1)
                    return

                if self.flag_scope_ready is True:
                    # nacitanie dat z pristroja
                    # nastavenie parametrov merania, nastavenie velkosti bloku, nacitanie wavememory
                    instr.write(":RUN")
                    time.sleep(0.1)

                    ch1_state = bool(instr.ask(":CHAN1:DISP?"))
                    ch2_state = bool(instr.ask(":CHAN2:DISP?"))
                    time.sleep(0.1)

                    print('CH1   :' + str(ch1_state))
                    print('CH2   :' + str(ch2_state))

                    if ch1_state and ch2_state is True:
                        instr.write(":ACQ:MDEP " + str(self.buff_size))
                    else:
                        instr.write(":ACQ:MDEP " + str(self.buff_size * 2))
                    time.sleep(0.1)

                    instr.write(":TRIG:SWE SING")
                    time.sleep(1)		# doba nacitanie pamate - TODO - upravit na nacitanie podla stavu osciloskopu

                    instr.write(":STOP")
                    time.sleep(0.5)

                    self.sample_rate = float(instr.ask(":ACQ:SRAT?"))
                    print ('Sample :', self.sample_rate)
                    self.step = 1.0 / self.sample_rate

                    print ('Step   :', self.step)

                    #------------------------------------------------------
                    # presun dat - kanal CH1
                    instr.write(":WAV:SOUR CHAN1")
                    time.sleep(0.1)

                    instr.write(":WAV:MODE MAX")
                    time.sleep(0.1)

                    instr.write(":WAV:RES")
                    time.sleep(0.1)

                    instr.write(":WAV:BEG")
                    time.sleep(0.5)

                    print ('State  :', str(instr.ask(":WAV:STAT?")))
                    #time.sleep(0.1)
                    buff = instr.ask_raw(":WAV:DATA?")

                    # konverzia dat pre kanal CH_1
                    buff = buff[11:-2]
                    for i in buff:
                        self.data_ch1.append(ord(i) - 128)
                    self.data_length = len(self.data_ch1)
                    print ('Data CH1:', self.data_length)

                    # ukoncenie merania
                    instr.write(":WAV:END")
                    time.sleep(0.3)

                    #------------------------------------------------------
                    # presun dat - kanal CH2
                    instr.write(":WAV:SOUR CHAN2")
                    time.sleep(0.1)

                    instr.write(":WAV:MODE MAX")
                    time.sleep(0.1)

                    instr.write(":WAV:RES")
                    time.sleep(0.1)

                    instr.write(":WAV:BEG")
                    time.sleep(0.1)

                    print('State  :', str(instr.ask(":WAV:STAT?")))
                    #time.sleep(0.1)
                    buff = instr.ask_raw(":WAV:DATA?")

                    # konverzia dat pre kanal CH_2
                    buff = buff[11:-2]
                    for i in buff:
                        self.data_ch2.append(ord(i) - 128)
                    self.data_length = len(self.data_ch2)
                    print ('Data CH2:', self.data_length)

                    # ukoncenie merania
                    instr.write(":WAV:END")
                    time.sleep(0.1)
                    #------------------------------------------------------

                    instr.write(":CHANNEL1:DISPLAY ON")
                    time.sleep(0.1)
                    instr.write(":RUN")
                    instr.write(":TRIG:SWE AUTO")

                    self.shapeFillColor = Color.mediumAquamarine
                    self.flag_data_read = True

                    # re-inicializacia hodnot parametrov
                    self.parameter['Step'].value = self.step
                    self.parameter['Stop Time'].value = self.step * self.data_length

                    # nastavenie kroku simulatora po nacitani dat
                    if self.engine is not None:
                        self.engine.setStep(self.step)
                        self.engine.setStopTime(self.step * self.data_length)

                    self.terminal[1].value = self.data_ch1[0]
                    self.terminal[2].value = self.data_ch2[0]

        elif flag == SIM_UPDATE:
            if self.flag_data_read is False:
                self.terminal[1].value = 0
                self.terminal[2].value = 0

                if self.engine is not None:
                    self.engine.stopSimulation()
                    time.sleep(0.1)
                return
            else:
                # nastavenie dat v standardnom mode
                self.terminal[1].value = self.data_ch1[self.data_counter]
                self.terminal[2].value = self.data_ch2[self.data_counter]
                self.data_counter = self.data_counter + 1

                if self.data_counter >= self.data_length:
                    self.engine.stopSimulation()
                    time.sleep(0.1)

        elif flag == SIM_FINISH:
            self.flag_data_read = False
            self.flag_scope_ready = False
