# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Pankaj\ABXpulse\REPO\SOURCE\SCRIPTS\PYTHON\LightNPray\lib\MayaAddon\renderConfirm.ui'
#
# Created: Mon Nov 01 19:26:22 2010
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(486, 161)
        Dialog.setMinimumSize(QtCore.QSize(486, 161))
        Dialog.setMaximumSize(QtCore.QSize(486, 161))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(Dialog)
        self.label.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.commentTE = QtGui.QTextEdit(Dialog)
        self.commentTE.setObjectName("commentTE")
        self.gridLayout.addWidget(self.commentTE, 0, 1, 1, 3)
        spacerItem = QtGui.QSpacerItem(238, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.revisionPB = QtGui.QPushButton(Dialog)
        self.revisionPB.setObjectName("revisionPB")
        self.gridLayout.addWidget(self.revisionPB, 1, 2, 1, 1)
        self.versionPB = QtGui.QPushButton(Dialog)
        self.versionPB.setObjectName("versionPB")
        self.gridLayout.addWidget(self.versionPB, 1, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Confirm Render", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Comment", None, QtGui.QApplication.UnicodeUTF8))
        self.revisionPB.setText(QtGui.QApplication.translate("Dialog", "Render", None, QtGui.QApplication.UnicodeUTF8))
        self.versionPB.setText(QtGui.QApplication.translate("Dialog", "Rerender", None, QtGui.QApplication.UnicodeUTF8))

