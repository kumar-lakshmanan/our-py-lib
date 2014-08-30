# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\REPO\PulseServer\Library\Common\AppReleaseLog\release_log_ui.ui'
#
# Created: Mon Jan 24 15:19:44 2011
#      by: PyQt4 UI code generator 4.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(413, 540)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lblAppName = QtGui.QLabel(self.widget)
        self.lblAppName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lblAppName.setObjectName(_fromUtf8("lblAppName"))
        self.gridLayout.addWidget(self.lblAppName, 0, 1, 1, 1)
        self.line = QtGui.QFrame(self.widget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 0, 1, 2)
        self.gridLayout_2.addWidget(self.widget, 0, 0, 1, 2)
        self.widget_2 = QtGui.QWidget(self.centralwidget)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.widget_2)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.txtLog = QtGui.QTextEdit(self.widget_2)
        self.txtLog.setReadOnly(True)
        self.txtLog.setObjectName(_fromUtf8("txtLog"))
        self.gridLayout_3.addWidget(self.txtLog, 3, 0, 1, 1)
        self.txtCurrent = QtGui.QTextEdit(self.widget_2)
        self.txtCurrent.setMaximumSize(QtCore.QSize(16777215, 150))
        self.txtCurrent.setReadOnly(True)
        self.txtCurrent.setObjectName(_fromUtf8("txtCurrent"))
        self.gridLayout_3.addWidget(self.txtCurrent, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.widget_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.widget_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_3.addWidget(self.label_4, 2, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget_2, 1, 0, 1, 2)
        self.widget_3 = QtGui.QWidget(self.centralwidget)
        self.widget_3.setObjectName(_fromUtf8("widget_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.widget_3)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.btnRelease = QtGui.QToolButton(self.widget_3)
        self.btnRelease.setMinimumSize(QtCore.QSize(70, 0))
        self.btnRelease.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnRelease.setObjectName(_fromUtf8("btnRelease"))
        self.gridLayout_4.addWidget(self.btnRelease, 0, 1, 1, 1)
        self.btnClose = QtGui.QToolButton(self.widget_3)
        self.btnClose.setMinimumSize(QtCore.QSize(70, 0))
        self.btnClose.setMaximumSize(QtCore.QSize(150, 16777215))
        self.btnClose.setObjectName(_fromUtf8("btnClose"))
        self.gridLayout_4.addWidget(self.btnClose, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget_3, 2, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Application Release Log", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Application: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblAppName.setText(QtGui.QApplication.translate("MainWindow", "AppName", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Current Version:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Change History:", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRelease.setText(QtGui.QApplication.translate("MainWindow", "New Release", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))

