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
        menuBar.addAction(newMenu.menuAction())
        return newMenu

    def createMenuItem(self, parentWindow, menu, itemName='', fnToCall=None):
        action = QtWidgets.QAction(parentWindow)
        action.setText(itemName)
        menu.addAction(action)
        if fnToCall is not None: action.triggered.connect(fnToCall)
        return action

    def createMenuItemSeperator(self, menu):
        menu.addSeparator()
