'''
Created on Sep 6, 2014

@author: Mukundan
'''
'''
Usage:

from kmxGeneral import kmxINIConfigReadWrite
from kmxGeneral import kmxTools
from kmxPyQt import kmxQtCommonTools


        self.cfg = kmxINIConfigReadWrite.INIConfig("config.ini")
        self.iconPath = self.cfg.getOption('UserInterface', 'IconPath')
        self.icons = core.icons.iconSetup()
        self.infoStyle = kmxTools.infoStyle()
        self.infoStyle.errorLevel = 2
        self.infoStyle.infoLevel = 0

        self.tls = kmxTools.Tools(self.infoStyle)
        self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)

'''

import os

from PyQt5 import QtCore, QtGui, QtWidgets

from kmxGeneral import kmxINIConfigReadWrite
from kmxGeneral import kmxTools


class CommonTools(object):
    '''
    classdocs
    '''
    def __init__(self, parentWindow, iconPath=None):
        '''
        Constructor
        '''
        self.CallingUI = parentWindow
        self.IconPath = iconPath
        self.defaultIcon = "NoIcon.png"
        self.infoStyle = kmxTools.infoStyle()
        self.ttls = kmxTools.Tools(self.infoStyle)
        if self.IconPath is None:
            self.cfg = kmxINIConfigReadWrite.INIConfig("config.ini", writeOk=False)
            if(self.cfg.iniReady):
                self.iconPath = self.cfg.getOption('UserInterface', 'IconPath')
            else:
                self.IconPath = "../icons/"

    def setIconByObj(self, itm2Icon):
        # print (itm2Icon.__name__)
        pass


    def getIconString(self, iconName='NoIcon.png', alternateIcon='NoIcon.png'):
        """
        Returns the path of ICONNAME found on 'iconPath'. Else
        """
        try:
            if os.path.exists(self.IconPath + '/' + iconName) and os.path.isfile(self.IconPath + '/' + iconName):
                return self.IconPath + '/' + iconName
            elif os.path.exists(self.IconPath + '/' + alternateIcon) and os.path.isfile(self.IconPath + '/' + alternateIcon):
                return self.IconPath + '/' + alternateIcon
            elif os.path.exists(self.IconPath + '/' + self.DefaultIcon) and os.path.isfile(self.IconPath + '/' + self.DefaultIcon):
                return self.IconPath + '/' + self.DefaultIcon
            else:
                print ("Error! No Icon found for: " + iconName)
                return None
        except:
            print ("Error! No Icon found for: " + iconName)
            return None

    def getIcon(self, iconName, alternate='', random=False):
            icon = QtGui.QIcon()
            pxmap = None

            if(random):
                iconName = "/04/16/" + str(self.ttls.getRandom(50, 10)) + ".png"

            if alternate:
                iconString = self.getIconString(iconName, alternate)
                if iconString:
                    icon.addPixmap(QtGui.QPixmap(iconString), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    pxmap = QtGui.QPixmap(iconString)
            else:
                iconString = self.getIconString(iconName)
                if iconString:
                    icon.addPixmap(QtGui.QPixmap(iconString), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    pxmap = QtGui.QPixmap(iconString)

            return icon

    def setIconForItem(self, item, iconName, isWindow=0, Col=0, comboBoxIndex=0, OptionalIcon='', thisImage='', clear=0, random=False):
        itemType = type(item)
        # print itemType
        icon = QtGui.QIcon()
        pxmap = None

        if thisImage:
                if os.path.exists(thisImage):
                    icon.addPixmap(QtGui.QPixmap(thisImage), QtGui.QIcon.Normal, QtGui.QIcon.On)
                    pxmap = QtGui.QPixmap(thisImage)
        else:
            icon = self.getIcon(iconName, OptionalIcon, random)

        if clear:
                icon = QtGui.QIcon()
                pxmap = QtGui.QPixmap()

        if isWindow:
            item.setWindowIcon(icon)

        if itemType == type(QtWidgets.QPushButton()):
            item.setIcon(icon)

        if itemType == type(QtWidgets.QToolButton()):
            item.setIcon(icon)

        if itemType == type(QtWidgets.QWidget()):
            tabWidget = item.parentWidget().parentWidget()
            if type(tabWidget) == type(QtWidgets.QTabWidget()):
                index = tabWidget.indexOf(item)
                tabWidget.setTabIcon(index, icon)

        if itemType == type(QtWidgets.QTreeWidgetItem()):
            item.setIcon(Col, icon)

        if itemType == type(QtWidgets.QTableWidgetItem()):
            item.setIcon(icon)

        if itemType == type(QtWidgets.QListWidgetItem()):
            item.setIcon(icon)

        if itemType == type(QtWidgets.QAction(None)):
            item.setIcon(icon)

        if itemType == type(QtWidgets.QLabel()):
            if (pxmap is not None):
                item.setPixmap(pxmap)

        if itemType == type(QtWidgets.QComboBox()):
            item.setItemIcon (comboBoxIndex, icon)


    def getValue(self, control):
        val = ""
        if (type(control) == QtWidgets.QLineEdit):
            val = control.text()
        elif (type(control) == QtWidgets.QLabel):
            val = control.text()
        return str(val)

    def setValue(self, control, value):
        if (type(control) == QtWidgets.QLineEdit):
            control.setText(str(value))
        elif (type(control) == QtWidgets.QLabel):
            control.setText(str(value))

    def applyStyle(self, style='Fusion'):
        # ['Windows', 'WindowsXP', 'WindowsVista', 'Fusion']
        # Use this ... getStyleList()
        QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create(style))
        QtWidgets.QApplication.setPalette(QtWidgets.QApplication.style().standardPalette())

    def getStyleList(self):
        return QtWidgets.QStyleFactory.keys()

    def showInputBox(self, Title='Information', Message='Information', DefaultValue=''):
        comments, ok = QtWidgets.QInputDialog.getText(self.CallingUI, str(Title), str(Message), QtWidgets.QLineEdit.Normal, DefaultValue)
        if ok:
            return comments
        else:
            return ''

    def getFile(self, Title='Select a file to open...', FileName='Select File', FileType='All Files (*);;Excel Files (*.xls);;Text Files (*.txt)'):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self.CallingUI, str(Title), FileName, str(FileType))
        if(fileName[0] == ""): return ""
        return fileName[0]

    def getFolder(self, Title='Select a directory...'):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self.CallingUI, str(Title))
        if(folder == ""): return ""
        return folder

    def showYesNoBox(self, Title='Information', Message='Information'):
        ret = QtWidgets.QMessageBox.question(self.CallingUI, Title, Message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        return ret == QtWidgets.QMessageBox.Yes

    def showInfoBox(self, Title='Information', Message='Information'):
        QtWidgets.QMessageBox.information(self.CallingUI, Title, Message)
