# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F:\Kumaresan\Code\Python\devPlugGenerator\src\user_interface\win_main.ui'
#
# Created: Thu Oct 16 11:21:31 2014
#      by: PyQt5 UI code generator 5.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(491, 313)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 5, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 3, 0, 1, 2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.gridLayout.addWidget(self.line_3, 6, 0, 1, 2)
        self.widget_5 = QtWidgets.QWidget(self.centralwidget)
        self.widget_5.setObjectName("widget_5")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.widget_5)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget_5)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.gridLayout_7.addWidget(self.lineEdit_5, 1, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.widget_5)
        self.label_5.setObjectName("label_5")
        self.gridLayout_7.addWidget(self.label_5, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.widget_5, 0, 0, 1, 2)
        self.widget_6 = QtWidgets.QWidget(self.centralwidget)
        self.widget_6.setObjectName("widget_6")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.widget_6)
        self.gridLayout_8.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.widget_6)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_8.addWidget(self.lineEdit_6, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.widget_6)
        self.label_6.setObjectName("label_6")
        self.gridLayout_8.addWidget(self.label_6, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.widget_6, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 491, 18))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dev Plug Generator"))
        self.pushButton.setText(_translate("MainWindow", "Generate Dev Plug"))
        self.lineEdit_5.setText(_translate("MainWindow", "plugTemplate"))
        self.label_5.setText(_translate("MainWindow", "PlugName:"))
        self.lineEdit_6.setText(_translate("MainWindow", "F:\\Kumaresan\\Code\\Python\\devPlugGenerator\\src\\core\\devPlugGenerator_bin\\devPlugs"))
        self.label_6.setText(_translate("MainWindow", "Destination:"))

