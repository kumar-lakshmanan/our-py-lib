'''
Created on Sep 6, 2014

@author: Mukundan
'''
from PyQt5 import QtCore, QtGui, QtWidgets

class Tools(object):
    '''
    classdocs
    '''
    def __init__(self, parentWindow):
        '''
        Constructor
        '''
        self.CallingUI = parentWindow

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

    def showInputBox(self, Title='Information', Message='Information', DefaultValue=''):
        comments, ok = QtWidgets.QInputDialog.getText(self.uiMain, str(Title), str(Message), QtWidgets.QLineEdit.Normal, DefaultValue)
        if ok and not comments.isEmpty():
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

class TreeWidget(object):

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def createItem(self, Text='', Data=''):
        itm = QtWidgets.QTreeWidgetItem()
        itm.setText(0, str(Text))
        itm.setData(0, QtCore.Qt.UserRole, QtCore.QVariant(str(Data)))
        return itm

    def addNewRoot(self, treeWidget, item):
        return treeWidget.addTopLevelItem(item)
