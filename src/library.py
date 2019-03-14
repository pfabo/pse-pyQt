# -*- coding: utf-8 -*-

"""!
@if English

Simple library manager.

Contains component viewer and drag & drop suport.

@endif
"""

import six

from color import Color
from component import Component
from diagram import GRID
import lib


if six.PY2:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

else:
    # from PyQt5.QtSvg import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *

'''
Config for library pages
var = (pageName,
      (componentName, posX, posY, description),
      ... )

optional description is used as text/component name in library window
  - no description or '' ... as text is used class name
  - ' ' ... component is displayed without description
'''

# config for library pages
# var = (pageName,
#       (componentName, posX, posY, description),
#      ... )
#
# optional description is used as text/component name in library window
#    - no description or '' ... as text is used class name
#    - ' ' ... component is displayed without description
sources = (
         'Sources',
        ('GenSine', 0, 0, 'Sin'), ('GenRamp', 80, 0, 'Ramp'), ('GenPulse', 160, 0, 'Pulse'), ('GenRandInt', 240, 0, 'RandInt'),
        ('ContrGenRamp', 0, 80, 'RampCnt'), ('GenSineContr', 80, 80, 'SinCnt'), ('GenOneShot', 160, 80, 'OneShot'), ('FileRead_CSV', 240, 80, 'RdFile'),
        ('GenNoiseGauss', 0, 160, 'Noise'), ('GenCos', 80, 160, 'Cos'), ('GenPulseSeq', 160, 160, 'SqPulse'),
        ('GenConst', 0, 225, 'Const'), ('GenTime', 80, 225, 'Time'), ('GenStep', 160, 225, 'Step'),
        ('ArduinoBoard', 0, 320, 'Arduino'), ('TomcatBoard', 80, 290, 'Tomcat'),
        # ('ScopeRigol', 0, 440, 'Rigol'),
    )

sinks = (
         'Sinks',
        ('Console', 0, 0), ('FileCSV', 80, 0, 'WrFile'), ('FileHDF5', 80 + 80, 0, 'FileHDF5'), ('WsArray', 160+80, 0, 'Array'), ('MplPlot_YT', 240+80, 0, 'MatPlot YT'),
        ('MplPlot_XY', 320 + 80, 0, 'MatPlot XY'), ('MplPlot_Hist', 400 + 80, 0, 'MatPlot Hist'),
        ('Plot', -20, 50, ' '), ('Plot_Q4', 240, 50, ' '),
        ('Plot_XY', -20, 250, ' '), ('Plot_Q8', 240, 250, ' '),
        ('Plot_DT', -20, 450, ' ')
    )

signal = (
         'Signal',
        ('PortIn', 0, 0, 'In'), ('PortOut', 80, 0, 'Out'), ('PortNull', 160, 0, 'Null'),
        ('BusCompressor', 0, 60, 'Compress'), ('BusExpander', 80, 60, 'Expand'),
        ('Block', 0, 130)
        )

linear = ('Linear',
        ('Gain', 15, -80), ('Integ', 115, -80),

        ('Abs', 0, 0), ('Sin', 80, 0), ('Cos', 160, 0), ('Sqrt', 240, 0),
        ('Exp', 0, 80), ('Pow2', 80, 80), ('Ln', 160, 80), ('Log10', 240, 80),
        ('FuncEval', 0, 160), ('Min', 80, 160), ('Max', 160, 160), ('Ratio', 240, 160),

        ('TrFunc1', 10, 240), ('TrFunc2', 140, 240),

        ('Sum21', -20, 320, ' '), ('Mult22', 80, 320, ' '), ('RegSum2B', 200, 320, ' '), ('Equ', 290, 320, ' '),
        ('Sum22', -20, 400, ' '), ('Mult21', 80, 400, ' '), ('RegSum2A', 200, 400, ' '), ('Lss', 290, 400, ' '),
        ('Sum31', -20, 480, ' '), ('Mult31', 80, 480, ' '), ('RegSum3', 200, 480, ' '), ('Leq', 290, 480, ' '),
                                  ('Div22', 80, 560, ' '),
        )

discrete = (
         'Discrete',
        ('Clock', 0, -80), ('UnitDelay', 80, -80), ('LogPulse', 160, -80), ('LogCounter', 240, -80),
        ('Adc', 0, 0), ('UnitDelayClk', 80, 0),
        ('And2', 0, 80, ' '), ('Nand2', 80, 80, ' '), ('Buffer', 170, 80, ' '), ('Or2', 250, 80, ' '),
        ('And3', 0, 160, ' '), ('Nand3', 80, 160, ' '), ('Invertor', 170, 160, ' '), ('Nor2', 250, 160, ' '),
        ('RS', -40, 200, ' '), ('D', 70, 200, ' '),
        ('Led', 0, 280, ' '), ('Led4', 60, 280, ' '), ('LedBig', 120, 280, ' '),
    )

nonlinear = (
         'Nonlinear',
        ('Logistic', 0, 0), ('Saturation', 80, 0), ('Chuafonc', 160, 0), ('Fmodulo', 240, 0),
        ('FmoduloB', 0, 80), ('FmoduloC', 80, 80), ('CompBlock', 160, 80, 'Comp'), ('Switch2', 240, 80),

        ('CompST', 0, -80),
        ('CompHS', 0, -160), ('CompHSContr', 110, -160),
        ('CompLatch', 0, -240)
    )

interactive = (
         'Interactive',
        ('WdSliderV', 0, 0, ' '), ('WdDial', 80, 0, ' '), ('WdSliderH', 180, 40, ' '), ('WdButton', 180, 80, ' '),
        ('WdLcdInt', -40, 90, ' '), ('WdButtonSwitch', 180, 120, ' '), ('WdLcdFloat', -40, 150, ' '),
        ('WdSpinbox', 180, 200, ' '), ('WdLcdHex', -40, 210, ' '), ('WdLcdBin', -40, 270, ' '),
        ('WdProgressBar', -40, 360, ' ')
    )

control = (
         'Control',
        ('Solver_RK2', 80, 0, 'RK2'), ('Solver_RT2', 160, 0, 'RT2'),
        ('Control_PPC', 0, 0, 'PPC'),
        ('WdLcdTime', 0, 160, ' ')
    )

complx = (
        'Complex',
        ('ConstComplex', 0, 0, 'Complex'), ('Complex2XY', 80, 0, 'C-XY'), ('XY2Complex', 80, 80, 'XY-C'),
        ('Complex2RP', 160, 0, 'C-RP'), ('RP2Complex', 160, 80, 'RP-C'),
    )

decorations = (
         'Decorations',
        ('ImagePNG', 0, 0, ' '),
        ('DecorationText', 0, 120, ' '),
        ('DecorationFileName', 0, 150, ' '),
        ('DecorationTime', 0, 180, ' '),
        ('ImageLaTex', 150, 100, ' '),
        ('ImageSVG', 150, 170, ' ')
    )

solar = (
         'Solar',
        ('Azimut', 0, 0), ('Altitude', 100, 0), ('Radiation', 200, 0), ('IncidenceAngle', 300, 0),
        ('Date2Epoch', 0, 100), ('Epoch2Date', 0, 180),
    )

aor = (
         'AOR',
        ('AR_Antenna', 30, 0), ('AR_AntGain', 130, 0), ('AR_Control', 220, 0),
        ('AR_Frequency', 0, 100),
        ('AR_Spectrogram', 0, 160),
        ('AR_Spectrum', 0, 380)
    )

electric = (
         'Electric',
        ('ResH', 0, 0, ' '), ('Gnd', 80, 0, ' '), ('Npn', 120, 0, ' '),
        ('CapH', 0, 60, ' '), ('Vcc', 80, 80, ' '), ('Pnp', 120, 80, ' '),
        ('ResV', 0, 150, ' '), ('IndV', 80, 150, ' '), ('Diode', 140, 180, ' '),
        ('CapV', 0, 240, ' '), ('Opamp', 120, 240, ' '), ('NetIn', 20, 300, ' '),
        ('NetOut', -30, 330, ' ')
    )

# library config - list of visible pages
libConfig = [sources, sinks, signal, linear, nonlinear, control, discrete,
             interactive, complx, decorations,  electric, aor,  solar
             ]


class ComponentViewer(QGraphicsScene):
    '''
    Zjednoduseny prehliadac komponentov, zobrazuje komponenty v zozname
    a podporuje drag & drop.
    '''

    def __init__(self, parent=None):
        super(ComponentViewer, self).__init__()
        self.parent = parent
        self.gridType = GRID.DOT  # typ mriezky
        self.gridShow = True	 # zobrazenie mriezky

        self.componentList = []	 # zoznam komponentov na ploche
        self.activeComponent = None  # referencia na vybrany/posuvany komponent
        self.setGrid(self.gridType)

    def dropEvent(self, event):
        event.accept()

    def dragEnterEvent(self, event):
        event.accept()

    def dragMoveEvent(self, event):
        event.accept()

    def setGrid(self, gridType):
        '''
        Nastavenie typu mriezky.
        '''
        if gridType == GRID.NONE:
            self.setBackgroundBrush(QBrush(QPixmap(None)))
        elif gridType == GRID.LINE:
            self.setBackgroundBrush(QBrush(QPixmap('./images/grid_01.png')))
        elif gridType == GRID.LINE_BIG:
            self.setBackgroundBrush(QBrush(QPixmap('./icons/grid_03.png')))
        elif gridType == GRID.DOT:
            self.setBackgroundBrush(QBrush(QPixmap('./icons/grid_02.png')))

        self.gridType = gridType
        self.update()

    def mousePressEvent(self, event):

        for q in self.componentList:
            q.setSelected(False)
            self.activeComponent = None

        x = event.scenePos().x()
        y = event.scenePos().y()

        t = QTransform()
        self.activeComponent = self.itemAt(x, y, t)

        if isinstance(self.activeComponent, Component) is True:
            self.activeComponent.setSelected(True)

    def mouseMoveEvent(self, event):
        '''
        '''
        if event.buttons() == Qt.LeftButton:

            if isinstance(self.activeComponent, Component) is True:
                mimeData = QMimeData()
                mimeData.setText(self.activeComponent.className)

                drag = QDrag(self.parent)
                drag.setMimeData(mimeData)
                drag.exec_(Qt.CopyAction)

    def mouseReleaseEvent(self, event):
        pass

    def addComponent(self, compClassName, x, y, description=''):
        '''
        Zaradenie komponentu do zoznamu. Vytvori novy objekt na zaklade mena triedy.
        TODO - doplnit vynimku, vypis chyby pri beznej chybe v konstruktore objektu
        '''
        # constructor = globals()[compClassName]
        constructor = getattr(lib, compClassName)
        component = constructor(compClassName, QPoint(x, y))
        self.componentList.append(component)
        self.addItem(component)
        # zobrazenie mena komponentu v kniznici
        # 1. rozmery komponentu
        box = component.box
        # 2. uprava parametra 'Ref' pre zobrazenie v kniznici
        #    povolenie zobrazenia parametra a uprava polohy
        if description == '':
            component.parameter['Ref'].value = compClassName
        else:
            component.parameter['Ref'].value = description
        component.parameter['Ref'].visibleValue = True
        component.parameter['Ref'].position = QPoint(0, box.height() / 2 + 5)
        component.parameter['Ref'].font = QFont('Decorative', 9)
        component.parameter['Ref'].font.setItalic(True)
        component.parameter['Ref'].color = Color.firebrick
        component.updateShape()

        self.update()
        return component


class Library(QMainWindow):
    '''
    '''

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.centralWidget = QWidget()
        self.resize(800, 500)
        self.setWindowTitle('Library')

        self.tabs = QTabWidget()

        # konfiguracia tab-u
        for p in libConfig:
            diagram = ComponentViewer(self)
            view = QGraphicsView(diagram)
            diagram.compLock = True

            for i in range(1, len(p)):
                if len(p[i]) == 3:        # nezadany popis
                    c = diagram.addComponent(p[i][0], p[i][1], p[i][2])
                else:
                    c = diagram.addComponent(p[i][0], p[i][1], p[i][2], p[i][3])

                c.setFlag(QGraphicsItem.ItemIsMovable, False)

            tab = QWidget()
            layout = QVBoxLayout()
            layout.addWidget(view)
            tab.setLayout(layout)

            self.tabs.addTab(tab, p[0])		# pridanie tabu, nazov

        layout = QHBoxLayout()
        layout.addWidget(self.tabs)
        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.setCentralWidget(self.widget)

if __name__ == '__main__':
    import sys
    import logging
    logging.basicConfig()
    app = QApplication(sys.argv)

    # spustenie kniznice - moze byt spustena ako nezavisla aplikacia
    library = Library()
    library.setGeometry(20, 20, 400, 500)
    library.show()

    app.exec_()
    sys.exit()
