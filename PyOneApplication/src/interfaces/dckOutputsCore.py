'''
Created on Oct 23, 2015

@author: MUKUND
'''


from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt, )
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, )
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
#from PyQt5.uic.Compiler.qtproxies import QtWidgets

from time import strftime
import os
import sys
import html2text

import dckOutputs  
import version

class SysOutputs(dckOutputs.Ui_DockWidget):
    '''
    classdocs
    '''

    def __init__(self,parent):
        '''
        Constructor        
        '''
        self.parent = parent
        
    def initialize(self, configs):   
        self.configs = configs
        if not self.configs.disableOuput:        
            print("Standard outputs and errors redirected to the system... "+ self.__class__.__name__)
            sys.stdout = self
            sys.stderr = self
        
        self.logFile = os.path.join(self.configs.logPath,'PyOneLog_' + str(strftime("%Y-%m-%d_%H-%M-%S")) + '.log')
        if self.configs.logEnable: self.parent.ttls.makePathForFile(self.logFile)
        if self.configs.logEnable: self.parent.ttls.writeFileContent(self.logFile,'')
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.textEdit.setFont(font)
        self.textEdit.setMarginsFont(font)
        
        self.textEdit.setMarginSensitivity(1, True)
        self.textEdit.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.textEdit.setEolMode(Qsci.QsciScintilla.EolUnix)
        self.textEdit.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.textEdit.setAutoCompletionThreshold(1)
        self.textEdit.setAutoIndent(True)
        self.textEdit.setIndentationsUseTabs(True)
        self.textEdit.setTabWidth(4)
        self.textEdit.setMarginLineNumbers(1, 1)
        self.textEdit.setMarginWidth(1, 55)        
        self.textEdit.setAutoCompletionFillupsEnabled(True)
        self.textEdit.setBraceMatching(Qsci.QsciScintilla.StrictBraceMatch)
        self.textEdit.setUtf8(True)
        self.textEdit.setEolVisibility(False)      
        self.textEdit.setCaretLineVisible(True)
        self.textEdit.setCaretLineBackgroundColor(QColor("#ffe4e4"))
        self.textEdit.setReadOnly(True)

        print (self.parent.aboutInfoPlainText) 
        print ('---------------------------------------')
        print('{0}: {1}'.format('AppName'.ljust(20,'.'), version.__buildAppName__))
        print('{0}: {1}'.format('ProductName'.ljust(20,'.'), version.__buildProductName__))
        print('{0}: {1}'.format('AppDescription'.ljust(20,'.'), version.__buildAppDescription__))
        print('{0}: {1}'.format('CompanyName'.ljust(20,'.'), version.__buildCompanyName__))
        print('{0}: {1}'.format('Copyrights'.ljust(20,'.'), version.__buildCopyrights__))
        print('')
        print('{0}: {1}'.format('Version'.ljust(20,'.'), version.__buildNumber__))
        print('{0}: {1}'.format('Date'.ljust(20,'.'), version.__buildDateTime__))
        print('{0}: {1}'.format('System'.ljust(20,'.'), version.__buildSystem__))
        print('{0}: {1}'.format('Owner'.ljust(20,'.'), version.__buildOwner__))   
        print('')
        print('{0}: {1}'.format('initalizeScripts'.ljust(20,'.'), self.configs.initalizeScripts))
        print('{0}: {1}'.format('scriptsPath'.ljust(20,'.'), os.path.abspath(self.configs.scriptsDirName)))
        print('{0}: {1}'.format('pluginsVerbose'.ljust(20,'.'), self.configs.pluginsVerbose))
        print('{0}: {1}'.format('ignoreList'.ljust(20,'.'), self.configs.ignoreList))
        print('{0}: {1}'.format('disableOuput'.ljust(20,'.'), self.configs.disableOuput))
        print('{0}: {1}'.format('logPath'.ljust(20,'.'), self.configs.logPath))
        print('{0}: {1}'.format('logEnable'.ljust(20,'.'), self.configs.logEnable))
        print('{0}: {1}'.format('pyDesigner'.ljust(20,'.'), self.configs.pyDesigner))
        print('{0}: {1}'.format('decryptValue'.ljust(20,'.'), self.configs.decryptValue))
        print('{0}: {1}'.format('startArgument'.ljust(20,'.'), self.parent.getArg()))
        print('')
        print ('---------------------------------------')
        print ('Initiated!')
        print ('Log Start Time: ' + str(strftime("%Y/%m/%d %H:%M:%S")))
        print ('\n---------------------------------------\n')
        print ('*** Python %s on %s.***' % (sys.version, sys.platform))
        print (sys.copyright)
        print ('')
        print ('Platform: ' + sys.platform)
        print ('Version: ' + str(sys.getwindowsversion()))
        print ('FileSys encodeing: ' + str(sys.getfilesystemencoding()))  
        print ('')     

    def logFileUpdate(self, data):
        if self.configs.logEnable:
            f = open(self.logFile,'a')
            f.write(str(data))
            f.close()

    def write(self, data):
        self.appendPlainOutput(data)

    def appendPlainOutput(self, data):
        self.textEdit.setCursorPosition(self.textEdit.lines(),0)
        self.logFileUpdate(data)
        self.textEdit.insert(str(data))        
        vsb = self.textEdit.verticalScrollBar()
        vsb.setValue(vsb.maximum())    
        hsb = self.textEdit.horizontalScrollBar()
        hsb.setValue(0)        
                                        