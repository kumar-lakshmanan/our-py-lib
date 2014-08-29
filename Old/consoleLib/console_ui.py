# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Kumaresan\Dev\Python\opl\consoleLib\console_ui.ui'
#
# Created: Fri Jan 13 08:50:10 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnCopy = QtGui.QToolButton(Form)
        self.btnCopy.setAutoRaise(True)
        self.btnCopy.setObjectName(_fromUtf8("btnCopy"))
        self.gridLayout.addWidget(self.btnCopy, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(229, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.btnClose = QtGui.QToolButton(Form)
        self.btnClose.setAutoRaise(True)
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout.addWidget(self.btnClose, 1, 2, 1, 1)
        self.sci = Qsci.QsciScintilla(Form)
        self.sci.setToolTip(_fromUtf8(""))
        self.sci.setWhatsThis(_fromUtf8(""))
        self.sci.setFrameShape(QtGui.QFrame.Panel)
        self.sci.setObjectName(_fromUtf8("sci"))
        self.gridLayout.addWidget(self.sci, 0, 0, 1, 3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Console", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCopy.setText(QtGui.QApplication.translate("Form", "Copy to Clipboard", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("Form", "Close", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import Qsci
