import six

if six.PY2:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import QRectF, QPointF, Qt, QPoint, QThread
    from PyQt4.QtSvg import QSvgWidget
else:
    from PyQt5.QtSvg import QSvgWidget
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
# from lib.pseqt import *  # @UnusedWildImport
