'''
Created on Jun 26, 2015 Fri - 22:58:49

@author: LKumaresan
'''
import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

from interface_runner.win_main import WinMain
from kmxGeneral import kmxINIConfigReadWrite
from kmxGeneral import kmxTools
from kmxPyQt import kmxQtCommonTools
from kmxPyQt import kmxQtTreeWidget
from kmxPyQt import kmxQtConnections
import inspect

from kmxPyQt.devConsole3 import DevConsolePlug
from kmxPyQt.kmxNodeGraph import kmxNodeGraphSystem as kgs
from kmxPyQt.kmxNodeGraph import kmxNodeGraphReader as kgr

import core.icons
import pkgutil
from core.devPlugs import nodes

from core import dynamicModules
import win32com
import win32com.client

class pepper(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.win = WinMain(self)
        self.win.show()

        self.cfg = kmxINIConfigReadWrite.INIConfig("config.ini")
        self.iconPath = self.cfg.getOption('UserInterface', 'IconPath')
        self.icons = core.icons.iconSetup()

        self.tls = kmxTools.Tools(kmxTools.infoStyle())        
        self.qtConsole = DevConsolePlug.DevConsole(self.win, ShowPrint=True, ShowError=True, StatusBar=self.win.statusBar(), AsDock=True, InitalizeScripts=True)        
        self.qtTrees = kmxQtTreeWidget.TreeWidget()
        self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)
        self.qtConn = kmxQtConnections.QtConnections(self.win)
        self.setupUI()
        self.qtTools.uiLayoutRestore('layout.lyt',[self.win.splitter_2])
        self.tell("Ready!")
        self.currentNode = None
        self.selectedInputVariable = None
                        
    def meClose(self,arg):
        self.qtTools.uiLayoutSave('layout.lyt',[self.win.splitter_2])
        
    def setupUI(self):
        #self.qtConn.connectToClick(self.win.bt, FunctionToInvoke)
        self.win.actionLoad_Scene.triggered['bool'].connect(self.loadScene)
        self.win.actionSave_Scene.triggered['bool'].connect(self.saveScene)
        self.win.actionNew_Scene.triggered.connect(self.newScene)
        self.qtConn.connectToClick(self.win.trInput, self.trInputClicked)
        self.qtConn.connectToClick(self.win.pushButton, self.parseModules)
        self.qtConn.connectToDblClick(self.win.trOutput, self.trOutputsDblClicked)
        self.qtConn.connectToClick(self.win.btnApplyInputs, self.applyInputs)
        #self.qtConn.connectToKeyPress(self.win.txtInputOutput, self.applyInputs)
        self.win.actionExecute.triggered['bool'].connect(self.doExecute)
        self.qtConn.connectToClose(self.win,self.meClose)
        self.qtConn.connectToDragDrop(self.win.graphicsView, self.dragDropNode)
        self.qtTools.setIconForItem(self.win, self.icons.windowIcon, isWindow=1)
        self.parseModules()
        
        self.kgs=kgs.KMXNodeGraphSystem(self.win, self.win.graphicsView, self.win.scene)
        self.kgs.readyTheScene()
        self.kgs.connectFnNodeSelected(self.nodeSelected)        
        self.kgs.connectFnNodeDeSelected(self.nodeDeSelected)        

    def applyInputs(self, *arg):
        if (self.currentNode and self.selectedInputVariable):
            vars = self.currentNode.getVariables()
            newValue = self.win.txtInputOutput.toPlainText()
            newSet = (self.selectedInputVariable, newValue)
            for each in vars:
                variable = each[0]
                value = each[1]
                if(variable==self.selectedInputVariable):
                    newSet = (variable, newValue)
                    vars.remove(each)
            vars.append(newSet) 
            self.currentNode.setVariables(vars) 
            self.tell("Variables Updated!")
                          
       
    def trInputClicked(self, itm):
        self.win.txtInputOutput.setHtml("")
        item = self.win.trInput.itemFromIndex(itm)
        nodeInput = item.text(0)
        self.selectedInputVariable = nodeInput
        
        vars = self.currentNode.getVariables()
#         print("--"+str(self.currentNode))
#         print("--"+str(self.currentNode.getVariables()))
        for each in vars:
            if len(each)==2:
                variable = each[0]
                value = each[1]
                if(variable==self.selectedInputVariable):
                    self.win.txtInputOutput.setText(value)            
        
    def trOutputsDblClicked(self, itm):
        item = self.win.trOutput.itemFromIndex(itm)
        parent = item.parent()
        
        info = parent.text(0) + "." + item.text(0) + "\n"
        self.win.txtInputOutput.insertPlainText(str(info).strip())
        
        #for each in self.currentNode.kmxNodeBlock.inputs:
        #self.currentNode.kmxNodeBlock.inputs.append(info)
        #self.currentNode.setVariables(info)
            
        
    def nodeDeSelected(self):
        self.currentNode = None
        self.selectedInputVariable = ''
        self.win.txtInputOutput.setText('')
        info=''
        self.win.txtDescription.setHtml(info)
        self.sceneReader()
        
    def nodeSelected(self, nd):   
        self.win.txtInputOutput.setText('')
        node = nd.kmxNodeBlock
        tag = node.nodeTag
        name = node.Name
        module = node.Module
        input = node.inPort
        output = node.outPort
        self.currentNode = nd
        self.selectedInputVariable = ''
                        
        data = self.kgs.sceneData()
        self.kgr = kgr.kmxNodeGraphReader(data,self)
                
        d = dynamicModules.DynamicModules(nodes)
        inlst = d.getInVariables(name, module)
        outlst = d.getOutVariables(name, module)
        instanceName = self.kgr.getInstanceName(tag)
        info = "\nTag: " + tag
        info += "<br>Class: " + name
        info += "<br>InstanceName: " + instanceName
        info += "<hr><b>Inputs:</b>"
        for each in inlst:
            info += "<br>" + each 
        info += "<hr><b>Outputs:</b>"
        for each in outlst:
            info += "<br>" + each                     
        info += "<hr>"
        self.win.txtDescription.setHtml(info)
        #self.tell(str(info) + " Selected!")
        #print(tag)
        #print(inlst)
        self.loadInputOutput(tag,inlst)

    def loadInputOutput(self, nodeTag, inlst):
        self.win.trInput.clear()
        self.win.trOutput.clear()
        self.win.trInput.setHeaderHidden(False)
        self.win.trOutput.setHeaderHidden(False)
        
        for each in inlst:
            root = self.qtTrees.createItem(each)
            self.qtTrees.addNewRoot(self.win.trInput, root)
        
        data = self.kgs.sceneData()
        self.kgr = kgr.kmxNodeGraphReader(data, self)
        lst = self.kgr.getParents(nodeTag)
        for each in lst:
            instanceName = self.kgr.getInstanceName(each)
            root = self.qtTrees.createItem(instanceName)
            self.qtTrees.addNewRoot(self.win.trOutput, root)

            node = self.kgs.getNodeByTag(each)
            name = node.Name
            module = node.Module            
            d = dynamicModules.DynamicModules(nodes)            
            inlst = d.getInVariables(name, module)
            outlst = d.getOutVariables(name, module)   
            
            for eachOut in outlst:
                citem = self.qtTrees.createItem(eachOut)
                self.qtTrees.addChild(citem, root)
                       
        self.win.trOutput.expandAll()
        
    def parseModules(self):
        self.parseModulesCore(nodes)

               
    def parseModulesCore(self, package):
        self.win.trNodes.clear()
        d = dynamicModules.DynamicModules(package)
        d.reParseModules()
        
        for eachClass in d.classes:
            self.win.item = QtWidgets.QTreeWidgetItem()
            self.win.item.setText(0, eachClass[0])
            setattr(self.win.item, 'dx', eachClass[1])
            self.win.trNodes.addTopLevelItem(self.win.item)        
                 
    
    def dragDropNode(self, eve):
        sourceWidget = eve.source()
        sourceItems = sourceWidget.selectedItems()[0]
        cls = sourceItems.text(0)
        mod = getattr(sourceItems, 'dx')
        p=self.win.graphicsView.mapToScene(eve.pos())        
        self.addFnBlock(cls,mod, p.x(), p.y())

    def addFnBlock(self, cls, mod, xpos=10, ypos=10):
        kmxNode = self.kgs.addNodeFn(cls, mod)
        kmxNode.Node.setPos(xpos,ypos)
        self.tell(cls + " added from " + mod)

    def tell(self, info):
        print(info)
#         matter = self.win.textBrowser.toPlainText()
#         matter = matter + info + "\n"
#         self.win.textBrowser.setText(matter)
#         
#         vsb = self.win.textBrowser.verticalScrollBar()
#         vsb.setValue(vsb.maximum())        
    
    def doExecute(self):
        data = self.kgs.sceneData()
        self.kgr = kgr.kmxNodeGraphReader(data, self)        
        code = self.kgr.genereteCode()
        k=self.qtConsole.runScript(code)
        print (k)
       
    def loadScene(self):
        f = self.qtTools.getFile('Load file', '', '*.scene')
        if(f): self.kgs.loadScene(f)    
            
    def saveScene(self):
        f = self.qtTools.getFileToSave('Save file', '', '*.scene')
        if(f): self.kgs.saveScene(f+".scene" if (not f.endswith('.scene')) else f)
            
    def newScene(self):
        self.kgs.readyTheScene()
        
    def sceneReader(self):
        data = self.kgs.sceneData()
        self.kgr = kgr.kmxNodeGraphReader(data, self)
        code = "Code<hr>"
        code += "<br>"+self.kgr.genereteCode().replace("\n", "<br>")
        code += "<hr>"
        self.win.txtDescription.setHtml(code)
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = pepper()
    sys.exit(app.exec_())
