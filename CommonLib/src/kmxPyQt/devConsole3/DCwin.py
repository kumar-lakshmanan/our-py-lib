# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J:\our-py-lib\CommonLib\src\kmxPyQt\devConsole3\/DCwin.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_devConsole(object):
    def setupUi(self, devConsole):
        devConsole.setObjectName("devConsole")
        devConsole.resize(846, 513)
        self.gridLayout_3 = QtWidgets.QGridLayout(devConsole)
        self.gridLayout_3.setSpacing(2)
        self.gridLayout_3.setContentsMargins(3, 3, 3, 3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter = QtWidgets.QSplitter(devConsole)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setOpaqueResize(False)
        self.splitter.setObjectName("splitter")
        self.widget_2 = QtWidgets.QWidget(self.splitter)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget_2)
        self.gridLayout_2.setSpacing(2)
        self.gridLayout_2.setContentsMargins(2, 2, 2, 2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.splitter_2 = QtWidgets.QSplitter(self.widget_2)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setOpaqueResize(False)
        self.splitter_2.setObjectName("splitter_2")
        self.sciOutput = Qsci.QsciScintilla(self.splitter_2)
        self.sciOutput.setToolTip("")
        self.sciOutput.setWhatsThis("")
        self.sciOutput.setFrameShape(QtWidgets.QFrame.Box)
        self.sciOutput.setObjectName("sciOutput")
        self.treeWidget = QtWidgets.QTreeWidget(self.splitter_2)
        self.treeWidget.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.treeWidget.setFont(font)
        self.treeWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setRootIsDecorated(True)
        self.treeWidget.setUniformRowHeights(True)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "Plugs")
        self.treeWidget.header().setVisible(True)
        self.gridLayout_2.addWidget(self.splitter_2, 0, 0, 1, 2)
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.widget)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(self.frame)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setObjectName("tabWidget")
        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 3)
        self.cline = QtWidgets.QLineEdit(self.splitter)
        self.cline.setMaximumSize(QtCore.QSize(16777215, 25))
        self.cline.setObjectName("cline")
        self.gridLayout_3.addWidget(self.splitter, 1, 0, 1, 11)
        self.btnLoadScript = QtWidgets.QToolButton(devConsole)
        self.btnLoadScript.setMinimumSize(QtCore.QSize(75, 0))
        self.btnLoadScript.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btnLoadScript.setAutoRaise(True)
        self.btnLoadScript.setObjectName("btnLoadScript")
        self.gridLayout_3.addWidget(self.btnLoadScript, 0, 2, 1, 1)
        self.btnSaveScript = QtWidgets.QToolButton(devConsole)
        self.btnSaveScript.setMinimumSize(QtCore.QSize(75, 0))
        self.btnSaveScript.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btnSaveScript.setAutoRaise(True)
        self.btnSaveScript.setObjectName("btnSaveScript")
        self.gridLayout_3.addWidget(self.btnSaveScript, 0, 4, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(33, 17, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 10, 1, 1)
        self.label = QtWidgets.QLabel(devConsole)
        self.label.setText("")
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 0, 7, 1, 1)
        self.btnNewScript = QtWidgets.QToolButton(devConsole)
        self.btnNewScript.setMinimumSize(QtCore.QSize(75, 0))
        self.btnNewScript.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btnNewScript.setAutoRaise(True)
        self.btnNewScript.setObjectName("btnNewScript")
        self.gridLayout_3.addWidget(self.btnNewScript, 0, 1, 1, 1)
        self.btnQuickSaveScript = QtWidgets.QToolButton(devConsole)
        self.btnQuickSaveScript.setMinimumSize(QtCore.QSize(75, 0))
        self.btnQuickSaveScript.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btnQuickSaveScript.setAutoRaise(True)
        self.btnQuickSaveScript.setObjectName("btnQuickSaveScript")
        self.gridLayout_3.addWidget(self.btnQuickSaveScript, 0, 3, 1, 1)
        self.btnExecute = QtWidgets.QToolButton(devConsole)
        self.btnExecute.setMinimumSize(QtCore.QSize(75, 0))
        self.btnExecute.setMaximumSize(QtCore.QSize(75, 16777215))
        self.btnExecute.setAutoRaise(True)
        self.btnExecute.setObjectName("btnExecute")
        self.gridLayout_3.addWidget(self.btnExecute, 0, 9, 1, 1)
        self.line = QtWidgets.QFrame(devConsole)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_3.addWidget(self.line, 0, 8, 1, 1)

        self.retranslateUi(devConsole)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(devConsole)

    def retranslateUi(self, devConsole):
        _translate = QtCore.QCoreApplication.translate
        devConsole.setWindowTitle(_translate("devConsole", "DevConsole"))
        self.treeWidget.setSortingEnabled(True)
        self.btnLoadScript.setText(_translate("devConsole", "Load Script"))
        self.btnSaveScript.setText(_translate("devConsole", "Save Script As"))
        self.btnNewScript.setText(_translate("devConsole", "New Script"))
        self.btnQuickSaveScript.setText(_translate("devConsole", "Save Script"))
        self.btnExecute.setText(_translate("devConsole", "Execute"))

from PyQt5 import Qsci
