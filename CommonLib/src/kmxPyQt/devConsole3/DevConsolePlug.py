from code import InteractiveInterpreter
import code
from importlib.abc import InspectLoader
from threading import Thread
from time import strftime
import atexit

import cgi
import inspect
import mimetypes
import os, sys
import re
import shutil
import traceback
import urllib
import requests
from bs4 import BeautifulSoup
import json
import urllib3
import xmlutils
import logging
import lxml
import subprocess
import xml.etree.ElementTree as ET
import pythoncom, logging
from pylab import *
import sqlite3
import sip
import fatcow_rc
import tarfile

from PyQt5.uic.Compiler.qtproxies import QtWidgets
from PyQt5.QtWidgets import QFileDialog
#from PyQt5.uic import pyuic5
import pkgutil
import inspect
os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), "cacert.pem")

"""
In UI File REPLACE below line
from Qsci.qsciscintilla import QsciScintilla
with this line
from PyQt5.Qsci import QsciScintilla
"""
from PyQt5.Qsci import QsciScintilla
from PyQt5.uic import loadUi
import win32com
import win32com.client
import pprint
from PyQt5 import Qsci
from kmxPyQt import kmxQtMenuBuilder
import argparse

import ssl
from functools import wraps
def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)

def convertToRaw(text):
    """Returns a raw string representation of text"""
    escape_dict={'\a':r'\a',
                 '\b':r'\b',
                 '\c':r'\c',
                 '\f':r'\f',
                 '\n':r'\n',
                 '\r':r'\r',
                 '\t':r'\t',
                 '\v':r'\v',
                 '\'':r'\'',
                 '\"':r'\"'}
    new_string=''
    for char in text:
            try: 
                    new_string += escape_dict[char]
            except KeyError: 
                    new_string += char
    return new_string
    

def errorReport():
    # Show/Return Error Report
    traceback_lines = traceback.format_exc().split('\n')
    data = '\n'.join(traceback_lines)
    print(data)
    return data

def crashHandle():
    # Prepare Report
    data = errorReport()
    f = open('CrashReport.txt', 'w')
    f.write(str(data))
    f.close()
    sys.exit(0)

# Safly Import Additional Modules
try:
    from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
    # import lxml
    # import xlrw
    # import xlrd
except:
    crashHandle()


# Safly Import Custom Modules
try:
    from kmxPyQt.devConsole3.DCwin import Ui_devConsole
    from kmxPyQt.qne import qneblock
    from kmxPyQt import kmxQtTreeWidget
    from kmxPyQt import kmxQtCommonTools
    from kmxGeneral import kmxTools
    from kmxGeneral import kmxDynamicModules
    from kmxPyQt import kmxQtConnections

    import http.server
    #from devPlugs import *

except:
    crashHandle()


class DevConsole(QtWidgets.QMainWindow, QtWidgets.QDialog, Ui_devConsole):
    '''
    DevConsole
    self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)
    self.qtTools.applyStyle()
    dv = self.qtTools.getIconString('/04/16/39.png')
    self.qtConsole = DevConsolePlug.DevConsole(self.win,
                                                ShowPrint=True,
                                                ShowError=True,
                                                StatusBar=self.win.statusBar,
                                                AsDock=True,
                                                InitalizeScripts=True,
                                                logCount=30,
                                                btnIcon=dv,
                                                addObj=self)

    Arguments:
    ShowPrint... Captures all print outputs to DevConsole o/p
    ShowError... Captures all error info outputs to DevConsole o/p

    Methods:
    appendPlainOutput(txt) ... Append plain text into DevConsole o/p
    appendSplOutput(txt) ... Append TimeStamped text into DevConsole o/p

    '''

    def __init__(self, parent=None,
                    ShowPrint=True,
                    ShowError=True,
                    StatusBar=None,
                    AsDock=False,
                    logCount=30,
                    ScriptsPath='Scripts/',
                    InitalizeScripts=True,
                    btnText="Console",
                    btnIcon="F:/04/06/29.PNG",
                    addObj=None):
        '''
        Parent - Pass QWIDGET based objects. Else I will create my own.
        ShowPrint - Redirect standard prints
        ShowError - Redirect standard errors
        StatusBar - Attach DevC Invoke button to this status bar else You should invoke DevC explicitly
        AsDock - If True creates DevC as a dock else as a dialog window
        '''
        last_update_date='July 02 2015' # July 02 2015 , Jan 12 2013 
        self.addObj = addObj
        self.parent = parent
        self.asDock = AsDock
        self.logCount = logCount
        self.history = []
        super(DevConsole, self).__init__(self.parent)
        atexit.register(self.writeToLog)

        self.nodesDirName = 'nodes'

        # Load File
        self.loadedFile = False
        self.loadedFileName = ''
        self.pyDesigner = 'C:\Python34\Lib\site-packages\PyQt5\designer.exe'
                
        #Flags        
        self.qtTools = kmxQtCommonTools.CommonTools(self)
        self.ttls = kmxTools.Tools()
        self.qtTree = kmxQtTreeWidget.TreeWidget()
        self.qtMenu = kmxQtMenuBuilder.MenuBuilder()
        self.qtConn = kmxQtConnections.QtConnections(self)
        self.qtIcon = kmxQtCommonTools.iconSetup(self)

        self.standalone = 0 if self.parent else 1

        if self.standalone:
            print ('No parent specified! Creating standalone console!')
            self.parent = self.win = QtWidgets.QMainWindow()
            self.win.resize(689, 504)
                        
            self.mainWidget = QtWidgets.QWidget(self.win)
            self.setupUi(self.mainWidget)
            self.win.setCentralWidget(self.mainWidget)
            self.toolbar = QtWidgets.QToolBar('Main Tools',self)
            self.toolbar2 = QtWidgets.QToolBar('Additional Tools',self) 
            self.toolbar.setFloatable(True)           
            self.toolbar2.setFloatable(True)
            self.win.addToolBar(self.toolbar)
            self.win.addToolBar(self.toolbar2)            
            self.setStandAloneModeFeatures()

            self.btnExecute.setVisible(0)
            self.btnLoadScript.setVisible(0)
            self.btnSaveScript.setVisible(0)
            self.btnNewScript.setVisible(0)
            self.btnQuickSaveScript.setVisible(0)
            
            self.label.setVisible(1)
            self.label.setText('Output:')
            self.line.setVisible(0)
            #self.sciOutput.resize(self.sciOutput.width(), self.sciOutput.height() + 90)                         
                               
        elif self.asDock:
            if hasattr(self.parent, 'addDockWidget'):
                print ('Creating dock based console!')
                self.win = QtWidgets.QDockWidget(self.parent)
                base = QtWidgets.QWidget()
                self.setupUi(base)
                self.win.setWidget(base)
                self.parent.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.win)

                # print ('Creating dock based console!')
                # self.dck = QtWidgets.QDockWidget(self.parent)
                #
                # dlg = QtWidgets.QWidget()
                #
                # self.win = QtWidgets.QMainWindow()
                # lyt = QtWidgets.QVBoxLayout()
                # lyt.addWidget(self.win)
                # wdgt = QtWidgets.QWidget(self.dck)
                # self.setupUi(wdgt)
                # self.win.setCentralWidget(wdgt)
                #
                # dlg.setLayout(lyt)
                #
                # self.dck.setWidget(dlg)
                # self.parent.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dck)


            else:
                print ('Unsupported Parent for creating dock based console! ' + str(self.parent))
                print ('Connecting console to given parent as a dialog...' + str(self.parent))
                self.win = QtWidgets.QDialog(self.parent)
                self.setupUi(self.win)
        else:
            print ('Connecting console to given parent as a dialog...' + str(self.parent))
            self.win = QtWidgets.QDialog(self.parent)
            self.setupUi(self.win)

        self.outputFont = self.sciOutput.font()
        self.outputFont.setFamily("Courier")
        self.outputFont.setPointSize(10)
        self.outputFont.setFixedPitch(True)
        self.sciOutput.setFont(self.outputFont)
        self.sciOutput.setMarginsFont(self.outputFont)

        print("Outputs Redirected to HaPy. Check HaPy console log for furthur system messages.")
        if ShowPrint: sys.stdout = self
        if ShowError: sys.stderr = self

        self.inter = InteractiveInterpreter()
        self.inter.locals['dev'] = self       
        globals()['dev'] = self

        self.win.setWindowIcon(self.parent.windowIcon())
        self.win.setWindowTitle('HaPy')

        self.PLX = Qsci.QsciLexerPython(self)
        self.ABS = Qsci.QsciAPIs(self.PLX)
        # self.PLX.setAPIs(self.ABS)
        self.ABS.prepare()

        self.sciOutput.setReadOnly(1)
        self._setQSci(self.sciOutput)

        # Connections
        self.tabWidget.tabCloseRequested.connect(self.tabClose)
        
        if not self.standalone:
            self.btnExecute.clicked.connect(self.btnRedirector)
            #self.btnExecute_2.clicked.connect(self.btnRedirector)
            self.btnLoadScript.clicked.connect(self.btnRedirector)
            self.btnSaveScript.clicked.connect(self.btnRedirector)
            self.btnNewScript.clicked.connect(self.btnRedirector)
            self.btnQuickSaveScript.clicked.connect(self.btnRedirector)
        
        self.qtTools.connectToRightClick(self.treeWidget,self.pluginRightClick)

        self.cline.returnPressed.connect(self.commandLineExecute)
        self.cline.__class__.keyReleaseEvent = self.commandLineKeyPress
        self.tabWidget.__class__.keyReleaseEvent = self.tabKeyPress
        
        if StatusBar:
            self.stsBtnDebugger = QtWidgets.QToolButton(self.parent)
            self.stsBtnDebugger.setText(btnText)
            self.stsBtnDebugger.setToolTip(btnText)
            self.stsBtnDebugger.setAutoRaise(1)
            self.stsBtnDebugger.setMaximumHeight(18)
            StatusBar.addPermanentWidget(self.stsBtnDebugger, 0)
            self.stsBtnDebugger.clicked.connect(self.btnRedirector)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(btnIcon), QtGui.QIcon.Normal, QtGui.QIcon.On)
            self.stsBtnDebugger.setIcon(icon)
        else:
            self.stsBtnDebugger = None

        self.win.hide()

        # Plugin Lister
        #self.treeWidget.headerItem().setText(0, "DevS")
        self.treeWidget.itemDoubleClicked.connect(self.pluginSelected)

        self.treeWidget.setVisible(False)

        print ('---------------------------------------')
        print ('HaPy - Handy Python') 
        print ('Interactive Interpreter')
        print ('---------------------------------------')
        print ('Initiated!')

        print ('\nLog Start Time: ' + str(strftime("%Y/%m/%d %H:%M:%S")))
        print ('\n---------------------------------------\n')
        print ('*** Python %s on %s.***' % (sys.version, sys.platform))
        print (sys.copyright)
        print ('')
        print ('Platform: ' + sys.platform)
        print ('Version: ' + str(sys.getwindowsversion()))
        print ('FileSys encodeing: ' + str(sys.getfilesystemencoding()))

        drline = "\n---------------------------------------\n"
        self.credit = drline + 'About HaPy:\nHandy Python - Interactive Interpreter/Scripting Environment \nAn expreimental project by \nKumaresan Lakshmanan\nFor Quick, Portable windows automation. \nDate: ' + last_update_date + drline
        print(self.credit)

        self.InitalizeScripts = InitalizeScripts
        self.scriptsDirName = ScriptsPath
        self.scriptsPath = os.path.abspath(self.scriptsDirName)
        print("Checking scripts path..."+ os.path.abspath(self.scriptsPath))
        if self.scriptsPath:
            if self.InitalizeScripts and self.scriptsPath and not os.path.exists(self.scriptsPath):
                os.makedirs(self.scriptsPath)
        else:
            print ('Invalid script path!')

        #Start loading the scripts...
        try:
            self.execPlugin()
            self.treeWidget.setVisible(True)
        except:
            print (errorReport())

        try:
            if self.InitalizeScripts:
                self.execStartUp()
            else:
                self.addEmptyTab()
        except:
            print (errorReport())
          
        if self.standalone:            
            self.qtConn.uiMain = self.win
            self.qtConn.installEventHandler()
            self.qtConn.addEventConnection(self.win, 'WindowDeactivate', self.onWinDeAct)
            self.qtConn.addEventConnection(self.win, 'Close', self.onClose)
            self.qtConn.addEventConnection(self.win, 'Hide', self.onHide)
            self.qtConn.addEventConnection(self.win, 'Show', self.onShow)
            
            if (os.path.exists('layout.lyt')):  
                customList = self.qtTools.uiLayoutRestore('layout.lyt',[self.splitter,self.splitter_2])
                if(customList):
                    self.win.resize(customList[0])
                    self.win.move(customList[1])                                
            self.loadTabs()            

    def onWinDeAct(self, *arg):
        #self.win.hide()
        pass

    def _handleTrayItemClicked(self, itemName):
        pass
        
    def trayItemClicked(self, *arg):
        caller = self.sender()        
        itm = caller.text()
        if(itm=='Quit'):
            sys.exit(0)
        if(itm=='About'):
            print(self.credit)
        if(itm=='Help'):
            print('Not Implemented')
        
    def trayAgentReady(self):    
        """
        trayagent(forwho,trayclickedfunction)
    
        catch the trayobj i trhough...
        Dont forget to kill your object on Close Event
        use...
        xtools.traykiller()
    
        """
        self.tray = QtWidgets.QSystemTrayIcon(self.qtIcon.getIcon('action_log.png'), self.win)
        self.tray.activated.connect(self.trayClicked)
        #self.connect(self.tray,SIGNAL("activated(QSystemTrayIcon::ActivationReason)"),self.trayClicked)
        self.tray.show()
        return self.tray
    
    def trayClicked(self, click):
                         
        if(click==3): 
            if (self.win.isVisible()):
                self.win.hide()
            else:
                self.win.show()
                #if self.win.windowState() == QtCore.Qt.WindowMinimized: 
                self.win.setWindowState(QtCore.Qt.WindowActive)
                self.win.activateWindow()     
                self.win.raise_()
               
    def traymessage(self, messagetitle, message):
        self.tray.showMessage(messagetitle,message)
    
    def traykiller(self):
        self.tray.hide()
        del(self.tray)
        
    def onClose(self,*arg):
        print("Closing...")
        self.traykiller()
        customList = [self.win.size(),self.win.pos()]
        self.qtTools.uiLayoutSave('layout.lyt',[self.splitter,self.splitter_2], customList)
        self.saveTabs()
        self.writeToLog()
        
    def onHide(self, *arg):
        #print("Hide")
        #self.win.setWindowFlags(QtCore.Qt.ToolTip)
        pass

    def onShow(self, *arg):
        #print("Show")
        #self.win.setWindowFlags(QtCore.Qt.Window)
        pass
        
    def saveTabs(self):
        lst=[]
        for cnt in range(0, self.tabWidget.count()):
            wdgt = self.tabWidget.widget(cnt)
            #'userSetup.py'
            lst.append(wdgt.toolTip())
            
        current = self.tabWidget.currentIndex()
        lst.append(current)
        self.qtTools.quickSave(lst, "tabs.tbs")
        
    def loadTabs(self):
        if (os.path.exists('tabs.tbs')):
            lst = self.qtTools.quickLoad("tabs.tbs")
            for cnt in range(0, len(lst)-1):
                if 'New Script' in lst[cnt]:
                    self.addEmptyTab()
                elif 'userSetup.py' in lst[cnt]:
                    continue
                else:
                    if (os.path.exists(lst[cnt])):
                        self.addNewTab(lst[cnt])
            index = lst[len(lst)-1]
            self.tabWidget.setCurrentIndex(index)
                
    def getUpdatedLocals(self):
        try:
            raise None
        except:
            frame = sys.exc_info()[2].tb_frame.f_back
        # evaluate commands in current namespace
        namespace = frame.f_globals.copy()
        namespace.update(frame.f_locals)
        return namespace

    def addShortcut(self, label='text', icon='bullet_star.png', callBackFn=None):
        if (text=='|'):
            self.toolbar2.addSeparator()
        else:
            action = QtWidgets.QAction(self)
            action.setText(label)
            if callBackFn is not None: action.triggered.connect(callBackFn)
            self.qtIcon.setIcon(action, icon)                        
            self.toolbar2.addAction(action)         

    def setStandAloneModeFeatures(self):
        """
        Standalone Mode
        :return:
        """
        # Ready Menu Bar
        self.menubar = self.qtMenu.createMenuBar(self.win)
        self.mnuFile = self.qtMenu.createMenu(self.menubar, "File")
        self.mnuEdit = self.qtMenu.createMenu(self.menubar, "Edit")
        self.mnuRun = self.qtMenu.createMenu(self.menubar, "Run")
        self.mnuAbout = self.qtMenu.createMenu(self.menubar, "About")

        self.mnuFileNewScript = self.qtMenu.createMenuItem(self.win, self.mnuFile, "New Script", self.btnRedirector)
        self.qtMenu.createMenuItemSeperator(self.mnuFile)        
        self.mnuFileLoadScript = self.qtMenu.createMenuItem(self.win, self.mnuFile, "Load Script", self.btnRedirector)
        self.mnuFileQuickSaveScript = self.qtMenu.createMenuItem(self.win, self.mnuFile, "Save Script", self.btnRedirector)
        self.mnuFileSaveScript = self.qtMenu.createMenuItem(self.win, self.mnuFile, "Save Script As", self.btnRedirector)
        self.qtMenu.createMenuItemSeperator(self.mnuFile)
        self.mnuFileQuit = self.qtMenu.createMenuItem(self.win, self.mnuFile, "Quit", self.btnRedirector)

        self.mnuEditClearOutput = self.qtMenu.createMenuItem(self.win, self.mnuEdit, "Clear Outputs", self.btnRedirector)
        self.mnuEditClearInput = self.qtMenu.createMenuItem(self.win, self.mnuEdit, "Clear Inputs", self.btnRedirector)

#        self.mnuRunExecuteNoClear = self.qtMenu.createMenuItem(self.win, self.mnuRun, "Execute Script + No Clear", self.execute_Clicked_NoClear)
#        self.mnuRunExecuteNoClear.setShortcut("Ctrl+Enter")
        self.mnuRunExecute = self.qtMenu.createMenuItem(self.win, self.mnuRun, "Execute Script", self.doExecute)
        self.mnuRunExecute.setShortcut("Ctrl+Enter")

        self.mnuAboutHPSE = self.qtMenu.createMenuItem(self.win, self.mnuAbout, "About HaPy", self.btnRedirector)


        self.qtIcon.setIcon(self.mnuFileNewScript, 'page.png')
        self.qtIcon.setIcon(self.mnuFileLoadScript, 'page_edit.png')
        self.qtIcon.setIcon(self.mnuFileQuickSaveScript, 'page_save.png')
        self.qtIcon.setIcon(self.mnuFileSaveScript, 'page_green.png')
        self.qtIcon.setIcon(self.mnuEditClearOutput, 'align_bellow.png')
        self.qtIcon.setIcon(self.mnuEditClearInput, 'align_above.png')        
        self.qtIcon.setIcon(self.mnuRunExecute, 'page_lightning.png')
        self.qtIcon.setIcon(self.mnuAboutHPSE, 'emotion_happy.png')           
                
        self.toolbar.addAction(self.mnuFileNewScript)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.mnuFileLoadScript)
        self.toolbar.addAction(self.mnuFileQuickSaveScript)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.mnuEditClearOutput)
        #self.toolbar.addAction(self.mnuEditClearInput)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.mnuRunExecute)
        
        #self.toolbar.addWidget(self.mnuFileLoadScript)
        self.tray = self.trayAgentReady()
        #self.rightMenu = self.qtMenu.createMenuForList(self, 'DevConsoleMenu', ['|','Help','About','|','Quit'], self.trayItemClicked)
        self.rightMenu = self.qtMenu.createMenu(None, 'DevConsoleMenu')
        self.tray.setContextMenu(self.rightMenu)
        self.updateTrayMenu('Quit',self.trayItemClicked)
        self.updateTrayMenu('|')
        self.updateTrayMenu('About',self.trayItemClicked)
        self.updateTrayMenu('Help',self.trayItemClicked)
        
        #self.setWindowFlags(QtCore.Qt.Tool)

        '''
        # Remove other buttons
        self.btnClearOutput.setVisible(0)
        self.toolButton.setVisible(0)
        self.line_5.setVisible(0)
        self.line_6.setVisible(0)
        self.line_7.setVisible(0)

        self.btnLoadScript.setVisible(0)
        self.btnSaveScript.setVisible(0)
        self.line.setVisible(0)

        self.btnClearInput.setVisible(0)
        self.btnExecute.setVisible(0)
        self.line_2.setVisible(0)
        self.line_3.setVisible(0)
        self.line_4.setVisible(0)

        self.sciOutput.resize(self.sciOutput.width(), self.sciOutput.height() + 90)
        self.label.setText("Output:")
        self.label_2.setText("Workspace:")
        self.label_3.setText("Quick Commands:")
        '''
    def updateTrayMenu(self, itemName, fnToCall=None):
        self.qtMenu.updateMenu(self,  self.rightMenu, itemName, fnToCall)
        
    def pluginRightClick(self, point):
        #menu = ['m1','m2',['m3','m31',['m32','m321','m322'],'m33'],'m4','m5',['m6','m61','m62'],'m7']
        #self.qtTools.popUpMenuAdv(menu,self.treeWidget,point,self.pluginRightClickSelected,'addedArgument')
        item = self.treeWidget.itemAt(point)
        
        if(item):
            name = item.text(0)
            path = item.data(0,QtCore.Qt.UserRole)
            if (os.path.exists(path)):
                if (os.path.isfile(path)):
                    #Edit - File (If UI File there, Edit them) 
                    uiFile = item.data(0,QtCore.Qt.UserRole).replace('.py','.ui')            
                    if (os.path.exists(uiFile)):
                        self.qtTools.popUpMenu(self.treeWidget,point,["Edit","Edit UI","Delete"],self.pluginRightClickSelected,["myarg1","myarg2"])
                    else:
                        self.qtTools.popUpMenu(self.treeWidget,point,["Edit","Delete"],self.pluginRightClickSelected,["myarg1","myarg2"])
                else:
                    #Directories - Nodes or Other dir
                    if (name == "nodes"):
                        self.qtTools.popUpMenu(self.treeWidget,point,["New Node"],self.pluginRightClickSelected,["myarg1","myarg2"])
                    else:
                        self.qtTools.popUpMenu(self.treeWidget,point,["New Simple Plug","New UI Plug","New Folder","Refresh"],self.pluginRightClickSelected,["myarg1","myarg2"])
            else:
                #Empty area - right clicked or unknown path.
                self.qtTools.popUpMenu(self.treeWidget,point,["New Simple Plug","New UI Plug","New Folder","Refresh"],self.pluginRightClickSelected,["myarg1","myarg2"])
        else:
            self.qtTools.popUpMenu(self.treeWidget,point,["New Simple Plug","New UI Plug","New Folder","Refresh"],self.pluginRightClickSelected,["myarg1","myarg2"])
            
    def pluginRightClickSelected(self,*arg):
        act = self.parent.sender()
        menuOption = act.text()
        item = self.treeWidget.itemAt(act.data())
        itemSelected = item.text(0) if item else None
        path = item.data(0,QtCore.Qt.UserRole) if item else self.scriptsPath
        if(menuOption=="Refresh"):
            self.execPlugin()
        if(menuOption=="New Folder"):
            nFolderName = self.qtTools.showInputBox("ScriptFolderName","Enter the new folder name", "folderName")
            if (nFolderName):
                newPath = os.path.join(path,nFolderName)
                os.makedirs(newPath, exist_ok=True)
                self.execPlugin()
        if(menuOption=="New Node"):
            nFileName = self.qtTools.showInputBox("ScriptName","Enter the new Node name", "newNode")
            if (nFileName):               
                data = self.ttls.fileContent('templateNode.py')
                data = data.replace('Add', nFileName.capitalize())
                f = os.path.join(path, nFileName+".py")
                self.ttls.writeFileContent(f, data)
                self.execPlugin()
                self.addNewTab(f)
        if(menuOption=="New Simple Plug"):          
            nFileName = self.qtTools.showInputBox("PlugName","Enter the new Plug name", "newPlug")   
            if (nFileName):            
                data = self.ttls.fileContent('templatePlug.py')
                data = data.replace('myClass', nFileName)
                f = os.path.join(path, nFileName+".py")
                self.ttls.writeFileContent(f, data)
                self.execPlugin()
                self.addNewTab(f)
        if(menuOption=="New UI Plug"):
            nFileName = self.qtTools.showInputBox("PlugName","Enter the new UI Plug name", "newUIPlug")
            if (nFileName):
                pyf = os.path.join(path, nFileName+".py")
                uif = os.path.join(path, nFileName+".ui")                
                data = self.ttls.fileContent('templateUIPlug.py')
                data = data.replace('UI_myUIPlug.ui', uif)                
                data = data.replace('myUIPlug', nFileName)                
                self.ttls.writeFileContent(pyf, data)
                self.execPlugin()
                self.addNewTab(pyf)                
                data = self.ttls.fileContent('templateUIPlug.ui')
                self.ttls.writeFileContent(uif, data)
                print("Created..." + pyf)
                print("Created..." + uif)
        if(menuOption=="Edit"):
            pyFile = (item.data(0,QtCore.Qt.UserRole))
            self.addNewTab(pyFile)
        if(menuOption=="Edit UI"):
            uiFile = item.data(0,QtCore.Qt.UserRole).replace('.py','.ui')
            args = '"' + self.pyDesigner + '"' + " " + '"' + uiFile + '"'
            print("Execute: (" + args + ")")
            subprocess.call(args)                        
        if(menuOption=="Delete"):
            pyFile = item.data(0,QtCore.Qt.UserRole)
            uiFile = pyFile.replace('.py','.ui')
            try:
                if(os.path.exists(pyFile)):
                    print("Deleting..." + pyFile)
                    os.remove(pyFile)
                if(os.path.exists(uiFile)):
                    print("Deleting..." + uiFile)
                    os.remove(uiFile)
                self.execPlugin() 
            except OSError:
                pass    
       
    def pluginSelected(self, *eve):
        selectedItem = eve[0]
        itemInfo = self.qtTree.getItemLabel(selectedItem)
        name = itemInfo['Label']
        path = itemInfo['Data']
        if(os.path.isfile(path)):
            print("\nExecuting: " + path)
            if not (self.nodesDirName in path):
                content = self.ttls.fileContent(path)
                self.runScript(content)
            else:
                self.addNewTab(path)

    def showAttrs(self, obj):
        dlg = QtWidgets.QDialog(self.win)
        dlg.setWindowTitle(str(type(obj)))
        lt = QtWidgets.QListWidget(dlg)
        for each in inspect.getmembers(obj):
            itm = QtWidgets.QListWidgetItem()
            attrName = str(each[0])
            fnSymbol = ""
            if(inspect.isfunction(each[1]) or inspect.ismethod(each[1])):
                args = inspect.getargspec(each[1])[0]
                fnSymbol = "(" + str(args) + ")"
            itm.setText(attrName + fnSymbol)
            lt.addItem(itm)
        dlg.setFixedHeight(190)
        dlg.setFixedWidth(255)
        dlg.show()

    def execPlugin(self, *arg):
        self.populatePlugins()
        
    def populatePlugins(self):
        self.treeWidget.clear()
        
        print("Loading Plugins... ")
        spath = os.getcwd()
        if('\.' in spath): return None
        self.addToSysPath(spath)
        self.addToSysPath(self.scriptsPath)
                
        for eachItem in os.listdir(self.scriptsPath):
            currentDirName = eachItem
            currentDirPath = os.path.join(self.scriptsPath,currentDirName)
            
            if (not "__" in currentDirPath):
                if os.path.isdir(currentDirPath):
                    rItem = self.qtTree.createItem(currentDirName, currentDirPath)
                    self.qtTree.addNewRoot(self.treeWidget, rItem)
                    self.populatePluginsCore(rItem, currentDirPath)
                else:
                    self.loadPlugin(currentDirPath)
        
        print("Plugins Loaded!")
                                                
    def populatePluginsCore(self, parentItem, searchPath):                
        if('\.' in searchPath): return None
        self.addToSysPath(searchPath)        
        for eachItem in os.listdir(searchPath):
            currentDirName = eachItem
            currentDirPath = os.path.join(searchPath,currentDirName)    
            if (not "__" in currentDirPath):
                if os.path.isdir(currentDirPath):                
                    rItem = self.qtTree.createItem(currentDirName,currentDirPath)
                    self.qtTree.addChild(rItem, parentItem)
                    self.populatePluginsCore(rItem, currentDirPath)
                else:
                    self.loadPlugin(currentDirPath, parentItem)                
        
    def addToSysPath(self, path):
        path = os.path.abspath(path)
        if('\.' in path): return None
        print ("Adding path to system... " + path)
        code = r'''import sys,os
path2Add="%s"
if path2Add not in sys.path and os.path.exists(path2Add):
    sys.path.append(path2Add)
''' % (path).replace(os.path.sep,'/')
        self.runScript(code)

    def loadPlugin(self, plugFile, parentTreeItem=None):   
        if('\.' in plugFile): return None
        modName = os.path.basename(plugFile).replace(os.path.splitext(plugFile)[1], '')
        content = self.ttls.fileContent(plugFile)
        expecting = "For DevConsole" 
        if(expecting in content):
            item = self.qtTree.createItem(modName, plugFile)
            if(parentTreeItem is None):
                plugTreeItem = self.qtTree.addNewRoot(self.treeWidget, item)
            else:
                plugTreeItem = self.qtTree.addChild(item, parentTreeItem)
            print("Adding Plug... " + plugFile)
        else:
            print("Skipped Plug! (Add tag 'For DevConsole') " + plugFile)
            plugTreeItem = None
        #self.runScript(content)
        return plugTreeItem

    def execStartUp(self, *arg):
        self.userSetup = os.path.join(self.scriptsPath, 'userSetup.py')
        self.userSetup = self.userSetup if os.path.exists(self.userSetup) else os.path.join(self.scriptsPath, 'userSetup.pyc')
        self.userSetup = self.userSetup if os.path.exists(self.userSetup) else ''
        if self.userSetup and os.path.exists(self.userSetup):
            print ('Executing... %s' % self.userSetup)
            data = self.ttls.fileContent(self.userSetup)
            self.loadScriptCore(self.userSetup)
            self.runScript(data)
        else:
            print ('No Startup script file! ' + self.userSetup)

    def commandLineExecute(self):
        if not str(self.cline.text()) == '':
            inputs = str(self.cline.text()).rstrip()
            self.appendPlainOutput(">>> " + inputs)
            self.appendLineOutput()
            self.addToHistory(inputs)
            self.runScript(inputs)
            self.cline.setText('')

    def tabKeyPress(self, event):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if (modifiers == QtCore.Qt.ControlModifier and event.key()==QtCore.Qt.Key_S):
            self.quickSave()
            
        if (modifiers == QtCore.Qt.ControlModifier and event.key()==QtCore.Qt.Key_N):
            self.addEmptyTab()
        #print(modifiers == QtCore.Qt.ControlModifier and event.key()==16777221)
        
    def commandLineKeyPress(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self.setCommand(self.getPrevHistoryEntry())
            return
        elif event.key() == QtCore.Qt.Key_Down:
            self.setCommand(self.getNextHistoryEntry())
            return

    def setCommand(self, command):
        self.cline.setText(command)

    def tabClose(self,tabIndex):
        cnt = self.tabWidget.count()
        if(cnt>1):
            #proceed closing the tab
            self.tabWidget.removeTab(tabIndex)

    def addEmptyTab(self):
        newTab = QtWidgets.QWidget()
        self.tabWidget.addTab(newTab, 'New Script')
        newTab.setToolTip('New Script')
        self.tabWidget.setCurrentWidget(newTab)

        tabGrid = QtWidgets.QGridLayout(newTab)
        tabGrid.setContentsMargins(2, 2, 2, 2)
        newSciInput = QsciScintilla(newTab)
        newSciInput.setFrameShape(QtWidgets.QFrame.Box)
        tabGrid.addWidget(newSciInput, 0, 0, 1, 1)
        self._setQSci(newSciInput)
        newSciInput.setText('')
        newSciInput.setFocus()

    def addNewTab(self,scriptFile):
        print("Loading tab..." + scriptFile)
        fileName = os.path.basename(scriptFile)

        newTab = QtWidgets.QWidget()
        self.tabWidget.addTab(newTab, fileName)
        newTab.setToolTip(scriptFile)
        self.tabWidget.setCurrentWidget(newTab)

        tabGrid = QtWidgets.QGridLayout(newTab)
        tabGrid.setContentsMargins(2, 2, 2, 2)
        newSciInput = QsciScintilla(newTab)
        newSciInput.setFrameShape(QtWidgets.QFrame.Box)
        tabGrid.addWidget(newSciInput, 0, 0, 1, 1)
        self._setQSci(newSciInput)
        data = str(self.ttls.fileContent(scriptFile))
        newSciInput.setText(data)

    def _setQSci(self, newSciInput):
        newSciInput.setEolMode(Qsci.QsciScintilla.EolUnix)
        newSciInput.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        newSciInput.setLexer(self.PLX)
        newSciInput.setAutoCompletionThreshold(1)
        newSciInput.setAutoIndent(True)
        newSciInput.setIndentationsUseTabs(False)
        newSciInput.setAutoCompletionFillupsEnabled(True)
        newSciInput.setBraceMatching(Qsci.QsciScintilla.StrictBraceMatch)
        newSciInput.setMarginLineNumbers(1, 1)
        newSciInput.setMarginWidth(1, 45)
        newSciInput.setUtf8(True)
        newSciInput.setEolVisibility(False)
        #newSciInput.setWrapMode(Qsci.QsciScintilla.WrapMode(Qsci.QsciScintillaBase.SC_WRAP_WORD))
        #newSciInput.setWrapVisualFlags(Qsci.QsciScintilla.WrapVisualFlag(Qsci.QsciScintilla.WrapFlagByBorder), Qsci.QsciScintilla.WrapVisualFlag(Qsci.QsciScintilla.WrapFlagNone), 0)

    def quickSave(self):
        (qsci,scriptName) = self.getCurrentEditor()
        if (scriptName!='New Script'):
            self.saveQSCItoFile(qsci,scriptName)
            #self.qtTools.showInfoBox('Quick Save', 'File Saved!')
            print("Quick Saved! - " +str(scriptName))
        else:
            self.saveScriptAs()

    def saveScriptAs(self):
        scpt = self.scriptsPath
        scpt = scpt if os.path.exists(scpt) else 'C:'
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getSaveFileName(self.win, 'Save python script file...', scpt, 'Python(*.py);;All Files (*)', options=options)
        
        if (fileName and fileName[0] != ''):
            fileName = fileName[0]
            self.saveScriptCore(fileName)
            #Close and Reload Tab
            cin = self.tabWidget.currentIndex()
            self.tabClose(cin)
            self.loadScriptCore(fileName)

    def saveScriptCore(self,fileName):
        (qsci,scriptName) = self.getCurrentEditor()
        self.saveQSCItoFile(qsci,fileName)

    def saveQSCItoFile(self,qsci,fileName):
        self.ttls.writeFileContent(fileName, qsci.text())

    def loadScript(self):
        scpt = self.scriptsPath
        scpt = scpt if os.path.exists(scpt) else 'D:'
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getOpenFileName(self.win, 'Open python script file...', scpt, 'Python(*.py);;All Files (*)', options=options)
        if fileName and fileName[0] != '' and os.path.exists(fileName[0]):
            fileName = fileName[0]
            self.loadScriptCore(fileName)

    def loadScriptCore(self,fileName):
        self.addNewTab(fileName)

    def btnRedirector(self):
        actingButton = self.parent.sender()     
        scpt = self.scriptsPath
        scpt = scpt if os.path.exists(scpt) else 'D:'
        
        #if actingButton == self.toolButton:
        #    self.treeWidget.setVisible(self.toolButton.isChecked())
        if actingButton == self.stsBtnDebugger:
            if self.win.isVisible():
                self.win.hide()
            else:
                self.win.show()
        elif (actingButton == self.btnNewScript or (self.standalone and actingButton == self.mnuFileNewScript)):
            self.addEmptyTab()
        elif (actingButton == self.btnQuickSaveScript or (self.standalone and actingButton == self.mnuFileQuickSaveScript)):
            self.quickSave()
        # elif (actingButton == self.btnClearOutput or (self.standalone and actingButton == self.mnuEditClearOutput)):
        #     self.sciOutput.clear()
        #     self.loadedFileName = ''
        #     self.loadedFile = False
        #     self.lblFileLoadInfo.setText('No File Loaded!')
        elif (actingButton == self.btnExecute):
            self.doExecute()
        elif (actingButton == self.btnLoadScript or (self.standalone and actingButton == self.mnuFileLoadScript)):
            self.loadScript()
        elif (actingButton == self.btnSaveScript or (self.standalone and actingButton == self.mnuFileSaveScript)):
            self.saveScriptAs()
        elif (self.standalone and actingButton == self.mnuAboutHPSE):
            print (self.credit)
        elif (actingButton == self.mnuEditClearOutput):
            self.sciOutput.clear()
        elif (actingButton == self.mnuEditClearInput):
            (qsci,scriptName) = self.getCurrentEditor()
            qsci.clear()
        elif (self.standalone and actingButton == self.mnuFileQuit):
            sys.exit(0)
        else:
            print ('Unkown button' + str(actingButton))

    def getCurrentEditor(self):
        cwidget = self.tabWidget.currentWidget()
        lst = cwidget.children()
        if(len(lst)>1):
            qsci = lst[1]
            scriptName = cwidget.toolTip()
            return (qsci,scriptName)

    def mouseLock(self):             
        self.win.grabMouse(QtCore.Qt.WaitCursor)
        self.win.grabKeyboard()
        QtWidgets.QApplication.processEvents()        

    def mouseRelease(self):
        self.win.releaseMouse()
        self.win.releaseKeyboard()
        QtWidgets.QApplication.processEvents()        

    def doExecute(self):
        self.mouseLock()
        (qsci,scriptName) = self.getCurrentEditor()
        if (scriptName!=""):
            print("Executing..."+scriptName)
        if not str(qsci.text()) == '':
            inputs = str(qsci.text()).rstrip()
            self.appendPlainOutput(inputs)
            self.appendLineOutput()
            self.ABS.add(inputs)
            self.ABS.prepare()
            self.runScript(inputs)
        self.mouseRelease()
        
    """
    '''    def runScript(self, script):
            try:
                command = str(script).replace('\r\n', '\n')
                try:
                    #self.inter.compile(commands)
                    res = eval(command, globals(), self.inter.locals)
                    #res = exec(command, globals(), self.inter.locals)
                    #print('Done1')
                except SyntaxError:
                    # self.inter.showtraceback()
                    # exec (command, globals(), locals())
                    res = self.inter.runcode(command)
                    #print('Done2')
                QtWidgets.QApplication.processEvents()
                if res is not None:
                    print(repr(res))
            except SystemExit:
                self.inter.showsyntaxerror()
                crashHandle()
                sys.exit(0)
            except:
                print (errorReport())
    '''
    """
    def runScript(self, script):
        try:
            command = str(script).replace('\r\n', '\n')
            locals = self.getUpdatedLocals()
            self.inter.locals.update(locals)
            try:
                res = self.inter.runcode(command)
            except SyntaxError:
                self.inter.showsyntaxerror()
            QtWidgets.QApplication.processEvents()
            if res is not None:
                print ('\n---------------------------------------\n')
                print(repr(res))
                print ('\n---------------------------------------\n')
        except SystemExit:
            self.inter.showsyntaxerror()
            crashHandle()
            sys.exit(0)
        except:
            print (errorReport())

    def appendPlainOutput(self, txt):
        self.appendTextCore(txt)

    def appendLineOutput(self):
        self.appendTextCore('\n')

    def appendSplOutput(self, txt):
        nowtime = strftime("%Y-%m-%d %H:%M:%S")
        splOutput = str(nowtime) + ' : ' + str(txt)
        self.appendPlainOutput(splOutput)

    def appendLog(self, txt):
        self.appendLineOutput()
        self.appendTextCore(txt)

    def appendTextCore(self, txt):
        self.sciOutput.setCursorPosition(self.sciOutput.lines(),0)
        self.sciOutput.insert(str(txt))
        vsb = self.sciOutput.verticalScrollBar()
        vsb.setValue(vsb.maximum())    
        hsb = self.sciOutput.horizontalScrollBar()
        hsb.setValue(0)        
        
    # Standard Error and Print Capture
    def write(self, txt):
        self.appendPlainOutput(txt)

    def showEditor(self, exec_=0):
        if exec_:
            self.win.exec_()
        else:
            self.win.show()

    def writeToLog(self):
        """
        Write info
        :return:
        """
        curdir = os.getcwd()
        logdir = curdir + '/ConsoleLog'
        if not os.path.exists(logdir):
            os.makedirs(logdir)

        fileList = os.listdir(logdir)
        if len(fileList) >= self.logCount:
            fileToDelete = fileList[0]
            delFile = logdir + '/' + fileToDelete
            os.remove(delFile)

        print ('\nLog End Time: ' + str(strftime("%Y/%m/%d %H:%M:%S")))
        fileName = 'DC' + strftime("%Y%m%d%H%M%S") + '.log'
        logFileName = logdir + '/' + fileName
        self.saveQSCItoFile(self.sciOutput,logFileName)

    def getHistory(self):
        return self.history

    def setHisory(self, history):
        self.history = history

    def addToHistory(self, command):
        if command and (not self.history or self.history[-1] != command):
            self.history.append(command)
        self.history_index = len(self.history)

    def getPrevHistoryEntry(self):
        if self.history:
            self.history_index = max(0, self.history_index - 1)
            return self.history[self.history_index]
        return ''

    def getNextHistoryEntry(self):
        if self.history:
            hist_len = len(self.history)
            self.history_index = min(hist_len, self.history_index + 1)
            if self.history_index < hist_len:
                return self.history[self.history_index]
        return ''

import socket
if __name__ == '__main__':
    try:
        testhere=0
        app = QtWidgets.QApplication(sys.argv)
        if(socket.gethostname()=='MUKUND-PC'):
            dc = DevConsole(ShowPrint=not testhere, ShowError=not testhere, ScriptsPath='J:\devcon-scripts')
        else:
            dc = DevConsole(ShowPrint=True, ShowError=True)
        dc.showEditor()
        sys.exit(app.exec_())
    except:
        crashHandle()
    sys.exit(1)
