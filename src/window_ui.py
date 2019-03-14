# -*- coding: utf-8 -*-

import six

from diagram import GRID


if six.PY2:
    from PyQt4.QtGui import *  # @UnusedWildImport
    from PyQt4.QtCore import *  # @UnusedWildImport
else:
    from PyQt5.QtWidgets import *  # @UnusedWildImport
    from PyQt5.QtGui import *  # @UnusedWildImport
    from PyQt5.QtCore import *  # @UnusedWildImport


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.parent = MainWindow
        self.create_actions()
        self.createMenu()
        self.createToolbars()

    def create_actions(self):
        parent = self.parent
        icon = QIcon.fromTheme("window-new")
        self.ActionNewFile = QAction(icon, "New", parent,
                                     shortcut=QKeySequence.New,
                                     statusTip="New diagram",
                                     triggered=parent.newDiagram)

        icon = QIcon('./icons/icon32_new_win.png')
        self.ActionNewWindow = QAction(icon, "New window", parent,
                                       shortcut="Ctrl+W",
                                       statusTip="New diagram window",
                                       triggered=parent.newDiagramWindow)

        self.ActionSaveFile = QAction("Save", parent,
                                      shortcut=QKeySequence.Save,
                                      statusTip="Save file",
                                      triggered=parent.saveDiagram)
        self.ActionSaveFile.setIcon(QIcon.fromTheme("document-save"))

        self.ActionSaveAsFile = QAction("Save As", parent,
                                        shortcut=QKeySequence.SaveAs,
                                        statusTip="Save file as ..",
                                        triggered=parent.saveAsDiagram)
        self.ActionSaveAsFile.setIcon(QIcon.fromTheme("document-save-as"))

        self.ActionLoadFile = QAction("Open", parent,
                                      shortcut=QKeySequence.Open,
                                      statusTip="Load file",
                                      triggered=parent.openDiagramDialog)
        self.ActionLoadFile.setIcon(QIcon.fromTheme("document-open"))

        self.ActionExit = QAction("E&xit", parent,
                                  shortcut=QKeySequence.Quit,
                                  statusTip="Quit program",
                                  triggered=parent.close)
        self.ActionExit.setIcon(QIcon.fromTheme("application-exit"))

        self.ActionAbout = QAction("A&bout", parent,
                                   shortcut="Ctrl+B",
                                   triggered=parent.about)
        self.ActionAbout.setIcon(QIcon.fromTheme("help-about"))

        self.ActionExportImage = QAction("Export Image", parent,
                                         shortcut=QKeySequence.Print,
                                         statusTip="Export Image",
                                         triggered=parent.exportImage)

        # Net act_lst
        icon = QIcon('./icons/icon32_add_net.png')
        self.ActionAddNet = QAction(icon, "Add &net", parent,
                                    shortcut="",
                                    statusTip="Add net to diagram",
                                    triggered=parent.addNet)

        icon = QIcon('./icons/icon32_add_vertex.png')
        self.ActionAddVertex = QAction(icon, "&Add vertex", parent,
                                       shortcut="",
                                       statusTip="Add new vertex to net",
                                       triggered=parent.addVertex)

        icon = QIcon('./icons/icon32_del_vertex.png')
        self.ActionDelVertex = QAction(icon, "&Delete vertex", parent,
                                       shortcut="",
                                       statusTip="Delete vertex from net",
                                       triggered=parent.delVertex)

        # Connection act_lst
        icon = QIcon('./icons/icon32_add_connection.png')
        self.ActionAddConnection = QAction(icon, "&Add connection", parent,
                                           shortcut="",
                                           statusTip="Add new connection to net",
                                           triggered=parent.addConnection)

        # Component act_lst
        icon = QIcon('./icons/icon32_del_component.png')
        self.ActionDelComponent = QAction(icon, "&Del component", parent,
                                          shortcut="",
                                          statusTip="Delete component from diagram",
                                          triggered=parent.delComponent)

        icon = self.icon(theme="input-mouse",
                         alt='./icons/icon32_move_component.png')
        self.ActionMoveComponent = QAction(icon, "&Move component", parent,
                                           shortcut="",
                                           statusTip="Move component",
                                           triggered=parent.move)

        icon = QIcon('./icons/icon32_front_component.png')
        self.ActionFrontComponent = QAction(icon, "Component to front", parent,
                                            shortcut="",
                                            statusTip="Move component to front",
                                            triggered=parent.frontComponent)

        icon = QIcon('./icons/icon32_back_component.png')
        self.ActionBackComponent = QAction(icon, "Component to back", parent,
                                           shortcut="",
                                           statusTip="Move component to back",
                                           triggered=parent.backComponent)

        icon = self.icon(theme="object-rotate-left",
                         alt='./icons/icon32_rotate_left.png')

        _act = QAction(icon, "Rotate left", parent,
                       shortcut="",
                       statusTip="Rotate component to left",
                       triggered=parent.rotateLeft)
        self.ActionRotateLeftComponent = _act

        icon = self.icon(theme="object-rotate-right",
                         alt='./icons/icon32_rotate_right.png')
        _act = QAction(icon, "Rotate right", parent,
                       shortcut="",
                       statusTip="Rotate component to right",
                       triggered=parent.rotateRight)
        self.ActionRotateRightComponent = _act

        icon = self.icon(theme="object-flip-horizontal",
                         alt='./icons/icon32_flip_horizontal.png')
        _act = QAction(icon, "Flip horizontal", parent, shortcut="",
                       statusTip="Flip component horizontal",
                       triggered=parent.flipHorizontal)
        self.ActionFlipHorizontalComponent = _act

        icon = self.icon(theme="object-flip-vertical",
                         alt='./icons/icon32_flip_vertical.png')

        _act = QAction(icon, "Flip vertical", parent, shortcut="",
                       statusTip="Flip component vertical",
                       triggered=parent.flipVertical)
        self.ActionFlipVerticalComponent = _act

        icon = QIcon.fromTheme("document-properties")
        _act = QAction(icon, "Properties", parent,
                       shortcut="",
                       statusTip="Edit component properties",
                       triggered=parent.editComponentProperties)
        self.ActionEditComponent = _act

        # Simulator act_lst
        icon = self.icon(theme="media-playback-start",
                         alt='./icons/icon32_run.png')
        self.ActionSimStart = QAction(icon, "Start", parent, shortcut="CTRL+1",
                                      statusTip="Start simulation",
                                      triggered=parent.simStart)

        icon = self.icon(theme="media-playback-stop",
                         alt='./icons/icon32_stop.png')

        self.ActionSimStop = QAction(icon, "Stop", parent, shortcut="CTRL+2",
                                     statusTip="Stop simulation",
                                     triggered=parent.simStop)

        icon = QIcon.fromTheme("media-eject")
        self.ActionSimReset = QAction(icon, "Reset", parent, shortcut="CTRL+3",
                                      statusTip="Reset simulation and clean results",
                                      triggered=parent.simReset)

    def icon(self, theme, alt=''):
        '''return Qicon from theme.
        If does't exist in theme, construct icon from alt parameter
        method is needed because in MS Windows theme does't work

        :param theme: theme string
        :param alt: string with path to the icon
        '''
        icon = QIcon.fromTheme(theme)
        if icon.isNull():
            icon = QIcon(alt)
        return icon

    def createToolbars(self):
        '''!
        @if English

        @endif

        @if Slovak

        @endif
        '''
        parent = self.parent
        self.editToolBar = parent.addToolBar("Component")
        # velkost ikon je specificka pre kazdy toolbar
        self.editToolBar.setIconSize(QSize(24, 24))
        self.editToolBar.addAction(self.ActionNewWindow)
        # self.editToolBar.addAction(self.act_lst.delComponent)
        self.editToolBar.addAction(self.ActionMoveComponent)
        # self.editToolBar.addAction(self.act_lst.frontComponent)
        # self.editToolBar.addAction(self.act_lst.backComponent)
        self.editToolBar.addAction(self.ActionRotateLeftComponent)
        self.editToolBar.addAction(self.ActionRotateRightComponent)
        self.editToolBar.addAction(self.ActionFlipHorizontalComponent)
        self.editToolBar.addAction(self.ActionFlipVerticalComponent)

        self.gridToolBar = self._mk_grid_toolbar()
        parent.addToolBar(self.gridToolBar)

        self.netToolBar = QToolBar("Net")
        self.netToolBar.setIconSize(QSize(36, 36))
        self.netToolBar.addAction(self.ActionAddNet)
        self.netToolBar.addAction(self.ActionAddVertex)
        self.netToolBar.addAction(self.ActionDelVertex)
        self.netToolBar.addAction(self.ActionAddConnection)
        parent.addToolBar(Qt.LeftToolBarArea, self.netToolBar)

        self.simToolBar = parent.addToolBar("Simulation")
        self.simToolBar.setIconSize(QSize(24, 24))
        self.simToolBar.addAction(self.ActionSimStart)
        self.simToolBar.addAction(self.ActionSimStop)
        # self.simToolBar.addAction(self.ActionSimReset)

    def createMenu(self):
        '''PSE window menu'''
        parent = self.parent
        menu_file = parent.menuBar().addMenu('&File')
        menu_edit = parent.menuBar().addMenu("&Edit")
        menu_sim = parent.menuBar().addMenu("&Simulation")
        menu_window = parent.menuBar().addMenu('&Window')
        menu_about = parent.menuBar().addMenu("&Help")

        menu_file.addAction(self.ActionNewFile)
        menu_file.addAction(self.ActionNewWindow)
        menu_file.addSeparator()
        menu_file.addAction(self.ActionLoadFile)

        act = QAction('Recent files', parent)
        act.setIcon(QIcon.fromTheme("document-open-recent"))
        menu_file.addAction(act)
        self.recent = QMenu()
        act.setMenu(self.recent)

        menu_file.addSeparator()
        menu_file.addAction(self.ActionSaveFile)
        menu_file.addAction(self.ActionSaveAsFile)
        menu_file.addSeparator()
        menu_file.addAction(self.ActionExportImage)
        menu_file.addAction('Page Setup')
        menu_file.addAction('Print')
        menu_file.addSeparator()
        menu_file.addAction(self.ActionExit)

        menu_edit.addAction(self.ActionAddNet)
        menu_edit.addSeparator()
        menu_edit.addAction(self.ActionAddVertex)
        menu_edit.addAction(self.ActionDelVertex)

        menu_sim.addAction(self.ActionSimStart)
        menu_sim.addAction(self.ActionSimStop)
        menu_sim.addAction(self.ActionSimReset)

        show_lib = QAction("Liblary", parent,
                           statusTip="Show Liblary",
                           triggered=parent.show_libwindow)

        menu_window.addAction(show_lib)
        menu_about.addAction(self.ActionAbout)

    def _mk_grid_toolbar(self):
        '''create toolbar with grid act_lst'''
        parent = self.parent
        bar = QToolBar("Grid")
        bar.setIconSize(QSize(32, 32))

        grid_none = QAction(QIcon('./icons/icon32_show_grid.png'),
                            "Hide &grid", parent,
                            statusTip="Hide diagram grid")
        grid_none.setData(GRID.NONE)

        grid_line = QAction(QIcon('./icons/icon32_grid_10.png'),
                            "Set grid 10x10", parent,
                            statusTip="Set grid 10x10 pixels")
        grid_line.setData(GRID.LINE)

        grid_linebig = QAction(QIcon('./icons/icon32_grid_20.png'),
                               "Set grid 20x20", parent,
                               statusTip="Set grid 20x20 pixels")
        grid_linebig.setData(GRID.LINE_BIG)

        grid_dot = QAction(QIcon('./icons/icon32_grid_dot.png'),
                           "Set grid dot", parent,
                           statusTip="Set grid 20x20 pixels")
        grid_dot.setData(GRID.DOT)

        grid_none.setCheckable(True)
        grid_line.setCheckable(True)
        grid_linebig.setCheckable(True)
        grid_dot.setCheckable(True)

        grid_line.setChecked(True)  # this is pressed by default

        # add grid type act_lst to the ActionGroup
        group = QActionGroup(parent)
        group.addAction(grid_line)
        group.addAction(grid_linebig)
        group.addAction(grid_dot)
        group.addAction(grid_none)
        group.triggered.connect(parent._setGridAction)

        snap2grid = QAction(QIcon('./icons/icon32_snap_grid.png'),
                            "Snap to g&rid", parent,
                            statusTip="Snap component to grid",
                            triggered=parent._snapGrid)
        snap2grid.setCheckable(True)
        snap2grid.setChecked(True)  # pressed by default

        # add act_lst to the toolbar
        for gridaction in group.actions():
            bar.addAction(gridaction)

        bar.addSeparator()
        bar.addAction(snap2grid)
        return bar
