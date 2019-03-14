# -*- coding: utf-8 -*-

'''!
@if English

@endif

@if Slovak

Komunikácia s diagramom z prostredia Pythonu resp. iPythonu pomocou výmeny dát cez systémovú pipe.
Formát dát je definovaný pomocou knižnice JSON. Pipe sa vytvára v systémovom ./tmp adresári. Komunikacia
je nezavisla od shellu, v ktorom je spusteny Python alebo aplikacia, v diagrame musi byť len umiestnený
komponent PPC, ktorý vytvorí pomocou pipe komunikačný kanál.

Velkosť pipe je obmedzená systémom na 64K. Pre väščie dáta je vhodné použiť zápis do súboru.

@endif
'''

from threading import Thread
import json
import os
import time

from color import Color
from component import Component
from componenttypes import TYPE_DECORATION
from lib.pseqt import *


# kody povelov a chybovych hlaseni
PSE_CMP_LIST = 1          # zoznam komponentov
PSE_NET_LIST = 2          # zoznam prepojeni
PSE_SET_VALUE = 3         # nastavenie hodnoty parametra
PSE_GET_VALUE = 4         # nacitanie hodnoty parametra
PSE_SIM_START = 5         # spustenie simulacie
PSE_SIM_STOP = 6          # zastavenie simulacie
PSE_SIM_RESET = 7         # reset hodnot objektov
PSE_SIM_STATE = 8         # stav simulacie, prebiehajuca simulacia
                          # @todo - doplnit prikaz pre nacitanie zoznamu parametrov objektu

PSE_ERR_NONE = 0          # ziadna chyba
PSE_ERR_CODE = 100        # neznamy kod povelu
PSE_ERR_REF = 101         # neexistujuca referencia v diagrame
PSE_ERR_PARAM = 102       # objekt nema odkazovany parameter
PSE_ERR_VALUE = 103       # zly format nastavovanej hodnoty
PSE_EXC_PSIZE = 104       # prekrocena dlzka dat 64k pre pipe, data sa neodovzdavaju v pipe, ale v temp subore


class Control_PPC(Component):
    '''!
    @if English

    @brief Remote diagram control via system pipe OS Linux.

    @endif

    @if Slovak
    @brief Riadenie diagramu cez systémovú pipe v OS Linux.

    Komponent otvorí pipe pre čítanie / zápis definovanú v parametri <B>Pipe</B> a spustí interný thread,
    ktorý periodicky (cca 20x za sekundu) načítava obsah pipe. Podľa obsahu poľa zapísaného do pipe
    sa vyvolajú metódy pre načítanie alebo nastavenie parametrov komponentov v diagrame.



    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_DECORATION    # nesimulovany komponent
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.black

        self.addParameter('Pipe', '', visibleName=True)    # ! default meno = '' -> flag - nevytvara pipe pri zobrazeni komponentu v kniznici
        self.pipeRead = None        # pipe pre prijem povelov
        self.pipeWrite = None       # pipe pre zapis odpovede
        self.pipeTemp = None        # docasny subor pre zapis dlhych datovych blokov, presahujucich rozmer standardnej systemovej pipe (64k)

        self.pipeThread = None      # thread na citanie pipe

    def drawShape(self, gc):

        gc.setPen(QPen(self.shapeColor, 0.6))
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.cyan)
        gc.setBrush(QBrush(grad))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)

        font = QFont('Decorative', 12)
        font.setItalic(True)
        gc.setFont(font)
        gc.setPen(QPen(Color.blue, 1))
        gc.drawText(self.box, Qt.AlignCenter, 'PPC')

    def updateShape(self):

        pipePath = self.parameter['Pipe'].value

        # default path - nevytvara pipe pri vytvoreni objektu v kniznici a pod.
        if pipePath == '':
            return

        # ukoncenie beziaceho threadu citania pipe
        if self.pipeThread is not None:
            self.pipeThread.stop()

        # kontrola na zadanie cesty k pipe
        if ('/' in pipePath) is not True:
            # pipe neobsahuje cestu - doplnenie o cestu k /tmp adresaru
            pipePath = '/tmp/' + pipePath

        # kontrola existencie adresarov a vytvorenia pipe pre citanie a zapis
        if not os.path.exists(pipePath + '_dr'):        # dr - diagram read
            os.mkfifo(pipePath + '_dr')

        if not os.path.exists(pipePath + '_dw'):        # dw - diagram write
            os.mkfifo(pipePath + '_dw')

        # vytvorenie mena suboru pre zapis velkych dat
        self.pipeTemp = pipePath + '_data.txt'

        # otvorenie pipe, priradenie deskriptora a spustenie threadu pre citanie pipe
        try:
            self.pipeRead = os.open(pipePath + '_dr', os.O_RDWR | os.O_NONBLOCK)
            self.pipeWrite = os.open(pipePath + '_dw', os.O_RDWR | os.O_NONBLOCK)
            self.pipeThread = PipeThread(self, self.pipeRead, self.pipeWrite, self.pipeTemp)
        except:
            self.pipeWrite = None
            self.pipeRead = None
            print('>>> Error ')
            print('    Could not open pipe for reading / writing', pipePath + '_dr', pipePath + '_dw')

    def deleteShape(self):
        '''
        Ukoncenie threadu
        '''
        if self.pipeThread is not None:
            self.pipeThread.stop()
            self.pipeThread = None
        os.close(self.pipeRead)
        os.close(self.pipeWrite)


class PipeThread(Thread):
    '''
    @if English

    @endif

    @if Slovak

    Nacitanie sprav z pipe a ich spracovanie.

    @endif
    '''

    def __init__(self, component, pipeRead, pipeWrite, pipeTemp):
        Thread.__init__(self)
        self.pipeRead = pipeRead
        self.pipeWrite = pipeWrite
        self.pipeTemp = pipeTemp
        self.comp = component

        # vycistenie vstupnej pipe
        while True:
            try:
                os.read(self.pipeRead, 1)    # ? nahrada cez readline
            except:
                break

        self.start()

    def stop(self):
        self.pipeRead = None

    def run(self):
        s = ''
        while True:
            # ukoncenie threadu
            if self.pipeRead is None:
                break

            w = 0
            try:
                q = os.read(self.pipeRead, 1)    # ? nahrada cez readline
                w = q.decode('ascii')
                s = s + w
            except:
                # v pripade ze v pipe nie je ziaden znak -> delay
                time.sleep(0.05)

            # ukoncenie nacitanie
            if w == '\n':

                # dekodovanie dat, vykonanie povelu a odoslanie odpovede
                rdata = json.loads(s, object_hook=self.jsonImport)
                # format povelu
                msgId = rdata[0]        # cislo spravy
                cmd = rdata[1]          # kod povelu
                ref = rdata[2]          # referencia komponentu
                param = rdata[3]        # meno parametra komponentu
                value = rdata[4]        # hodnota parametra

                # odpoved na povel, default chybove hlasenie o neznamom povele
                if cmd == PSE_CMP_LIST:
                    wdata = self.cmdCompList(ref, param, value)

                elif cmd == PSE_NET_LIST:
                    wdata = self.cmdNetList(ref, param, value)

                elif cmd == PSE_SET_VALUE:
                    wdata = self.cmdSetValue(ref, param, value)

                elif cmd == PSE_GET_VALUE:
                    wdata = self.cmdGetValue(ref, param)

                elif cmd == PSE_SIM_START:
                    wdata = self.cmdSimStart(ref, param, value)

                elif cmd == PSE_SIM_STOP:
                    wdata = self.comp.diagram.parent.simStart()

                elif cmd == PSE_SIM_RESET:
                    wdata = self.comp.diagram.parent.simReset()

                elif cmd == PSE_SIM_STATE:
                    wdata = self.cmdSimState(ref, param, value)

                else:
                    wdata = [0, 0, 0, PSE_ERR_CODE]

                # navratova hodnota povelu
                retData = [msgId] + wdata
                ws = json.dumps(retData, default=self.jsonExport)

                # konverzia povelu
                if six.PY2 is True:
                    expData = ws + '\n'
                if six.PY3 is True:
                    expData = bytes(ws + '\n', 'UTF-8')

                if len(expData) >= 65536:
                    # data length exceeds pipe length system limit size
                    # data prekracujuce rozsah 64k su zapisane do docasneho suboru, v pipe sa odovzda meno suboru
                    # a hlasenie o prekroceni maximalneho rozsahu
                    f = open(self.pipeTemp, 'w')
                    f.write(expData)
                    f.close()

                    ws = json.dumps([msgId, 0, 0, self.pipeTemp, PSE_EXC_PSIZE], default=self.jsonExport)
                    if six.PY2 is True:
                        expData = ws + '\n'
                    if six.PY3 is True:
                        expData = bytes(ws + '\n', 'UTF-8')

                os.write(self.pipeWrite, expData)
                s = ''
                w = 0

    def jsonImport(self, obj):
        '''
        '''
        return obj

    def jsonExport(self, obj):
        '''
        '''
        return obj

    def cmdGetValue(self, ref, paramId):
        """!
        @if English
        @brief Return value of component selected parameter.

        Function return array with parameter value and error code:
            [ref, paramId, value, errCode]

        @param ref: component reference
        @param paramId: parameter name

        @return aray with parameter value and error code

        @endif

        @if Slovak
        @brief Vráti hodnotu vybraného parametra komponentu.

        Funkcia pri úspešnom načítaní hodnoty parametra vráti pole so štruktúrou:

            [ref, paramId, value, errCode]

        Hodnoty error_code:
        - PSE_ERR_NONE - pri načítani hodnoty parametra sa nevyskytla chyba
        - PSE_ERR_REF - v diagrame neexistuje objekt s udanou refrenciou / menom
        - PSE_ERR_PARAM - v danom komponente sa nevyskytuje zvoleny parameter

        @param ref: referencia / meno zvoleneho komponentu
        @param paramId: meno parametra

        @return Pole s hodnotami parametrov funkcie, hodnotou parametra a kódom chyby

        @endif
        """
        # prehladanie zoznamu komponentov
        for q in self.comp.diagram.componentList:
            if q.parameter['Ref'].value == ref:
                try:
                    return [ref, paramId, q.parameter[paramId].value, PSE_ERR_NONE]
                except:
                    # pristup k neexistujucemu parametru
                    return [ref, paramId, 0, PSE_ERR_PARAM]
        # v zozname sa nenachadza komponent s danym Ref
        return [ref, 0, 0, PSE_ERR_REF]

    def cmdSetValue(self, ref, paramId, value):
        """!
        @if English

        @endif

        @if Slovak

        @brief Nastavenie hodnoty parametra zvoleneho komponentu.

        Pri uspesnom nastaveni hodnoty parametra funkcia vrati pole so strukturou:

            [ref, paramId, value, errCode]

        Hodnoty error_code:
        - PSE_ERR_NONE - pri nastaveni hodnoty parametra sa nevyskytla chyba
        - PSE_ERR_REF - v diagrame neexistuje objekt s udanou refrenciou / menom
        - PSE_ERR_PARAM - v danom komponente sa nevyskytuje zvoleny parameter

        @param ref: referencia / meno zvoleneho komponentu

        @param paramId: meno parametra

        @param value: nastavovana hodnota parametra

        @return pole s hodnotami parametrov funkcie a kodom chyby

        @todo doplnit kontrolu typu parametra podla parameter.type
        @todo doplnit kody a popis chyb

        @endif
        """

        # prehladanie zoznamu komponentov
        # @todo - prerobit na inteligentnejsi algoritmus (strom)
        for q in self.comp.diagram.componentList:
            if q.parameter['Ref'].value == ref:
                try:
                    q.parameter[paramId].value = value
                    return [ref, paramId, q.parameter[paramId].value, PSE_ERR_NONE]
                except:
                    # pristup k neexistujucemu parametru
                    return [ref, paramId, 0, PSE_ERR_PARAM]
        # v zozname sa nenachadza komponent s danym Ref
        return [ref, 0, 0, PSE_ERR_REF]

    def cmdCompList(self, ref, paramId, value):
        '''!
        @if English

        @endif

        @if Slovak

        @brief Načítanie zoznamu referencií komponentov v diagrame.

        @endif
        '''
        compList = []
        # prehladanie zoznamu komponentov
        for q in self.comp.diagram.componentList:
            compList.append(q.parameter['Ref'].value)
        return [ref, paramId, compList, PSE_ERR_NONE]

    def cmdNetList(self, ref, paramId, value):
        '''!
        @if English

        @endif

        @if Slovak

        @brief Načítanie mien prepojení v diagrame.

        @endif
        '''
        netList = []
        # prehladanie zoznamu komponentov
        for q in self.comp.diagram.netList:
            netList.append(q.name)
        return [ref, paramId, netList, PSE_ERR_NONE]

    def cmdSimStart(self, ref, paramId, value):
        '''!
        @if English

        @endif

        @if Slovak

        @brief Spustenie simulacie, vrati status beziacej simulacie

        @endif
        '''
        simEngine = self.comp.diagram.parent.simEngine

        if simEngine is not None:
            # simulacia nie je spustena - spustenie simulacie
            self.comp.diagram.parent.simStop()

        simEngine = self.comp.diagram.parent.simStart()
        return [ref, paramId, True, PSE_ERR_NONE]

    def cmdSimState(self, ref, paramId, value):
        '''!
        @if English

        @endif

        @if Slovak

        @brief Nacitanie stavu simulacie.

        @endif
        '''
        simState = False
        simEngine = self.comp.diagram.parent.simEngine

        if simEngine is not None:
            simState = self.comp.diagram.parent.simEngine.flagSimActive

        return [ref, paramId, simState, PSE_ERR_NONE]
