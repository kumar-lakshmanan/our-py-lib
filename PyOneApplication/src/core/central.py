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

import ssl
from functools import wraps
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)

from code import InteractiveInterpreter
import os
import sys
import subprocess

certificate = os.path.join(os.getcwd(), "cacert.pem")
if(os.path.exists(certificate)):
    os.environ["REQUESTS_CA_BUNDLE"] = certificate

import crashSupport

try:
    from kmxGeneral import kmxTools
    from kmxGeneral import kmxDynamicModules
    from kmxPyQt import kmxQtTreeWidget
    from kmxPyQt import kmxQtCommonTools
    from kmxPyQt import kmxQtConnections
    from kmxPyQt import kmxQtMenuBuilder   
    import fatcow_rc        
    import dckOutputsCore
    import dckPOScriptsCore
    
    import settingsLib
    import traysLib
    import saftyLib
    import executerLib
    import widgetsLib
    
except:
    crashSupport.handleThis()
    
class CoreCentral(settingsLib.settings, traysLib.trays, saftyLib.cryption, executerLib.scriptExecute, widgetsLib.dynamicObjs):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        settingsLib.settings.__init__(self,None)
        widgetsLib.dynamicObjs.__init__(self,None)
        self.qtTools = kmxQtCommonTools.CommonTools(self)
        self.ttls = kmxTools.Tools()
        self.qtTree = kmxQtTreeWidget.TreeWidget()
        self.qtMenu = kmxQtMenuBuilder.MenuBuilder()
        self.qtConn = kmxQtConnections.QtConnections(self)
        self.qtIcon = kmxQtCommonTools.iconSetup(self)

        self.inter = InteractiveInterpreter()
        self.inter.locals['dev'] = self       
        globals()['dev'] = self

    def shutdownActivity(self):
        self.writeSettings()
        self.traykiller()
        self.customShutdownForOverride()
       
    def startupActivity(self):
        self.readAndApplySettings()   
        self.createDynamicTools()
     
        print("Checking custom scripts path..."+ os.path.abspath(self.scriptsPath))               
        if self.scriptsPath:
            if self.initalizeScripts and self.scriptsPath and not os.path.exists(self.scriptsPath):
                os.makedirs(self.scriptsPath)
            if os.path.exists(self.scriptsPath):
                self.scriptsWindow.initializer()                
        else:
            print ('Invalid script path!')

        try:
            if self.initalizeScripts:
                self.execStartUp()
        except:
            crashSupport.handleThis()

        self.readAndApplySettingsFinal()  
        self.customStartupForOverride()          
               
    def customStartupForOverride(self):
        print('Default Custom startup called.')

    def customShutdownForOverride(self):
        print('Default Custom shutdown called.')    
    
    def createDynamicTools(self):
        #Dock Output
        self.outputWindow = dckOutputsCore.SysOutputs(self)
        self.addNewDock(self.outputWindow, 'Output', 'Displays execution and all standard outputs')
        self.outputWindow.initialize(self.disableOuput)
        
        #Dock Scripts list 
        self.scriptsWindow = dckPOScriptsCore.POScripts(self)
        self.addNewDock(self.scriptsWindow, 'PyOneScripts', 'PyOne BuildIN Scripts')


        #System Tray
        self.setupTray()
        
        #Execution Button
        self.actExec = self.addNewAction('Execute', 'Execute the current script!', 'lightning.png')
        self.actExec.setShortcut("Ctrl+Enter")
        self.toolsMenu.addSeparator()
        self.toolsMenu.addAction(self.actExec)
        
        self.editToolBar.addSeparator()
        self.editToolBar.addAction(self.actExec)
                
if __name__ == '__main__':
    import sys
    sys.path.append('J:\our-py-lib\PyOneApplication\src')
    import PyOne
    mainPyOneApp = QtWidgets.QApplication(sys.argv)
    mainPyOneWin = PyOne.PyOneMainWindow(mainPyOneApp)
    mainPyOneWin.show()
    sys.exit(mainPyOneApp.exec_())        