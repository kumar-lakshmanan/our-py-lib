# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\REPO\PulseServer\Library\Common\AppReleaseLog\new_release_ui.ui'
#
# Created: Fri Jan 21 22:08:01 2011
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(488, 234)
        Dialog.setModal(True)
        self.gridLayout_3 = QtGui.QGridLayout(Dialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.rbMajor = QtGui.QRadioButton(self.groupBox)
        self.rbMajor.setObjectName("rbMajor")
        self.gridLayout.addWidget(self.rbMajor, 0, 0, 1, 1)
        self.rbMinor = QtGui.QRadioButton(self.groupBox)
        self.rbMinor.setObjectName("rbMinor")
        self.gridLayout.addWidget(self.rbMinor, 1, 0, 1, 1)
        self.rbPatch = QtGui.QRadioButton(self.groupBox)
        self.rbPatch.setChecked(True)
        self.rbPatch.setObjectName("rbPatch")
        self.gridLayout.addWidget(self.rbPatch, 2, 0, 1, 1)
        self.rbDev = QtGui.QRadioButton(self.groupBox)
        self.rbDev.setObjectName("rbDev")
        self.gridLayout.addWidget(self.rbDev, 3, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.txtChange = QtGui.QTextEdit(self.groupBox_2)
        self.txtChange.setObjectName("txtChange")
        self.gridLayout_2.addWidget(self.txtChange, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_2, 0, 1, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(220, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem1, 1, 1, 1, 1)
        self.btnRelease = QtGui.QToolButton(Dialog)
        self.btnRelease.setMinimumSize(QtCore.QSize(60, 0))
        self.btnRelease.setObjectName("btnRelease")
        self.gridLayout_3.addWidget(self.btnRelease, 1, 2, 1, 1)
        self.btnClose = QtGui.QToolButton(Dialog)
        self.btnClose.setMinimumSize(QtCore.QSize(60, 0))
        self.btnClose.setObjectName("btnClose")
        self.gridLayout_3.addWidget(self.btnClose, 1, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "New Release", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Release Type", None, QtGui.QApplication.UnicodeUTF8))
        self.rbMajor.setText(QtGui.QApplication.translate("Dialog", "Major Version", None, QtGui.QApplication.UnicodeUTF8))
        self.rbMinor.setText(QtGui.QApplication.translate("Dialog", "Minor Version", None, QtGui.QApplication.UnicodeUTF8))
        self.rbPatch.setText(QtGui.QApplication.translate("Dialog", "Patch Version", None, QtGui.QApplication.UnicodeUTF8))
        self.rbDev.setText(QtGui.QApplication.translate("Dialog", "Development", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Changes since last release", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRelease.setText(QtGui.QApplication.translate("Dialog", "Release", None, QtGui.QApplication.UnicodeUTF8))
        self.btnClose.setText(QtGui.QApplication.translate("Dialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

