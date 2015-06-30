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
from kmxPyQt.qne.qnodeseditor import QNodesEditor
from kmxPyQt.qne.qnesysblock import QNESysBlock
from kmxPyQt.qne.qneblock import QNEBlock
from kmxPyQt.qne.qneport import QNEPort
import inspect

from kmxPyQt.devConsole3 import DevConsolePlug
import core.icons
from core.Scripts import nodes

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
        self.qtConsole = DevConsolePlug.DevConsole(self.win, ShowPrint=False, ShowError=False, StatusBar=self.win.statusBar(), AsDock=True, InitalizeScripts=True)        
        self.qtTrees = kmxQtTreeWidget.TreeWidget()
        self.qtTools = kmxQtCommonTools.CommonTools(self.win, self.iconPath)
        self.qtConn = kmxQtConnections.QtConnections(self.win)
        self.setupUI()
        self.qtTools.uiLayoutRestore('layout.lyt',[self.win.splitter])
        self.tell("Ready!")
                        
    def meClose(self,arg):
        self.qtTools.uiLayoutSave('layout.lyt',[self.win.splitter])
        
    def setupUI(self):
        self.qtConn.connectToClose(self.win,self.meClose)
        self.qtConn.connectToDragDrop(self.win.graphicsView, self.dragDropNode)
        self.qtTools.setIconForItem(self.win, self.icons.windowIcon, isWindow=1)
        self.parseModules()
        
        #Start Node
        self.s=QNESysBlock(None)
        self.win.scene.addItem(self.s)
        self.s.addPort('Start', 0, QNEPort.NamePort)        
        self.s.addOutputPort('');
        #self.s.setPos(self.win.graphicsView.width()/2-100,self.win.graphicsView.height()/2)

        #End Node
        self.e=QNESysBlock(None)
        self.win.scene.addItem(self.e)
        self.e.addPort('End', 0, QNEPort.NamePort)        
        self.e.addInputPort('');
        self.e.setPos(160,0)  
       
    def parseModules(self):
        members = inspect.getmembers(nodes)
        self.win.trNodes.clear()
        for eachMember in members:
            obj = eachMember[1]
            mem = eachMember[0]
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                self.win.item = QtWidgets.QTreeWidgetItem()
                self.win.item.setText(0, mem)
                setattr(self.win.item, 'dx', eachMember[1])
                self.win.trNodes.addTopLevelItem(self.win.item)

    def getArguments(self, fnName):
        return inspect.getargspec(fnName)[0]
    
    def dragDropNode(self, eve):
        sourceWidget = eve.source()
        sourceItems = sourceWidget.selectedItems()[0]    
        obj = getattr(sourceItems, 'dx')
        p=self.win.graphicsView.sceneRect().center().toPoint()
        self.addFnBlock(obj, p.x(), p.y())

    def addFnBlock(self, fn, xpos=10, ypos=10):
        args=self.getArguments(fn)
        block = QNEBlock(None)
        self.win.scene.addItem(block)
        block.addPort(fn.__name__, 0, QNEPort.NamePort)
        block.addInputPort("")
        for eachArg in args:
            block.addInputPort(eachArg)
        block.addOutputPort("return");
        block.setPos(xpos,ypos)
        self.tell(fn.__name__ + "Added!")                                        

    def tell(self, info):
        matter = self.win.textBrowser.toPlainText()
        matter = matter + info + "\n"
        self.win.textBrowser.setText(matter)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = pepper()
    sys.exit(app.exec_())
