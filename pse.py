# -*- coding: utf-8 -*-

import os
import json
import time
import subprocess
import src.six as six

from numpy import *

'''!
@if English

Interface for interactive diagram control via Python/iPython.
For Linux only !  

@endif

@if Slovak

Rozhranie pre interaktivnu kontrolu diagramu z prostredia Python2/3 (iPython2/3).

Komunikacia je prostrednictvom pipe, v diagrame je potrebne umiestnit komponent
PPC a definovat v nom meno pipe. Komponent vytvori jednu pipe pre zapis a druhu
pre citanie.
Rovnake meno pipe je potrebne definovat aj pri vytvarani komunikacneho rozhrania
v konstruktore alebo volanim metody setPipe(..).

Dlzka pipe je limitovana systemom na 64kB, pri prenasani vacsieho objemu dat sa tieto odovzdavaju
prostrednictvom temp suboru. Komunikacnym formatom je JSON.

Pouzitie:

    run:
    ipython3 -matplotlib

    >>> from pse import *
    >>> pse=PSE('pipe_name')
    >>> pse.startApp('./main.py', 'file_name.pse')

@endif
'''

# kody povelov a chybovych hlaseni
PSE_CMP_LIST = 1
PSE_NET_LIST = 2
PSE_SET_VALUE = 3
PSE_GET_VALUE = 4
PSE_SIM_START = 5
PSE_SIM_STOP = 6
PSE_SIM_RESET = 7
PSE_SIM_STATE = 8

PSE_ERR_NONE = 0
PSE_ERR_CODE = 100        # neznamy kod povelu
PSE_ERR_REF = 101         # neexistujuca referencia v diagrame
PSE_ERR_PARAM = 102       # objekt nema odkazovany parameter
PSE_ERR_VALUE = 103       # zly format nastavovanej hodnoty

PSE_EXC_PSIZE = 104       # prekrocena dlzka dat 65536 byte pre pipe, data su ulozene v temo subore

PSE_ERR_TIMEOUT = 105     # klient neodpoveda
PSE_ERR_INIT = 106        # pipe nie je inicializovana


class pse():
    '''!
    @if English

    @endif

    @if Slovak

    Komunikacne rozhranie pre interaktivne riadenie simulacie z prostredia iPython3
    alebo uzivatelskeho programu.

    @endif
    '''

    def __init__(self, pipePath=None):
        self.pipePath = pipePath

        self.msgId = 0                    # identifikacne cislo spravy

        self.pipeRead = None              # pipe na zapis, diagram cita
        self.pipeWrite = None             # pipe na citanie, diagram zapisuje

        if self.pipePath is not None:
            self.setPipe(pipePath)

    def setPipe(self, pipePath):
        '''!
        @if English

        @endif

        @if Slovak

        Nastavenie alebo reinicializacia komunikacnej pipe.

        @endif
        '''
        self.pipePath = pipePath

        # kontrola na zadanie cesty k pipe
        if ('/' in pipePath) is not True:
            # pipe neobsahuje cestu - doplnenie o cestu k /tmp adresaru
            pipePath = '/tmp/' + pipePath

        # kontrola existencie adresarov a vytvorenia pipe pre citanie a zapis
        if not os.path.exists(pipePath + '_dr'):        # dr - diagram read
            os.mkfifo(pipePath + '_dr')

        if not os.path.exists(pipePath + '_dw'):        # dw - diagram write
            os.mkfifo(pipePath + '_dw')

        # otvorenie pipe a priradenie deskriptora
        try:
            # pipe na zapis (!)
            self.pipeRead = os.open(pipePath + '_dr', os.O_RDWR | os.O_NONBLOCK)
            # pipe na citanie (!)
            self.pipeWrite = os.open(pipePath + '_dw', os.O_RDWR | os.O_NONBLOCK)

            # vycistenie vstupnej pipe
            while True:
                try:
                    os.read(self.pipeWrite, 1)
                except:
                    break

        except:
            self.pipeWrite = None
            self.pipeRead = None
            print('>>> Error ')
            print('    Could not open pipe for reading / writing', pipePath + '_dr', pipePath + '_dw')

    def command(self, cmd, ref='', param='', value=0):
        '''!
        @if English

        @endif

        @if Slovak

        Vyslanie a prijem povelu.

        @endif
        '''

        if self.pipePath is None:
            print('>>> Error - nie je inicializovana pipe \n')
            return [PSE_ERR_INIT, '', '', 0]

        q = [self.msgId, cmd, ref, param, value]
        s = json.dumps(q, default=self.jsonExport)

        # zapis povelu
        if six.PY2 is True:
            os.write(self.pipeRead, s + '\n')
        if six.PY3 is True:
            os.write(self.pipeRead, bytes(s + '\n', 'UTF-8'))

        # nacitanie odpovede
        timeout = 0
        s = ''
        while True:
            w = 0
            try:
                q = os.read(self.pipeWrite, 1)    # ? nahrada cez readline
                w = q.decode('ascii')
                s = s + w
            except:
                # v pripade ze v pipe nie je ziaden znak -> delay
                time.sleep(0.05)
                timeout = timeout + 1

            # kontrola na timeout
            if timeout >= 100:        # 5sec
                # pipe neodpoveda
                print('>>> Error - timeout, klient neodpoveda \n')
                return [0, '', '', 0, PSE_ERR_TIMEOUT]

            if w == '\n':
                break

        # dekodovanie dat, vykonanie povelu a odoslanie odpovede
        rdata = json.loads(s, object_hook=self.jsonImport)

        # struktura odpovede
        # rdata[0] - msgId
        # rdata[1] - ref
        # rdata[2] - param
        # rdata[3] - value
        # rdata[4] - errCode

        if rdata[0] != self.msgId:
            print('>>> Error - chyba parovania sprav \n')

        self.msgId = self.msgId + 1

        if rdata[4] == PSE_ERR_REF:
            print('>>> Error - v diagrame sa nevyskytuje objekt s Ref = ', ref)

        elif rdata[4] == PSE_ERR_PARAM:
            print('>>> Error - Objekt Ref = ', ref, 'nema parameter ', param, '\n')

        elif rdata[4] == PSE_ERR_VALUE:
            print('>>> Error - Objekt Ref = ', ref, 'parameter ', param, ' - chybny typ hodnoty \n')

        elif rdata[4] == PSE_EXC_PSIZE:
            # presun dat pri prekroceni maximalneho rozsahu pipe 64k - data sa odovzdavaju cez temp subor
            # nacitanie dat zo subor, meno odovzdane v strukture cez pipe
            f = open(rdata[3], 'r')
            s = f.readline()
            f.close()
            # dekodovanie dat zo suboru
            tempdata = json.loads(s, object_hook=self.jsonImport)
            return tempdata[3]

        if rdata[4] == PSE_ERR_NONE:
            return rdata[3]
        else:
            return None

    def getCompList(self):
        '''!
        @if English

        Read diagram component list.

        @endif

        @if Slovak

        Funkcia vrati zoznam refrencii vsetkych vizualnych komponentov diagramu.

        @endif
        '''
        return self.command(PSE_CMP_LIST)

    def getNetList(self):
        '''!
        @if English

        Read diagram net list.

        @endif

        @if Slovak

        Funkcia vrati zoznam mien vsetkych prepojeni v diagrame.

        @endif
        '''
        return self.command(PSE_NET_LIST)

    def getValue(self, ref, paramId='Value'):
        '''!
        @if English

        @endif

        @if Slovak

        Nacitanie hodnoty komponentu.

        Komponent musi mat deklarovany parameter, default sa predpoklada parameter Value.
        Je mozne nacitat (pri zadani paramId) lubovolny parameter komponentu.

        @endif
        '''
        return self.command(PSE_GET_VALUE, ref, paramId)

    def setValue(self, ref, value, paramId='Value'):
        '''!
        @if English

        @endif

        @if Slovak

        Nastavenie hodnoty parametra komponentu.

        Nastavi hodnotu parametra (default 'Value') zvoleneho komponentu.

        @endif
        '''
        return self.command(PSE_SET_VALUE, ref, paramId, value)

    def simStart(self):
        '''!
        @if English

        @endif

        @if Slovak

        Spustenie alebo restart simulacie.

        @endif
        '''
        return self.command(PSE_SIM_START)

    def simStop(self):
        '''!
        @if English

        @endif

        @if Slovak

        Ukoncenie simulacie

        @endif
        '''
        return self.command(PSE_SIM_STOP)

    def simReset(self):
        '''!
        @if English

        @endif

        @if Slovak

        Reset komponentov - inicializacie premennych, zmazanie poli.

        @endif
        '''
        return self.command(PSE_SIM_RESET)

    def simState(self):
        '''!
        @if English

        @endif

        @if Slovak

        Zistenie stavu aktualne prebiehajucej simulacie.

        True - simulacia je aktivna
        False - simulacia je ukoncena

        @endif
        '''
        return self.command(PSE_SIM_STATE)

    def jsonExport(self, obj):
        return obj

    def jsonImport(self, obj):
        return obj

    def startApp(self, app, param=''):
        '''!
        @if English

        @endif

        @if Slovak

        Spustenie aplikacie ako samostatneho subprocesu.

        app - string, meno suboru aplikacie, napr './src/main.py'
        param - string, parametre odovzdavane aplikacii

        @endif
        '''
        if six.PY2:
            subprocess.Popen(['python', app, param], shell=False)

        if six.PY3:
            subprocess.Popen(['python3', app, param], shell=False)
