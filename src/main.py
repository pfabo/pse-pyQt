#!/usr/bin/python3
# -*- coding: utf-8 -*-

# following sip lines shall be imported first
# it set python2 qt4 api to higher version, so it's compatible with qt5
# harmless for Qt5 (and can be removed if use only Qt5)
import sip  # @NoMove
sip.setapi('QString', 2)
sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QVariant', 2)

import logging
import os
import sys
import time

import six

from window import MainPseWindow
import lib  # @UnusedImport  |there we might get exception from import


if six.PY2:
    from PyQt4.QtGui import *  # @UnusedWildImport
else:
    # from PyQt5.QtSvg import *
    from PyQt5.QtWidgets import *  # @UnusedWildImport
    from PyQt5.QtGui import *  # @UnusedWildImport
    from PyQt5.QtCore import *  # @UnusedWildImport

logging.basicConfig(level=logging.NOTSET,  # NOTSET= log also debug messages
                    format='%(name)-12s: %(levelname)-8s %(message)s')

# import matplotlib
# sys.path.append(os.path.abspath("../lib"))

fileName = ''
if len(sys.argv) >= 2:
    fileName = sys.argv[1]

# Application start
# 1. vytvorenie temporary adresara pre docasne/pomocne subory
#    ak adresar existoval, jeho vymazanie (potencialny konflikt pri vytvarani)
#    novych docasnych suborov
data_path = './tmp'
if not os.path.exists(data_path):
    os.mkdir(data_path)
else:
    tmpFiles = os.listdir('./tmp')
    for f in tmpFiles:
        os.remove('./tmp/' + f)

app = QApplication(sys.argv)
app.setApplicationName("PSE")
app.setOrganizationName("")
app.setApplicationVersion('0.0.8')
app.setOrganizationDomain("pse.com")
app.setDesktopSettingsAware(True)

# PSE application window
mainApp = MainPseWindow(fileName)
mainApp.setGeometry(100, 100, 1024, 768)

# Show liblary window
mainApp.show_libwindow()

# Show PSE window (later than lib, in order to be on top)
mainApp.show()


# 4. thread aplikacie, pri ukonceni treba cakat, synchronizacia
#    medzi ukoncenim aplikacie a uvolnenim pamati
app.exec_()
app.deleteLater()
time.sleep(0.3)
sys.exit()
