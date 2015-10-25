# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'J:\our-py-lib\PyOneApplication\src\interfaces\/dckOutputs.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(520, 223)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = Qsci.QsciScintilla(self.dockWidgetContents)
        self.textEdit.setToolTip("")
        self.textEdit.setWhatsThis("")
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 2)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "Output"))

from PyQt5 import Qsci
