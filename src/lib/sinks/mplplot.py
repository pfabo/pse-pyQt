# -*- coding: utf-8 -*-

import json
import os
import subprocess

from numpy import ndarray

from color import Color
from component import Component
from componenttypes import *  # @UnusedWildImport
from lib.pseqt import *  # @UnusedWildImport
from terminal import TERM


class MplPlot_YT(Component):
    '''
    @if English

    Interface for data visualisation with Matplotlib.

    Time record (Y-Time) plot.

    @endif

    @if Slovak

    Rozhranie pre vizualizáciu dát pomocou Matplotlib-u.

    Zobrazenie časového priebehu dát.

    Komponent pripraví dáta pre vizualizáciu, serializuje ich pomocou JSON,
    uloží do dočasného súboru v adresári ./tmp
    a spustí podproces s klientom zobrazujúcim dáta.

    Data z každej simulácie sa ukladajú do samostatného súboru
    @todo
    ? - možnosť dodatočného použitia dát
    ? - prepisovanie po každej simulacii
    ? - nastavenie inej cesty ako ./tmp - obsah sa maze pri starte

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'mpl_yt.svg'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.blue

        self.data_x = []		# datove polia
        self.data_y = []

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST,
                         TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)

        self.addParameter('Title', '')
        self.addParameter('X Label', '')
        self.addParameter('Y Label', '')
        self.addParameter('Grid', 'True')
        self.addParameter('Format', '')
        self.addParameter('File', '')
        self.addParameter('Y Data', [])
        self.addParameter('Time', [])

        self.fileCounter = 1

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.mediumAquamarine)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):

        if flag == SIM_INIT or flag == SIM_RESET: 	# re / inicializaci dat
            self.data_x = []
            self.data_y = []

        elif flag == SIM_UPDATE:
            inp = self.terminal[1].value
            self.data_x.append(time)
            if (type(inp) == ndarray) or (type(inp) == list):
                self.data_y.append(list(inp))     # konverzia array->list, JSON circular reference
            else:
                self.data_y.append(inp)

        elif flag == SIM_FINISH:
            # zbalenie dat pre zobrazovanie do suboru pomocou JSON
            plot_title = self.parameter['Title'].value
            plot_xlabel = self.parameter['X Label'].value
            plot_ylabel = self.parameter['Y Label'].value
            plot_grid = self.parameter['Grid'].value
            plot_format = self.parameter['Format'].value

            # formatovanie dat, prevod pomocou JSON a zapis do suboru
            ret_data = [plot_title, plot_xlabel, plot_ylabel, plot_grid,
                        plot_format, self.data_x, self.data_y]
            exp_data = json.dumps(ret_data, default=self.jsonExport)

            fileName = './tmp/mpl_%s_%s.txt' % (self.parameter['Ref'].value,
                                                self.fileCounter)

            fp = open(fileName, 'w')
            fp.write(exp_data)
            fp.close()
            self.parameter['File'].value = fileName
            self.parameter['Y Data'].value = self.data_y
            self.parameter['Time'].value = self.data_x

            # spustenie klientskej aplikacie pre zobrazenie dat
            start_script('mpl_yt.py', fileName)

            self.fileCounter = self.fileCounter + 1

    def jsonExport(self, obj):
        '''
        '''
        return obj


class MplPlot_XY(Component):
    '''
    @if English

    Interface for data visualisation with Matplotlib.

    Parametric (X-Y) plot.

    @endif

    @if Slovak

    Rozhranie pre vizualizáciu dát pomocou Matplotlib-u.

    Zobrazenie parametrického (X-Y) priebehu dát.

    Komponent pripraví dáta pre vizualizáciu, serializuje ich pomocou JSON,
    uloží do dočasného súboru v adresári ./tmp a spustí podproces
    s klientom zobrazujúcim dáta.

    Data z každej simulácie sa ukladajú do samostatného súboru
    @todo
    ? - možnosť dodatočného použitia dát
    ? - prepisovanie po každej simulacii
    ? - nastavenie inej cesty ako ./tmp - obsah sa maze pri starte

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'mpl_xy.svg'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.blue

        self.data_x = []		# datove polia
        self.data_y = []

        self.addTerminal('IN_Y', 1, TERM.IN, QPointF(-30, -10), TERM.DIR_EAST,
                         TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)
        self.addTerminal('IN_X', 2, TERM.IN, QPointF(-30, 10), TERM.DIR_EAST,
                         TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)

        self.addParameter('Title', '')
        self.addParameter('X Label', '')
        self.addParameter('Y Label', '')
        self.addParameter('Grid', 'True')
        self.addParameter('Format', '')
        self.addParameter('File', '')
        self.addParameter('Y Data', [])
        self.addParameter('X Data', [])

        self.fileCounter = 1

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.mediumAquamarine)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):

        if flag == SIM_INIT or flag == SIM_RESET: 	# re / inicializaci dat
            self.data_x = []
            self.data_y = []

        elif flag == SIM_UPDATE:
            inp_y = self.terminal[1].value
            if (type(inp_y) == ndarray) or (type(inp_y) == list):
                self.data_y.append(list(inp_y))     # konverzia array->list, JSON circular reference
            else:
                self.data_y.append(inp_y)

            inp_x = self.terminal[2].value
            if (type(inp_x) == ndarray) or (type(inp_x) == list):
                self.data_x.append(list(inp_x))     # konverzia array->list, JSON circular reference
            else:
                self.data_x.append(inp_x)

        elif flag == SIM_FINISH:
            # zbalenie dat pre zobrazovanie do suboru pomocou JSON
            plot_title = self.parameter['Title'].value
            plot_xlabel = self.parameter['X Label'].value
            plot_ylabel = self.parameter['Y Label'].value
            plot_grid = self.parameter['Grid'].value
            plot_format = self.parameter['Format'].value

            # formatovanie dat, prevod pomocou JSON a zapis do suboru
            ret_data = [plot_title, plot_xlabel, plot_ylabel, plot_grid,
                        plot_format, self.data_x, self.data_y]
            exp_data = json.dumps(ret_data, default=self.jsonExport)

            fileName = './tmp/mpl_%s_%s.txt' % (self.parameter['Ref'].value,
                                                self.fileCounter)

            fp = open(fileName, 'w')
            fp.write(exp_data)
            fp.close()
            self.parameter['File'].value = fileName
            self.parameter['Y Data'].value = self.data_y
            self.parameter['X Data'].value = self.data_x

            # spustenie klientskej aplikacie pre zobrazenie dat
            start_script('mpl_xy.py', fileName)
            self.fileCounter = self.fileCounter + 1

    def jsonExport(self, obj):
        '''
        '''
        return obj


class MplPlot_Hist(Component):
    '''
    @if English

    Interface for data visualisation with Matplotlib.

    Histogram plot.

    @endif

    @if Slovak

    Rozhranie pre vizualizáciu dát pomocou Matplotlib-u.

    Zobrazenie histogramu dát.

    Ak je vstupná hodnota vektor, zobrazí sa histogram len prvej položky vektora.
    Komponent pripraví dáta pre vizualizáciu, serializuje ich pomocou JSON,
    uloží do dočasného súboru v adresári ./tmp a spustí podproces
    s klientom zobrazujúcim dáta.

    Data z každej simulácie sa ukladajú do samostatného súboru
    @todo
    ? - možnosť dodatočného použitia dát
    ? - prepisovanie po každej simulacii
    ? - nastavenie inej cesty ako ./tmp - obsah sa maze pri starte

    @endif
    '''

    def __init__(self, name, pos):
        Component.__init__(self, name, pos)

        self.compType = TYPE_SIM_CONTINUOUS
        self.shapeImage = 'mpl_hist.svg'
        self.box = QRectF(-30, -30, 60, 60)
        self.shapeColor = Color.blue

        self.data_y = []

        self.addTerminal('IN', 1, TERM.IN, QPointF(-30, 0), TERM.DIR_EAST,
                         TERM.IN_ARROW_SMALL_FILL, TERM.IN_ARROW_SMALL)

        self.addParameter('Title', '')
        self.addParameter('X Label', '')
        self.addParameter('Y Label', '')
        self.addParameter('Grid', 'True')
        self.addParameter('Bins', 50)
        self.addParameter('File', '')
        self.addParameter('Y Data', [])

        self.fileCounter = 1

    def drawShape(self, gc):
        grad = QLinearGradient(0, -25, 0, 50)
        grad.setColorAt(0, Color.white)
        grad.setColorAt(1, Color.mediumAquamarine)
        gc.setBrush(QBrush(grad))

        gc.setPen(QPen(self.shapeColor, 1))
        gc.drawRoundedRect(-25, -25, 50, 50, 5, 5)
        self.drawIcon(gc, -20, -20)

    def sim(self, flag, value, time, step):

        if flag == SIM_INIT or flag == SIM_RESET: 	# re / inicializaci dat
            self.data_y = []

        elif flag == SIM_UPDATE:
            inp = self.terminal[1].value
            if (type(inp) == ndarray) or (type(inp) == list):
                self.data_y.append(list(inp[0]))     # konverzia array->list, JSON circular reference
            else:
                self.data_y.append(inp)

        elif flag == SIM_FINISH:
            # zbalenie dat pre zobrazovanie do suboru pomocou JSON
            plot_title = self.parameter['Title'].value
            plot_xlabel = self.parameter['X Label'].value
            plot_ylabel = self.parameter['Y Label'].value
            plot_grid = self.parameter['Grid'].value
            plot_bins = self.parameter['Bins'].value

            # formatovanie dat, prevod pomocou JSON a zapis do suboru
            ret_data = [plot_title, plot_xlabel, plot_ylabel,
                        plot_grid, plot_bins, self.data_y]
            exp_data = json.dumps(ret_data, default=self.jsonExport)

            fileName = './tmp/mpl_%s_%s.txt' % (self.parameter['Ref'].value,
                                                self.fileCounter)
            fp = open(fileName, 'w')
            fp.write(exp_data)
            fp.close()
            self.parameter['File'].value = fileName
            self.parameter['Y Data'].value = self.data_y

            # spustenie klientskej aplikacie pre zobrazenie dat
            start_script('mpl_hist.py', fileName)
            self.fileCounter = self.fileCounter + 1

    def jsonExport(self, obj):
        '''
        '''
        return obj


def start_script(sname, filename):
    '''start script in python interpreter.

    :param sname: path to python script
    :param filename: argument
    '''
    here = os.path.dirname(__file__)
    pth = os.path.join(here, sname)

    # TODO: check what is proper way to find python.exe in Windows
    if six.PY2:
        subprocess.Popen(["python", pth, filename])
    if six.PY3:
        subprocess.Popen(["python3", pth, filename])
