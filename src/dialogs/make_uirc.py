# ! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.uic import compileUi
import sys
from _io import StringIO
prefix = r'C:\Python27\Lib\site-packages\PyQt4'

if sys.platform == "win32":
    cmd = prefix + r'\pyuic4.bat'
else:
    cmd = "pyuic5"

import os
QSCSIPATCH = '''
try:
    from PyQt5 import Qsci
except ImportError:
    from . import Qsci
'''

UNI_QT_IMPORT = '''
import six
if six.PY2:
    from PyQt4.QtGui import *  # @UnusedWildImport
    from PyQt4.QtCore import *  # @UnusedWildImport
else:
    # from PyQt5.QtSvg import *
    from PyQt5.QtWidgets import *  # @UnusedWildImport
    from PyQt5.QtGui import *  # @UnusedWildImport
    from PyQt5.QtCore import *  # @UnusedWildImport
'''


def get_uifiles(directory):
    uilst = []
    for item in os.listdir(directory):
        pth = os.path.join(directory, item)
        if os.path.isdir(pth):
            uilst.extend(get_uifiles(pth))
        if item.endswith('.ui'):
            uilst.append(pth)
    return uilst

uilst = get_uifiles('.')

for uifilename in uilst:
    pyfilename = uifilename.replace('.ui', '_ui.py')
    uifile = open(uifilename, 'r')
    pyfile = open(pyfilename, 'wb')
    pyfile.write('# -*- coding: utf-8 -*-\n'.encode(encoding='utf_8', errors='strict'))
    pyfile.write('#@PydevCodeAnalysisIgnore\n'.encode(encoding='utf_8', errors='strict'))
    pyfile.write('#pylint: disable-all\n'.encode(encoding='utf_8', errors='strict'))

    xfile = StringIO()
    compileUi(uifile, xfile, execute=True, indent=4, from_imports=True,
              resource_suffix='_rc')

    xfile.seek(0)
    for line in xfile.readlines():

        # --- patch to qt4 /qt5 compatibility
        line = line.replace('QtGui.', '')
        line = line.replace('QtCore.', '')
        line = line.replace('QtWidgets.', '')
        line = line.replace('from PyQt5 import QtCore, QtGui, QtWidgets',
                            UNI_QT_IMPORT)
        # ^^^ patch to qt4 /qt5 compatibility

        if line == 'from PyQt5 import Qsci\n':
            pyfile.write(QSCSIPATCH.encode(encoding='utf_8', errors='strict'))
        else:
            pyfile.write(line.encode(encoding='utf_8', errors='strict'))

    pyfile.close()
    print(pyfile)

# cmd = 'pyrcc4'
# print (subprocess.call([cmd, 'resource.qrc', '-o', 'resource_rc.py']))
