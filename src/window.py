# -*- coding: utf-8 -*-
import logging
import os
import time

import six

from component import Component
from componenttypes import *  # @UnusedWildImport
from diagram import Diagram, MODE
from dialogs.blockproperties import CompProperties
from net import Net
from sim.simulator import SimulatorEngine
import math
from library import Library
from window_ui import Ui_MainWindow


if six.PY2:
    from PyQt4.QtGui import *  # @UnusedWildImport
    from PyQt4.QtCore import *  # @UnusedWildImport
else:
    from PyQt5.QtWidgets import *  # @UnusedWildImport
    from PyQt5.QtGui import *  # @UnusedWildImport
    from PyQt5.QtCore import *  # @UnusedWildImport

MAX_RECENT = 10  # File->Recent
LOG = logging.getLogger(__name__)


class MyQGraphicsView(QGraphicsView):
    '''Zoom-able GraphicsView'''
    _xscale = 1

    def wheelEvent(self, event):
        '''zoom on Ctrl + mouse wheel'''
        if Qt.ControlModifier == QApplication.keyboardModifiers():
            if six.PY2:
                delta = event.delta()  # Qt4
            else:
                delta = event.angleDelta().y()  # Qt5
            self.set_zoom(delta)
            event.accept()
        else:
            event.ignore()
            super(MyQGraphicsView, self).wheelEvent(event)

    def keyPressEvent(self, event):
        '''set zoom via keyboard
             Ctrl +  increase
             Ctrl -  decrease
             Ctrl+0  100%
        '''
        accepted = False
        if int(event.modifiers()) & Qt.ControlModifier:
            if event.key() == Qt.Key_0:
                accepted = True
                self._xscale = 1
                self.resetTransform()
            if event.key() == Qt.Key_Plus:
                accepted = True
                delta = 120
                self.set_zoom(delta)

            if event.key() == Qt.Key_Minus:
                accepted = True
                delta = -120
                self.set_zoom(delta)

        if accepted:
            event.accept()
        else:
            event.ignore()

    def set_zoom(self, delta):
        factor = math.pow(2.0, delta / 1000.0)
        if self._xscale * factor > 0.4 and self._xscale * factor < 6:
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.scale(factor, factor)
            self._xscale = self._xscale * factor


class MainPseWindow(QMainWindow):
    '''
    @if English

    Main application window.

    @endif

    @if Slovak

    Hlavne okno aplikacie.

    Ovladacie klavesy a skratky editora diagramov.

    ESC - Cancel action
    DEL - Delete selected component or net
    C   - Copy component
    M   - Move
    N   - Add net
    R   - Rotate right
    L   - Rotate left

    CTRL+1 	Start simulatora / generatora
    CTRL+2	Stop simulatora
    CTRL+3	Stop simulatora a reset komponentov

    @endif
    '''

    def __init__(self, fileName='', parent=None):
        super(MainPseWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        layout = QHBoxLayout()  # horizontal box layout

        self.view = MyQGraphicsView(self)
        self.diagram = Diagram(self)  # Diagram is QGraphicsScene
        self.view.setScene(self.diagram)  # set scene to the view

        self.view.setSceneRect(QRectF(-2000, -2000, 4000, 4000))
        self.view.centerOn(QPointF(0, 0))		# pociatocna poloha
        # vyvolanie mouseMoveEvent pri kazdom pohybe mysi
        self.view.setMouseTracking(True)

        # self.view.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        layout.addWidget(self.view)

        self.widget = QWidget()
        self.widget.setLayout(layout)
        self.widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setCentralWidget(self.widget)

        self.widget.customContextMenuRequested.connect(self.createContextMenu)

        self.fileName = fileName  # inicializacia diagramu pri zadanom mene diagramu
        if self.fileName == '':
            self.setWindowTitle('Untitled.pse')
        else:
            self.diagram.diagramLoad(self.fileName)
            self.setWindowTitle(self.fileName)

        self.setWindowIcon(QIcon('./icons/ikona_pse_128x128.png'))

        self.simEngine = None

        self.recentFileActs = []
        self.init_recent_files()

        self.setStatusBar(QStatusBar(self))
        self.lib_win = None  # Liblary window

    def createContextMenu(self):
        '''create and show context menu for component'''
        menu = QMenu(self)
        menu.addAction(self.ui.ActionEditComponent)
        menu.addSeparator()
        menu.addAction(self.ui.ActionRotateLeftComponent)
        menu.addAction(self.ui.ActionRotateRightComponent)
        menu.addSeparator()
        menu.addAction(self.ui.ActionFlipHorizontalComponent)
        menu.addAction(self.ui.ActionFlipVerticalComponent)
        menu.exec_(QCursor.pos())

    def _setGridAction(self, action):
        '''set diagram grid according to action data'''
        grid_type = action.data()
        self.diagram.setGrid(grid_type)  # hide

    def _snapGrid(self, checked):
        '''set/unset snapping on the grid, according action button'''
        self.diagram.snapOnGrid = checked

    def saveDiagram(self):
        '''!
        @if English

        @endif

        @if Slovak

        Uloženie diagramu.

        V prípade nezadaného mena vyvolá štandardný dialóg pre zadanie mena a cesty
        a uloženie diagramu do súboru.

        @endif
        '''
        self.diagram.mode = MODE.MOVE
        # Reset vsetkych komponentov, zmazanie poli v hodnotach parametrov (ukladali by sa do suboru)
        for comp in self.diagram.componentList:
            comp.sim(SIM_RESET, 0, 0, 0)

        if self.fileName == '':
            data = QFileDialog.getSaveFileName(self, 'Save', '..', filter='*.pse')
            self.fileName = data[0]

        # kontrola na nezadane meno suboru
        if self.fileName != '':

            if self.fileName.endswith('.pse') is False:
                self.fileName = self.fileName + '.pse'

            self.diagram.diagramSave(self.fileName)
            self.setWindowTitle(self.fileName)

    def saveAsDiagram(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.MOVE
        # Reset vsetkych komponentov, zmazanie poli v hodnotach parametrov (ukladali by sa do suboru)
        for comp in self.diagram.componentList:
            comp.sim(SIM_RESET, 0, 0, 0)

        data = QFileDialog.getSaveFileName(
            self, 'Save As', '..', filter='*.pse')
        self.fileName = data[0]

        if self.fileName != '':
            self.fileName = self.fileName.replace('.txt', '.pse')

            if self.fileName.endswith('.pse') is False:
                self.fileName = self.fileName + '.pse'

            self.diagram.diagramSave(self.fileName)
            self.setWindowTitle(self.fileName)

    def openDiagramDialog(self):
        self.diagram.mode = MODE.MOVE

        filename = QFileDialog.getOpenFileName(self, 'Open', '..',
                                               filter='*.txt *.pse')
        if isinstance(filename, tuple):
            filename = filename[0]  # cut the filter
        if filename:
            self.loadDiagram(filename)

    def loadDiagram(self, filename):
        if self.fileName != '':
            self.diagram.deleteAll()

        self.fileName = filename
        self.diagram.diagramLoad(filename)
        self.setWindowTitle(filename)
        self.add_to_recent(filename)

    def exportImage(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.MOVE

        fileName = QFileDialog.getSaveFileName(self, 'Save image', '..',
                                               filter='*.png')
        fn = fileName[0]

        if fn is not None:
            if not fn.endswith('.png'):
                fn = fn + '.png'

            if six.PY2:
                geometry = self.view.viewport().geometry()
                rect = self.view.mapToScene(geometry).boundingRect()
                pixMap = QPixmap.grabWidget(self.view, x=0, y=0,
                                            width=rect.width(),
                                            height=rect.height())
            else:
                pixMap = self.view.grab()
            pixMap.save(fn)

    def simStart(self):
        '''!
        @if English

        @endif

        @if Slovak

        Spustenie simulacie.

        Funkcia vytvori objekt simulatora a spusti simulaciu. Na zaciatku simulacie
        su reinicializovane zoznamy prepojeni a komponentov. V pripade prebiehajucej
        simulacie sa simulacia restartuje.

        @todo simulacia viacerych diagramov spojenie zoznamov komponentov a prepojeni

        @endif
        '''
        self.diagram.mode = MODE.SIMULATION

        if self.simEngine:
            self.simEngine.stopSimulation()

        self.simEngine = SimulatorEngine(self.diagram)
        self.simEngine.startSimulation()

        return self.simEngine

    def simStop(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        if self.simEngine is not None:
            self.simEngine.stopSimulation()
            time.sleep(0.3)  # cakanie na bezpecne ukoncenie threadu
            self.simEngine = None

        self.diagram.mode = MODE.MOVE

    def simReset(self):
        """!
        @if English

        @endif

        @if Slovak

        Zastavenie prebiehajucej simulacie a reset vsetkych komponentov.

        @endif
        """
        self.diagram.mode = MODE.MOVE

        # 1. zastavenie simulacie
        if self.simEngine is not None:
            self.simEngine.stopSimulation()
            time.sleep(0.3)  # cakanie na bezpecne ukoncenie threadu
            self.simEngine = None

        # 2. reset vsetkych komponentov, prip. re-inicializacia terminalov
        for comp in self.diagram.componentList:
            comp.sim(SIM_RESET, 0, 0, 0)

    def newDiagramWindow(self):
        '''!
        @if English

        @endif

        @if Slovak

        Funkcia otvorí nové okno pre diagram.

        @endif
        '''
        self.diagram.mode = MODE.MOVE

        self.newWindow = MainPseWindow('')
        self.newWindow.setGeometry(120, 120, 800, 500)
        self.newWindow.show()

    def newDiagram(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.MOVE
        # @todo - v pripade existujuceho diagramu dialog o ulozeni diagramu ...
        # ukoncenie simulacie
        self.simReset()

        # zmazanie vsetkych komponentov
        self.diagram.deleteAll()

        self.fileName = ''
        self.setWindowTitle('Untitled.pse')

    def rotateLeft(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.rotateComponentLeft()

        self.diagram.mode = MODE.MOVE

    def rotateRight(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.rotateComponentRight()
        self.diagram.mode = MODE.MOVE

    def flipHorizontal(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.MOVE
        self.diagram.flipComponentHorizontal()

    def flipVertical(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.MOVE
        self.diagram.flipComponentVertical()

    def delComponent(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.MOVE

        for item in self.diagram.selectedItems():
            self.diagram.deleteComponent(item)
        self.diagram.update()

    def move(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.MOVE
        print('mode move')

    def frontComponent(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        pass

    def backComponent(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        pass

    def addNet(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.ADD_NEW_NET

    def delNet(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        for net in self.diagram.netList:
            if net.isActive is True:
                self.diagram.deleteNet(net)

    def selNet(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.SELECT_NET

    def addVertex(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.INSERT_VERTEX

    def delVertex(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.DELETE_VERTEX

    def moveVertex(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.MOVE

    def addConnection(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        self.diagram.mode = MODE.ADD_JUNCTION

    def about(self):
        '''show about dialog'''
        s = "The <b>pse</b> is simple python simulator and block editor<br>" \
            "<br>Project of Research Centre University of Zilina<br>" \
            "Zilina, Slovak Republic<br>" \
            "<b>E-mail</b> info@vyskumnecentrum.sk<br>" \
            "<b>Version</b> 151214_0.11<br>"
        QMessageBox.about(self, "About pse", s)

    def editComponentProperties(self):
        '''Open Component Properties dialog on active component'''
        comp = self.diagram.activeComponent

        if not isinstance(comp, Component):
            LOG.debug('Cannot edit: %s' % comp)
            return

        if comp:
            # vypocet polohy okna pre editovanie vlastnosti komponentu
            # okno sa nachadza v blizkosti polohy komponentu
            winPos = self.view.mapFromScene(
                QPoint(comp.position.x(), comp.position.y())) + self.pos()
            w = CompProperties(comp, winPos, self)
            w.show()

        self.diagram.mode = MODE.MOVE

    def closeEvent(self, event):
        '''!
        @if English

        @endif

        @if Slovak

        Ukoncenie aplikacie.

        Pri ukonceni aplikacie sa zastavi prebiehajuca simulacia.

        @todo - kontrola na neulozeny subor

        @endif
        '''

        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # ukoncenie simulacie
            self.simReset()

            # zmazanie vsetkych komponentov a ukoncenie refresovacieho threadu
            self.diagram.deleteAll()
            self.diagram.stopRefresh()
            if self.lib_win:
                self.lib_win.close()  # close liblary
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):
        key = event.key()

        if key == Qt.Key_Escape:
            print('>>> Key event - ESC - Cancel action')
            self.diagram.cancelAction()

        elif key == Qt.Key_C:
            print('>>> Key event - C - Copy action')
            self.diagram.copyComponent()

        elif key == Qt.Key_M:
            print('>>> Key event - M - Move ')
            self.move()

        elif key == Qt.Key_N:
            print('>>> Key event - N - Add net ')
            self.addNet()

        elif key == Qt.Key_R:
            print('>>> Key event - R - Rotate right')
            self.diagram.rotateComponentRight()

        elif key == Qt.Key_L:
            print('>>> Key event - L - Rotate left')
            self.diagram.rotateComponentLeft()

        elif key == Qt.Key_Q:
            print('>>> Key event - Q - Component list dump')
            for comp in self.diagram.componentList:
                print(comp)

        elif key == Qt.Key_W:
            print('>>> Key event - W - Net list dump')
            for net in self.diagram.netList:
                print(net)

        elif key == Qt.Key_Delete:
            print('>>> Key event - DEL - Delete')
            for item in self.diagram.selectedItems():
                if isinstance(item, Component):
                    self.diagram.deleteComponent(item)

                elif isinstance(item, Net):
                    self.diagram.deleteNet(item)

        self.diagram.update()

    def init_recent_files(self):
        '''inicialization of File->Recent'''
        for _ in range(MAX_RECENT):
            act = QAction(self, visible=False,
                          triggered=self.__openRecentFile)
            self.ui.recent.addAction(act)
            self.recentFileActs.append(act)
        self._updateRecentFileActions()

    def _updateRecentFileActions(self):
        ''' '''
        settings = QSettings("PSE", 'data')
        recent = settings.value("recent", defaultValue=[])
        numRecentFiles = min(len(recent), MAX_RECENT)

        for i in range(numRecentFiles):
            path = recent[i]
            filename = os.path.basename(path)
            text = "&%d  %s" % (i + 1, filename)
            act = self.recentFileActs[i]
            act.setText(text)
            act.setData(path)
            act.setVisible(True)
            act.setStatusTip('%s' % path)
            icon = QIcon('./icons/ikona_pse_128x128.png')
            act.setIcon(icon)

    def add_to_recent(self, filename):
        '''remember current file to the recent files '''
        settings = QSettings("PSE", 'data')
        recent = settings.value("recent", defaultValue=[])
        try:
            recent.remove(filename)
        except ValueError:
            pass
        recent.insert(0, filename)
        settings.setValue('recent', recent)
        settings.sync()
        self._updateRecentFileActions()

    def __openRecentFile(self):
        '''open choosed diagram from recent files'''
        action = self.sender()
        filename = str(action.data())
        self.loadDiagram(filename)

    def show_libwindow(self):
        '''Show liblary window'''
        if not self.lib_win:
            self.lib_win = Library()
            self.lib_win.setGeometry(20, 20, 400, 500)
        self.lib_win.show()


if __name__ == '__main__':
    import sys
    logging.basicConfig()
    app = QApplication(sys.argv)
    form = MainPseWindow()
    form.show()
    app.exec_()
    sys.exit()
