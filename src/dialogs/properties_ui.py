# -*- coding: utf-8 -*-
#@PydevCodeAnalysisIgnore
#pylint: disable-all
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './properties.ui'
#
# Created by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!


import six
if six.PY2:
    from PyQt4.QtGui import *  # @UnusedWildImport
    from PyQt4.QtCore import *  # @UnusedWildImport
else:
    # from PyQt5.QtSvg import *
    from PyQt5.QtWidgets import *  # @UnusedWildImport
    from PyQt5.QtGui import *  # @UnusedWildImport
    from PyQt5.QtCore import *  # @UnusedWildImport


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(460, 90)
        Dialog.setSizeGripEnabled(True)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_param = QGridLayout()
        self.gridLayout_param.setObjectName("gridLayout_param")
        self.gridLayout.addLayout(self.gridLayout_param, 1, 0, 3, 3)
        self.label_blockname = QLabel(Dialog)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_blockname.setFont(font)
        self.label_blockname.setObjectName("label_blockname")
        self.gridLayout.addWidget(self.label_blockname, 0, 0, 1, 3)
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 2, 1, 1)
        self.label_code = QLabel(Dialog)
        self.label_code.setEnabled(True)
        font = QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_code.setFont(font)
        self.label_code.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_code.setOpenExternalLinks(True)
        self.label_code.setObjectName("label_code")
        self.gridLayout.addWidget(self.label_code, 5, 0, 1, 1)
        spacerItem = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 2, 1, 1)
        self.gridLayout.setRowStretch(3, 1)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_blockname.setText(_translate("Dialog", "block name"))
        self.label_code.setToolTip(_translate("Dialog", "Open file with default application"))
        self.label_code.setText(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><a href=\"__PATH__\"><span style=\" text-decoration: underline; color:#0000ff;\">code</span></a></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

