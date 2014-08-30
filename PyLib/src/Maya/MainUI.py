# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Kumaresanz\Quest\Test\MainUI.ui'
#
# Created: Fri Jan 07 16:50:32 2011
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(251, 410)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(1)
        self.gridLayout.setHorizontalSpacing(1)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtGui.QGridLayout(self.widget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtGui.QLabel(self.widget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.widget, 0, 1, 1, 2)
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 251, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.actionOption1 = QtGui.QAction(MainWindow)
        self.actionOption1.setObjectName("actionOption1")
        self.actionOption2 = QtGui.QAction(MainWindow)
        self.actionOption2.setObjectName("actionOption2")
        self.toolBar.addAction(self.actionOption1)
        self.toolBar.addAction(self.actionOption2)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "LOGO", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOption1.setText(QtGui.QApplication.translate("MainWindow", "Option1", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOption2.setText(QtGui.QApplication.translate("MainWindow", "Option2", None, QtGui.QApplication.UnicodeUTF8))

