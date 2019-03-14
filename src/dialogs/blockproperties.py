import os
import six

from dialogs.properties_ui import Ui_Dialog
import logging
import inspect
from component import PARAM

if six.PY2:
    from PyQt4.QtGui import *  # @UnusedWildImport
    from PyQt4.QtCore import *  # @UnusedWildImport
else:
    from PyQt5.QtWidgets import *  # @UnusedWildImport
    from PyQt5.QtGui import *  # @UnusedWildImport
    from PyQt5.QtCore import *  # @UnusedWildImport

LOG = logging.getLogger(__name__)


class ParamLine(QObject):
    '''responsible for one row = one parameter'''
    def __init__(self, parent, param):
        '''provide 6 widgets, so they can be added to layout (outside)

        :param parent: parent widget
        :param param: component parameter, instance of
        '''
        super(ParamLine, self).__init__(parent)
        self.param = param

        # 1. col - parameter name
        self.q1 = QLabel(param.name)

        # 2. col - parameter value
        # standard types are:  STR, INT, FLOAT
        if PARAM.INT == self.param.paramType:
            self.q2 = QSpinBox()
            self.q2.setRange(-2147483647, 2147483647)
            self.q2.setValue(param.value)

        elif PARAM.BOOL == self.param.paramType:
            self.q2 = QCheckBox()
            self.q2.setChecked(param.value)

        else:
            # default to line edit
            self.q2 = QLineEdit(str(param.value))

        if self.param.name == 'Ref':
            self.q2.setEnabled(False)  # do not change reference

        # (optional) button to open select file dialog
        self.q3 = QPushButton('...')
        self.q3.hide()  # is hidden by default
        self.q3.setMaximumWidth(30)
        self.q3.clicked.connect(self.buttonEditFileName)
        if param.paramType >= PARAM.FILE:
            self.q3.show()

        # 4. col - set parameter value visibility
        self.q4 = QCheckBox()
        self.q4.setChecked(param.visibleValue)

        # 5. col - set parameter name visibility
        self.q5 = QCheckBox()
        self.q5.setChecked(param.visibleName)

        # 6. column - button to set parameter color
        self.q6 = QPushButton()
        self.q6.setFlat(True)
        self.q6.setMaximumSize(16, 16)  # rozmery tlacitka
        pal = QPalette(self.q6.palette())  # kopia existujucej palety
        # nastavenie farby - vyber podla vlastnosti
        pal.setColor(QPalette.Button, param.color)
        self.q6.setPalette(pal)  # priradenie novej palety
        self.q6.setAutoFillBackground(True)
        self.q6.clicked.connect(self.colButtonClick)

    def buttonEditFileName(self):
        '''open file dialog and set property'''
        # TODO: open dialogs in the dir where file is
        title = 'no title'
        filt = '*.*'
        if self.param.paramType == PARAM.FILE:
            filt = '*.*'
        if self.param.paramType == PARAM.FILE_CSV:
            title = 'CSV file'
            filt = '*.csv, *.txt'
        if self.param.paramType == PARAM.FILE_PNG:
            title = 'PNG image'
            filt = '*.png'
        if self.param.paramType == PARAM.FILE_PSE:
            title = 'Diagram File'
            filt = '*.pse'
        if self.param.paramType == PARAM.FILE_SVG:
            title = 'SVG image'
            filt = '*.svg'

        elif self.param.paramType == PARAM.IMAGE:
            filt = '*.svg *.png'
            title = 'Image'

        mydir = '.'
        try:
            mydir = os.path.relpath(self.q2.text())
            # if possible, then dialog will be opened with last file position
        except Exception:
            pass

        # normal 'open dialog'
        _getFilenameDlg = QFileDialog.getOpenFileName

        if self.param.paramType == PARAM.FILE_CSV_SAVE:
            title = 'CSV file'
            filt = '*.csv'
            # we have to use dialog to save file
            _getFilenameDlg = QFileDialog.getSaveFileName

        filename = _getFilenameDlg(self.parent(), title, mydir, filt)

        if isinstance(filename, tuple):
            filename = filename[0]  # cut the filter
        if filename:
            filename = os.path.relpath(filename)  # vytvorenie relativnej cesty
            self.q2.setText(filename)

    def colButtonClick(self):
        '''set the color when click to color button'''
        pal = QPalette(self.q6.palette())  # make a copy of the palette

        col = QColorDialog.getColor()
        pal.setColor(QPalette.Button, col)
        self.q6.setPalette(pal)

    def write_parameter(self):
        '''write values from widgets to the parameter'''
        # param.value
        # param.visibleValue
        # param.visibleName
        # param.color
        # param.name    <unchanged>
        # param.paramType  <unchanged>

        # konverzia/uprava typu, string je default
        if self.param.paramType in [PARAM.STRING, PARAM.IMAGE, PARAM.FILE]:
            val = str(self.q2.text())
        elif PARAM.INT == self.param.paramType:
            val = self.q2.value()  # from spinbox
        elif PARAM.BOOL == self.param.paramType:
            val = self.q2.isChecked()  # checkbox
        elif PARAM.FLOAT == self.param.paramType:
            val = float(self.q2.text())
        elif PARAM.COMPLEX == self.param.paramType:
            val = complex(self.q2.text())
        else:
            val = str(self.q2.text())
            LOG.warn('unknow PARAM type:%s' % self.param.paramType)

        # self.param.name
        self.param.visibleValue = self.q4.isChecked()
        self.param.visibleName = self.q5.isChecked()
        self.param.color = self.q6.palette().color(QPalette.Button)

        if self.param.name == 'Ref':
            pass  # do not write value of reference
        else:
            self.param.value = val  # write value

    def __str__(self):
        return str(self.param)


class CompProperties(QDialog):
    '''Dialog window to edit component properties.'''
    def __init__(self, comp, position, parent=None):
        '''Component properties dialog

        :param comp: instance of component.Component
        :param position:
        :param parent:
        '''
        super(CompProperties, self).__init__(parent)
        self.comp = comp  # referencia na editovany komponent
        self.move(position)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowTitle('%s Properties' % comp.parameter['Ref'].value)
        self.ui.buttonBox.clicked.connect(self.bbclicked)

        clsname, clsdoc, clspath = get_classinfo(comp)
        self.ui.label_blockname.setText(clsname)
        tip = '%s\n\n%s' % (clspath, clsdoc)
        self.ui.label_blockname.setToolTip(tip)

        html = self.ui.label_code.text()
        html = html.replace('__PATH__', clspath)
        self.ui.label_code.setText(html)

        self._paramlst = []
        for param in comp.paramList:
            pobj = ParamLine(self, param)
            self._paramlst.append(pobj)

        # set header
        lst = [QLabel(''), QLabel(''), QLabel(''),
               QLabel('V'), QLabel('N'), QLabel('C')]
        lst[3].setToolTip('set visible Value')
        lst[4].setToolTip('set visible Name\n(works only when visible value)')
        lst[5].setToolTip('set color')
        self.ui.gridLayout_param.addWidget(lst[0], 0, 0)
        self.ui.gridLayout_param.addWidget(lst[1], 0, 1)
        self.ui.gridLayout_param.addWidget(lst[2], 0, 2)
        self.ui.gridLayout_param.addWidget(lst[3], 0, 3)
        self.ui.gridLayout_param.addWidget(lst[4], 0, 4)
        self.ui.gridLayout_param.addWidget(lst[5], 0, 5)

        for i, pobj in enumerate(self._paramlst):
            row = i + 1  # first row is header
            self.ui.gridLayout_param.addWidget(pobj.q1, row, 0)
            self.ui.gridLayout_param.addWidget(pobj.q2, row, 1)
            self.ui.gridLayout_param.addWidget(pobj.q3, row, 2)
            self.ui.gridLayout_param.addWidget(pobj.q4, row, 3)
            self.ui.gridLayout_param.addWidget(pobj.q5, row, 4)
            self.ui.gridLayout_param.addWidget(pobj.q6, row, 5)

    def bbclicked(self, button):
        '''If clicked to OK or Apply, set parameters'''
        role = self.ui.buttonBox.buttonRole(button)
        if role in [self.ui.buttonBox.AcceptRole,
                    self.ui.buttonBox.ApplyRole]:

            for pobj in self._paramlst:
                try:
                    pobj.write_parameter()
                except Exception as e:
                    QMessageBox.warning(self.parent(),
                                        'Error', '%s\n\n\n%s' % (pobj, e),
                                        buttons=QMessageBox.Ignore)
        self.comp.updateShape()


def get_classinfo(component):
    '''return (classname, docsting, path)

    :param component: component
    '''
    clsname = component.__class__.__name__
    clsdoc = ''  # docstring from class
    for line in str(component.__class__.__doc__).split('\n'):
        line = line.strip()
        if not line:
            continue  # remove empty lines
        if line.startswith('!'):
            continue
        if line.startswith('@'):
            continue
        clsdoc += line + '\n'
    # clspath = component.__module__
    clspath = inspect.getfile(component.__class__)

    return clsname, clsdoc, clspath
