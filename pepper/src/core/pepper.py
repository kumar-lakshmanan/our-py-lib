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
        self.setupUI()

    def setupUI(self):
        self.win.trNodes.setDragEnabled(True)
        
        self.win.trNodes.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.qtTools.setIconForItem(self.win, self.icons.windowIcon, isWindow=1)
        self.parseModules()
        self.qtTools.dragDrop(self.win.trNodes, self.dragDropNode)
        self.qtTools.dragDrop(self.win.graphicsView, self.dragDropNode)
       
    def btnClickHere(self):
        input = self.qtTools.getValue(self.win.lineEdit)
        self.qtTools.setValue(self.win.label_3, "Your input is... " + input)

    def parseModules(self):
        members = inspect.getmembers(nodes)
        self.win.trNodes.clear()
        for eachMember in members:
            obj = eachMember[1]
            mem = eachMember[0]
            if inspect.isfunction(obj) or inspect.ismethod(obj):
                self.win.item = QtWidgets.QTreeWidgetItem()
                self.win.item.setText(0, mem)
                #self.win.item.setText(1, tp)
                setattr(self.win.item, 'dx', eachMember[1])
                self.win.trNodes.addTopLevelItem(self.win.item)

    def dragDropNode(self, *arg):
        print("Hie")
                        

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = pepper()
    sys.exit(app.exec_())
