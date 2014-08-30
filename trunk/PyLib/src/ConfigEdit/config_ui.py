# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\REPO\SOURCE\SCRIPTS\PYTHON\Shipping\ui\winConfig\config_ui.ui'
#
# Created: Thu Oct 14 16:11:24 2010
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_config(object):
    def setupUi(self, config):
        config.setObjectName("config")
        config.resize(610, 390)
        self.gridLayout = QtGui.QGridLayout(config)
        self.gridLayout.setObjectName("gridLayout")
        self.btnCancel = QtGui.QToolButton(config)
        self.btnCancel.setMinimumSize(QtCore.QSize(80, 0))
        self.btnCancel.setMaximumSize(QtCore.QSize(80, 16777215))
        self.btnCancel.setAutoRaise(True)
        self.btnCancel.setObjectName("btnCancel")
        self.gridLayout.addWidget(self.btnCancel, 3, 4, 1, 1)
        self.btnApply = QtGui.QToolButton(config)
        self.btnApply.setMinimumSize(QtCore.QSize(80, 0))
        self.btnApply.setMaximumSize(QtCore.QSize(80, 16777215))
        self.btnApply.setAutoRaise(True)
        self.btnApply.setObjectName("btnApply")
        self.gridLayout.addWidget(self.btnApply, 3, 3, 1, 1)
        self.tblSettings = QtGui.QTableWidget(config)
        self.tblSettings.setObjectName("tblSettings")
        self.tblSettings.setColumnCount(2)
        self.tblSettings.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tblSettings.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tblSettings.setHorizontalHeaderItem(1, item)
        self.gridLayout.addWidget(self.tblSettings, 1, 1, 2, 4)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 3, 2, 1, 1)
        self.trSections = QtGui.QTreeWidget(config)
        self.trSections.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.trSections.setFont(font)
        self.trSections.setAlternatingRowColors(True)
        self.trSections.setRootIsDecorated(False)
        self.trSections.setItemsExpandable(False)
        self.trSections.setObjectName("trSections")
        self.gridLayout.addWidget(self.trSections, 0, 0, 3, 1)
        self.lblSectionHead = QtGui.QLabel(config)
        self.lblSectionHead.setMinimumSize(QtCore.QSize(0, 15))
        self.lblSectionHead.setMaximumSize(QtCore.QSize(16777215, 15))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setItalic(False)
        font.setBold(True)
        self.lblSectionHead.setFont(font)
        self.lblSectionHead.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblSectionHead.setObjectName("lblSectionHead")
        self.gridLayout.addWidget(self.lblSectionHead, 0, 1, 1, 4)

        self.retranslateUi(config)
        QtCore.QMetaObject.connectSlotsByName(config)

    def retranslateUi(self, config):
        config.setWindowTitle(QtGui.QApplication.translate("config", "Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("config", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.btnApply.setText(QtGui.QApplication.translate("config", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.tblSettings.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("config", "Setting", None, QtGui.QApplication.UnicodeUTF8))
        self.tblSettings.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("config", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.trSections.setSortingEnabled(True)
        self.trSections.headerItem().setText(0, QtGui.QApplication.translate("config", "Section", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSectionHead.setText(QtGui.QApplication.translate("config", "Select a section", None, QtGui.QApplication.UnicodeUTF8))

