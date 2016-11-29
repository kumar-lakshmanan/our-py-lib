'''
Created on Oct 24, 2015

@author: MUKUND
'''
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt, )
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, QDockWidget)
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
import os
import sys

class trays(object):
    '''
    classdocs
    '''
    def __init__(self, params):
        '''
        Constructor
        '''
        print("Trays...!")

    def setupTray(self):
        self.tray = self.trayAgentReady()
        self.rightMenu = self.qtMenu.createMenu(None, 'DevConsoleMenu')
        self.tray.setContextMenu(self.rightMenu)
        self.updateTrayMenu('Quit',self.trayItemClicked)
        self.updateTrayMenu('|')
        self.updateTrayMenu('About',self.trayItemClicked)
        self.updateTrayMenu('Help',self.trayItemClicked)        

    def trayItemClicked(self, *arg):
        caller = self.sender()        
        itm = caller.text()
        if(itm=='Quit'):
            sys.exit(0)
        if(itm=='About'):
            print(self.aboutInfoPlainText)
        if(itm=='Help'):
            self.help()
        
    def trayAgentReady(self):    
        self.tray = QtWidgets.QSystemTrayIcon(self.qtIcon.getIcon('action_log.png'), self)
        self.tray.activated.connect(self.trayClicked)
        #self.connect(self.tray,SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),self.trayClicked)
        self.tray.show()
        return self.tray
    
    def trayClicked(self, click):   
        self.dcksState=[]                      
        if(click==3): 
            if (self.isVisible()):
                for each in self.findChildren(QDockWidget):
                    obj = each
                    objState = each.isVisible()
                    self.dcksState.append((obj,objState))
                self.hide()
            else:
                for each in self.dcksState:
                    obj = each[0]
                    objState = each[1]
                    obj.setVisible(objState)
                self.show()
                if self.windowState() == QtCore.Qt.WindowMinimized: 
                    self.setWindowState(QtCore.Qt.WindowActive)
                self.activateWindow()     
                self.raise_()
               
    def traymessage(self, messagetitle, message):
        self.tray.showMessage(messagetitle,message)
    
    def traykiller(self):
        self.tray.hide()
        del(self.tray)                    

    def updateTrayMenu(self, itemName, fnToCall=None):
        self.qtMenu.updateMenu(self,  self.rightMenu, itemName, fnToCall)        