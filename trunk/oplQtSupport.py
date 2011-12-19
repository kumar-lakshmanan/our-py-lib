#-------------------------------------------------------------------------------
# Name:        oplQtSupports
# Purpose:
#
# Author:      AIAA
#
# Created:     10-11-2011
# Copyright:   (c) AIAA 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
import sip
import os
import pickle

class oplQtSupport():

    """
        Following functions are ment for various purpose in QtBased UI Development.
    """
    def __init__(self, uiMain, iconBasePath="", defaultIcon="", defaultIcon2="", defaultIcon3=""):
        self.uiMain=uiMain
        self.iconBasePath=iconBasePath
        self.defaultIcon=defaultIcon;
        self.defaultIcon2=defaultIcon2;
        self.defaultIcon3=defaultIcon3 if defaultIcon3 else "default.png";

    def getText(self, widget):
        data = None
        if type(widget) is type(QtGui.QLineEdit()):
            data = str(widget.text())
        return data

    def setText(self, widget, value):
        if type(widget) is type(QtGui.QLineEdit()):
            widget.setText(str(value))

    def setData(self, widget, data=""):
        widget.setProperty("tag", data)

    def getData(self, widget):
        if hasattr(widget,"property"):
            return widget.property("tag")
        else:
            return None

    def showBusy(self):
        busyCursor = QtGui.QCursor(QtCore.Qt.WaitCursor)
        QtGui.qApp.setOverrideCursor(busyCursor)

    def showRelax(self):
        QtGui.qApp.restoreOverrideCursor()

    def getIconFile(self, icon=""):
        iconFile = icon if icon else self.__defaultIcon()
        iconFile = iconFile.lstrip("\\")
        iconFile = iconFile.lstrip("/")
        iconFile = os.path.join(self.iconBasePath, iconFile)
        if os.path.exists(iconFile) and os.path.isfile(iconFile):
            return iconFile
        else:
            return ""

    def setIcon(self, item, iconName="", overriddenIconFile=""):
        itemType = type(item)
        icon = QtGui.QIcon()
        pxmap = QtGui.QPixmap()
        iconFile = self.getIconFile(iconName)

        if iconFile:
            pxmap = QtGui.QPixmap(iconFile)
            icon.addPixmap(pxmap, QtGui.QIcon.Normal, QtGui.QIcon.On)
        elif overriddenIconFile:
            if os.path.exists(overriddenIconFile):
                pxmap = QtGui.QPixmap(overriddenIconFile)
                icon.addPixmap(pxmap, QtGui.QIcon.Normal, QtGui.QIcon.On)
        else:
            pxmap = QtGui.QPixmap()
            icon = QtGui.QIcon()

        if hasattr(item,"isWindow") and item.isWindow():
            item.setWindowIcon(icon)
        elif itemType == type(QtGui.QPushButton()):
            item.setIcon(icon)
        elif itemType == type(QtGui.QToolButton()):
            item.setIcon(icon)
        elif itemType == type(QtGui.QTreeWidgetItem()):
            item.setIcon(Col,icon)
        elif itemType == type(QtGui.QTableWidgetItem()):
            item.setIcon(icon)
        elif itemType == type(QtGui.QListWidgetItem()):
            item.setIcon(icon)
        elif itemType == type(QtGui.QAction(None)):
            item.setIcon(icon)
        elif itemType == type(QtGui.QLabel()):
            item.setPixmap(pxmap)
        elif itemType == type(QtGui.QComboBox()):
            item.setItemIcon (comboBoxIndex, icon)
        elif itemType == type(QtGui.QWidget()):
            tabWidget = item.parentWidget().parentWidget()
            if type(tabWidget)==type(QtGui.QTabWidget()):
                index = tabWidget.indexOf(item)
                tabWidget.setTabIcon(index,icon)

    def uiLayoutSave(self, layoutFile='layout.lyt'):
        dirname = os.path.dirname(layoutFile)
        if dirname!='' and not os.path.exists(dirname):
            os.makedirs(dirname)

        winsiz = self.uiMain.size()
        winpos = self.uiMain.pos()
        lst = [self.uiMain.saveState(),winsiz,winpos]
        f=open(layoutFile, 'w')
        pickle.dump(lst,f)
        f.close()

    def uiLayoutRestore(self,layoutFile='layout.lyt'):
        if os.path.exists(layoutFile):
            f=open(layoutFile, 'r')
            lst = pickle.load(f)
            f.close()
            self.uiMain.restoreState(lst[0])
            self.uiMain.resize(lst[1])
            self.uiMain.move(lst[2])

    def showInputBox(self, Title='Information', Message='Information', DefaultValue=''):
        comments, ok = QtGui.QInputDialog.getText(self.uiMain, str(Title), str(Message), QtGui.QLineEdit.Normal, DefaultValue)
        if ok and not comments.isEmpty():
            return comments
        else:
            return ''

    def __defaultIcon(self):
        if self.defaultIcon:
            icon=self.defaultIcon
        elif self.defaultIcon2:
            icon=self.defaultIcon2
        elif self.defaultIcon3:
            icon=self.defaultIcon3
        else:
            icon=""
        return icon