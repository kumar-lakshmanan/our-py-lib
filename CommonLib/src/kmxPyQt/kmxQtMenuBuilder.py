import os

from PyQt5 import QtCore, QtGui, QtWidgets


class MenuBuilder(object):

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def createMenuBar(self, parentWindow):
        menubar = QtWidgets.QMenuBar(parentWindow)
        parentWindow.setMenuBar(menubar)
        return menubar

    def createMenu(self, menuBar, menuName=''):
        newMenu = QtWidgets.QMenu(menuBar)
        newMenu.setTitle(menuName)        
        if menuBar: menuBar.addAction(newMenu.menuAction())
        return newMenu

    def createMenuItem(self, parentWindow, menu, itemName='', fnToCall=None):
        action = QtWidgets.QAction(parentWindow)
        action.setText(itemName)
        menu.addAction(action)
        if fnToCall is not None: action.triggered.connect(fnToCall)
        return action

    def createMenuItemSeperator(self, menu):
        menu.addSeparator()

    def createMenuForList(self, parentWindow, menuName, lstOfItems=[], fnToCall=None):
        if (len(lstOfItems)>0):     
            menu = self.createMenu(None, menuName)       
            for eachItem in lstOfItems:
                if(eachItem == '|'):
                    menu.addSeparator()
                else:
                    self.createMenuItem(parentWindow, menu, eachItem, fnToCall)
            return menu

    def updateMenu(self, parentWindow, menu, itemName, fnToCall=None):
        if(itemName == '|'): 
            menu.addSeparator()
        else:
            self.createMenuItem(parentWindow, menu, itemName, fnToCall)                    
                    
                    
            