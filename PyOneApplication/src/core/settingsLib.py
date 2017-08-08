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
from PyQt5.Qt import QVariant
import string

class settings():
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        self.configs =  QSettings('config.ini',QSettings.IniFormat)
        self.aboutInfo = "The <b>PyOne</b> - Kumar's experimental project for rapid automation of frequent windows activities. Kind of swiss knife for developers.<br> Got some ideas for it? Share with me <a href=\"mailto:kaymatrixgmail.com\">kaymatrix@gmail.com</a>."
        self.aboutInfoPlainText = "The PyOne - Kumar's experimental project for rapid automation of frequent windows activities. \nKind of swiss knife for developers. \nGot some ideas for it? Share with me kaymatrixgmail.com."
        
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
        self.configs.setValue('decryptValue',self.decryptValue)
        self.configs.setValue('logPath',self.logPath)
        self.configs.setValue('logEnable',self.logEnable)
                
    def readAndApplySettings(self):                  
        self.initalizeScripts =  self.configs.value('initalizeScripts',1,bool)
        self.scriptsDirName = self.configs.value('scriptsDirName','userScripts')
        self.scriptsPath = os.path.abspath(self.scriptsDirName)
        self.pluginsVerbose = self.configs.value('pluginsVerbose',1,bool)
        self.ignoreList = self.configs.value('ignoreList',['dropboxPkg','\.'])
        self.disableOuput = self.configs.value('disableOuput',0,bool)
        self.pyDesigner = self.configs.value('pyDesigner','C:\Python34\Lib\site-packages\PyQt5\designer.exe')
        self.decryptValue = self.configs.value('decryptValue','9687',str)
        self.logPath = self.configs.value('logPath','logs',str)
        self.logEnable = self.configs.value('logEnable',1,bool)
                        
    def readAndApplySettingsFinal(self):    
        #UI Settings
        pos = self.configs.value('winPos', QPoint(200, 200))
        size = self.configs.value('winSize', QSize(400, 400))
        state = self.configs.value('winDockState')
        if(state and pos and size):
            self.move(pos)
            self.resize(size)            
            self.restoreState(state)
                            