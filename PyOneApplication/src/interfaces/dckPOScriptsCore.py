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
import subprocess

import dckPOScripts  

class POScripts(dckPOScripts.Ui_DockWidget):
    '''
    classdocs
    '''

    def __init__(self,parent):
        '''
        Constructor        
        '''
        self.parent = parent
        
    def initializer(self):
        self.pluginsVerbose = self.parent.pluginsVerbose
        self.ignoreList = self.parent.ignoreList        
        self.populatePlugins()
        self.parent.qtTools.connectToRightClick(self.treeWidget,self.pluginRightClick)
        self.treeWidget.itemDoubleClicked.connect(self.pluginSelected)        

    def pluginSelected(self, *eve):
        self.parent.mouseLock()
        selectedItem = eve[0]
        itemInfo = self.parent.qtTree.getItemLabel(selectedItem)
        name = itemInfo['Label']
        path = itemInfo['Data']
        if(os.path.isfile(path)):
            print("\nExecuting: " + path)
            content = self.parent.ttls.fileContent(path)
            self.parent.runScript(content)
        self.parent.mouseRelease()
                
    def pluginRightClick(self, point):
        #menu = ['m1','m2',['m3','m31',['m32','m321','m322'],'m33'],'m4','m5',['m6','m61','m62'],'m7']
        #self.qtTools.popUpMenuAdv(menu,self.treeWidget,point,self.pluginRightClickSelected,'addedArgument')
        item = self.treeWidget.itemAt(point)
        
        if(item):
            name = item.text(0)
            path = item.data(0,QtCore.Qt.UserRole)
            if (os.path.exists(path)):
                if (os.path.isfile(path)):
                    uiFile = item.data(0,QtCore.Qt.UserRole).replace('.py','.ui')            
                    if (os.path.exists(uiFile)):
                        self.parent.qtTools.popUpMenu(self.treeWidget,point,["Edit","Edit UI","Delete"],self.pluginRightClickSelected,["myarg1","myarg2"])
                    else:
                        self.parent.qtTools.popUpMenu(self.treeWidget,point,["Edit","Delete"],self.pluginRightClickSelected,["myarg1","myarg2"])
                else:
                    self.parent.qtTools.popUpMenu(self.treeWidget,point,["New Simple Plug","New UI Plug","New Folder","Refresh"],self.pluginRightClickSelected,["myarg1","myarg2"])
            else:
                self.parent.qtTools.popUpMenu(self.treeWidget,point,["New Simple Plug","New UI Plug","New Folder","Refresh"],self.pluginRightClickSelected,["myarg1","myarg2"])
        else:
            self.parent.qtTools.popUpMenu(self.treeWidget,point,["New Simple Plug","New UI Plug","New Folder","Refresh"],self.pluginRightClickSelected,["myarg1","myarg2"])
            
    def pluginRightClickSelected(self,*arg):
        act = self.parent.sender()
        menuOption = act.text()
        item = self.treeWidget.itemAt(act.data())
        itemSelected = item.text(0) if item else None
        path = item.data(0,QtCore.Qt.UserRole) if item else self.parent.scriptsPath
        if(menuOption=="Refresh"):
            self.populatePlugins()
        if(menuOption=="New Folder"):
            nFolderName = self.parent.qtTools.showInputBox("ScriptFolderName","Enter the new folder name", "folderName")
            if (nFolderName):
                newPath = os.path.join(path,nFolderName)
                os.makedirs(newPath, exist_ok=True)
                self.populatePlugins()
        if(menuOption=="New Simple Plug"):          
            nFileName = self.parent.qtTools.showInputBox("PlugName","Enter the new Plug name", "newPlug")   
            if (nFileName):            
                data = self.parent.ttls.fileContent('templatePlug.py')
                data = data.replace('myClass', nFileName)
                f = os.path.join(path, nFileName+".py")
                self.parent.ttls.writeFileContent(f, data)
                self.populatePlugins()
                self.parent.loadFile(f)
        if(menuOption=="New UI Plug"):
            nFileName = self.parent.qtTools.showInputBox("PlugName","Enter the new UI Plug name", "newUIPlug")
            if (nFileName):
                pyf = os.path.join(path, nFileName+".py")
                uif = os.path.join(path, nFileName+".ui")                
                data = self.parent.ttls.fileContent('templateUIPlug.py')
                data = data.replace('UI_myUIPlug.ui', uif)                
                data = data.replace('myUIPlug', nFileName)                
                self.parent.ttls.writeFileContent(pyf, data)
                self.populatePlugins()
                self.parent.loadFile(pyf)                
                data = self.parent.ttls.fileContent('templateUIPlug.ui')
                self.parent.ttls.writeFileContent(uif, data)
                print("Created..." + pyf)
                print("Created..." + uif)
        if(menuOption=="Edit"):
            pyFile = (item.data(0,QtCore.Qt.UserRole))
            self.parent.loadFile(pyFile)
        if(menuOption=="Edit UI"):
            uiFile = item.data(0,QtCore.Qt.UserRole).replace('.py','.ui')
            args = '"' + self.parent.pyDesigner + '"' + " " + '"' + uiFile + '"'
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
                self.populatePlugins() 
            except OSError:
                pass    

    def isToBeIgnored(self, path):
        for eachIgnoreItem in self.ignoreList:
            if eachIgnoreItem in path:
                if (self.pluginsVerbose):
                    print("Ignoring.... " + path)
                return True
        return False
    
    def populatePlugins(self):
        self.treeWidget.clear()        
        print("Loading Plugins... ")
        spath = os.getcwd()
        self.parent.addToSysPath(spath)                
        for eachItem in os.listdir(self.parent.scriptsPath):
            currentDirName = eachItem
            currentDirPath = os.path.join(self.parent.scriptsPath,currentDirName)            
            if (not "__" in currentDirPath):
                if os.path.isdir(currentDirPath):
                    if not self.isToBeIgnored(currentDirPath):                  
                        rItem = self.parent.qtTree.createItem(currentDirName, currentDirPath)
                        self.parent.qtTree.addNewRoot(self.treeWidget, rItem)
                        self.populatePluginsCore(rItem, currentDirPath)
                else:
                    self.createPluginItem(currentDirPath)        
        print("Plugins Loaded!")
                                                
    def populatePluginsCore(self, parentItem, searchPath):                      
        self.parent.addToSysPath(searchPath)        
        for eachItem in os.listdir(searchPath):
            currentDirName = eachItem
            currentDirPath = os.path.join(searchPath,currentDirName)    
            if (not "__" in currentDirPath):
                if os.path.isdir(currentDirPath):
                    if self.isToBeIgnored(currentDirPath): return None
                    rItem = self.parent.qtTree.createItem(currentDirName,currentDirPath)
                    self.parent.qtTree.addChild(rItem, parentItem)
                    self.populatePluginsCore(rItem, currentDirPath)
                else:
                    self.createPluginItem(currentDirPath, parentItem)   

    def createPluginItem(self, plugFile, parentTreeItem=None):
        if self.isToBeIgnored(plugFile): return None    
        modName = os.path.basename(plugFile).replace(os.path.splitext(plugFile)[1], '')
        content = self.parent.ttls.fileContent(plugFile)
        expecting = "For DevConsole" 
        if(expecting in content):
            item = self.parent.qtTree.createItem(modName, plugFile)
            if(parentTreeItem is None):
                plugTreeItem = self.parent.qtTree.addNewRoot(self.treeWidget, item)
            else:
                plugTreeItem = self.parent.qtTree.addChild(item, parentTreeItem)
            if (self.pluginsVerbose):
                print("Adding Plug... " + plugFile)
        else:
            if (self.pluginsVerbose):
                print("Skipped Plug! (Add tag 'For DevConsole') " + plugFile)
            plugTreeItem = None
        #self.runScript(content)
        return plugTreeItem                          