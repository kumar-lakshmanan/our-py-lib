# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\REPO\SOURCE\SCRIPTS\PYTHON\UI_DB_lib\konfig\kconfigWin.ui'
#
# Created: Fri Jun 18 14:11:45 2010
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_konfigWin(object):
    def setupUi(self, konfigWin):
        konfigWin.setObjectName("konfigWin")
        konfigWin.resize(455, 476)
        konfigWin.setModal(True)
        self.gridLayout = QtGui.QGridLayout(konfigWin)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtGui.QSplitter(konfigWin)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.trSettings = QtGui.QTreeWidget(self.splitter)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(9)
        self.trSettings.setFont(font)
        self.trSettings.setObjectName("trSettings")
        self.stkSettingPages = QtGui.QStackedWidget(self.splitter)
        self.stkSettingPages.setFrameShape(QtGui.QFrame.Panel)
        self.stkSettingPages.setFrameShadow(QtGui.QFrame.Sunken)
        self.stkSettingPages.setObjectName("stkSettingPages")
        self.page = QtGui.QWidget()
        self.page.setObjectName("page")
        self.stkSettingPages.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName("page_2")
        self.stkSettingPages.addWidget(self.page_2)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 4)
        self.line = QtGui.QFrame(konfigWin)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 4)
        self.toolButton = QtGui.QToolButton(konfigWin)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 2, 1, 1, 1)
        self.toolButton_2 = QtGui.QToolButton(konfigWin)
        self.toolButton_2.setObjectName("toolButton_2")
        self.gridLayout.addWidget(self.toolButton_2, 2, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)

        self.retranslateUi(konfigWin)
        QtCore.QMetaObject.connectSlotsByName(konfigWin)

    def retranslateUi(self, konfigWin):
        konfigWin.setWindowTitle(QtGui.QApplication.translate("konfigWin", "Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.trSettings.headerItem().setText(0, QtGui.QApplication.translate("konfigWin", "Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("konfigWin", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton_2.setText(QtGui.QApplication.translate("konfigWin", "Close", None, QtGui.QApplication.UnicodeUTF8))

