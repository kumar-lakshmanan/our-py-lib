'''
Created on Oct 24, 2015

@author: MUKUND
'''
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt, )
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, )
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
#from PyQt5.uic.Compiler.qtproxies import QtWidgets

class dynamicObjs(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.dckItems = []
        self.actItems = []
        
    def addNewDock(self, dockUIObj, name, description='', icon=None):        
        dckItem = QtWidgets.QDockWidget(self)
        dockUIObj.setupUi(dckItem)
        dckItem.setObjectName(name)
        self.addDockWidget(QtCore.Qt.DockWidgetArea(1), dckItem)
         
        actItem = self.addNewAction(name, description, None, 1, 1)        
        actItem.toggled.connect(dckItem.setVisible)     
        dckItem.visibilityChanged.connect(actItem.setChecked)   
        self.toolsMenu.addAction(actItem)
        
        self.dckItems.append(dckItem)
        self.actItems.append(actItem)        

    def addNewAction(self, name, description=None, icon=None, checkable=False, checked=False):
        if(icon):
            itm = QAction(self.qtIcon.getIcon(icon), name, self, statusTip=description, triggered=self.doActionClicked)
        else:
            itm = QAction(name, self, statusTip=description, triggered=self.doActionClicked) 

        itm.setCheckable(checkable)
        itm.setChecked(checked)
        return itm

    def doActionClicked(self, *arg):
        currentActObj = self.sender()
        currentActName = currentActObj.iconText()
        if currentActName=='Execute':
            self.executeCurrentScript()
