# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Kumaresan\Quest\MyMail\MyMailUI.ui'
#
# Created: Fri Jul 30 12:17:45 2010
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(734, 472)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.toolButton = QtGui.QToolButton(self.centralwidget)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(710, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.tableWidget = QtGui.QTableWidget(self.splitter)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.textBrowser = QtGui.QTextBrowser(self.splitter)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 734, 19))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Mail", None, QtGui.QApplication.UnicodeUTF8))
        self.toolButton.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))

