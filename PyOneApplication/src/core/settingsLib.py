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
import os
import sys

class settings():
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.configs =  QSettings('config.ini',QSettings.IniFormat)
        self.aboutInfo = "The <b>PyOne</b> - Kumar's experimental project for rapid automation of frequent windows activities. Its kind of swiss knife for devlopers.<br> Got some ideas for it? Share with me <a href=\"mailto:kaymatrixgmail.com\">kaymatrix@gmail.com</a>, will join and implement them."

        
    def writeSettings(self):        
        #UI Settings
        self.configs.setValue('winPos', self.pos())
        self.configs.setValue('winSize', self.size())
        self.configs.setValue('winDockState', self.saveState())       
        self.configs.setValue('initalizeScripts', self.initalizeScripts)
        self.configs.setValue('scriptsDirName', self.scriptsDirName)
        self.configs.setValue('pluginsVerbose', self.pluginsVerbose)        
        self.configs.setValue('disableOuput', self.disableOuput)  
        self.configs.setValue('pyDesigner', self.pyDesigner)
        self.configs.setValue('ignoreList', self.ignoreList)  
                
    def readAndApplySettings(self):                  
        self.initalizeScripts =  self.configs.value('initalizeScripts',1,bool)
        self.scriptsDirName = self.configs.value('scriptsDirName','J:\devcon-scripts')
        self.scriptsPath = os.path.abspath(self.scriptsDirName)
        self.pluginsVerbose = self.configs.value('pluginsVerbose',1,bool)
        self.ignoreList = self.configs.value('ignoreList',['dropboxPkg','\.'])
        self.disableOuput = self.configs.value('disableOuput',1,bool)
        self.pyDesigner = self.configs.value('pyDesigner','C:\Python34\Lib\site-packages\PyQt5\designer.exe')
                        
    def readAndApplySettingsFinal(self):    
        #UI Settings
        pos = self.configs.value('winPos', QPoint(200, 200))
        size = self.configs.value('winSize', QSize(400, 400))
        state = self.configs.value('winDockState')
        if(state and pos and size):
            self.move(pos)
            self.resize(size)            
            self.restoreState(state)
                            