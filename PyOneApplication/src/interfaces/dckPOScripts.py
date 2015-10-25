# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J:\our-py-lib\PyOneApplication\src\interfaces\/dckPOScripts.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(400, 300)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setObjectName("gridLayout")
        self.treeWidget = QtWidgets.QTreeWidget(self.dockWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.treeWidget.setFont(font)
        self.treeWidget.setFrameShape(QtWidgets.QFrame.Box)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setRootIsDecorated(True)
        self.treeWidget.setUniformRowHeights(True)
        self.treeWidget.setAnimated(True)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.header().setVisible(False)
        self.gridLayout.addWidget(self.treeWidget, 0, 0, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "PyOneScripts"))
        self.treeWidget.setSortingEnabled(True)

