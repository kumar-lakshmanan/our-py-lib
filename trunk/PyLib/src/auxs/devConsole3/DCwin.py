# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\REPO\SOURCE\SCRIPTS\PYTHON\UI_DB_lib\devConsole3\DCwin.ui'
#
# Created: Mon Oct 04 15:07:33 2010
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_devConsole(object):
    def setupUi(self, devConsole):
        devConsole.setObjectName("devConsole")
        devConsole.resize(689, 504)
        self.gridLayout = QtGui.QGridLayout(devConsole)
        self.gridLayout.setObjectName("gridLayout")
        self.btnClearInput = QtGui.QToolButton(devConsole)
        self.btnClearInput.setMinimumSize(QtCore.QSize(75, 0))
        self.btnClearInput.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btnClearInput.setAutoRaise(True)
        self.btnClearInput.setObjectName("btnClearInput")
        self.gridLayout.addWidget(self.btnClearInput, 0, 0, 1, 1)
        self.btnClearOutput = QtGui.QToolButton(devConsole)
        self.btnClearOutput.setMinimumSize(QtCore.QSize(75, 0))
        self.btnClearOutput.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btnClearOutput.setAutoRaise(True)
        self.btnClearOutput.setObjectName("btnClearOutput")
        self.gridLayout.addWidget(self.btnClearOutput, 0, 1, 1, 1)
        self.btnLoadScript = QtGui.QToolButton(devConsole)
        self.btnLoadScript.setMinimumSize(QtCore.QSize(75, 0))
        self.btnLoadScript.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btnLoadScript.setAutoRaise(True)
        self.btnLoadScript.setObjectName("btnLoadScript")
        self.gridLayout.addWidget(self.btnLoadScript, 0, 2, 1, 1)
        self.btnSaveScript = QtGui.QToolButton(devConsole)
        self.btnSaveScript.setMinimumSize(QtCore.QSize(75, 0))
        self.btnSaveScript.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btnSaveScript.setAutoRaise(True)
        self.btnSaveScript.setObjectName("btnSaveScript")
        self.gridLayout.addWidget(self.btnSaveScript, 0, 3, 1, 1)
        self.btnExecute = QtGui.QToolButton(devConsole)
        self.btnExecute.setMinimumSize(QtCore.QSize(75, 0))
        self.btnExecute.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btnExecute.setAutoRaise(True)
        self.btnExecute.setObjectName("btnExecute")
        self.gridLayout.addWidget(self.btnExecute, 0, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(33, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 5, 1, 1)
        self.splitter = QtGui.QSplitter(devConsole)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.sciOutput = Qsci.QsciScintilla(self.splitter)
        self.sciOutput.setObjectName("sciOutput")
        self.sciInput = Qsci.QsciScintilla(self.splitter)
        self.sciInput.setObjectName("sciInput")
        self.cline = QtGui.QLineEdit(self.splitter)
        self.cline.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cline.setObjectName("cline")
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 6)

        self.retranslateUi(devConsole)
        QtCore.QMetaObject.connectSlotsByName(devConsole)

    def retranslateUi(self, devConsole):
        devConsole.setWindowTitle(QtGui.QApplication.translate("devConsole", "DevConsole", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClearInput.setText(QtGui.QApplication.translate("devConsole", "Clear Inputs", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClearOutput.setText(QtGui.QApplication.translate("devConsole", "Clear Outputs", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoadScript.setText(QtGui.QApplication.translate("devConsole", "Load Script", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSaveScript.setText(QtGui.QApplication.translate("devConsole", "Save Script", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExecute.setText(QtGui.QApplication.translate("devConsole", "Execute", None, QtGui.QApplication.UnicodeUTF8))
        self.btnExecute.setShortcut(QtGui.QApplication.translate("devConsole", "Ctrl+Enter", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import Qsci
