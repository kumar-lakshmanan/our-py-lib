#-------------------------------------------------------------------------------
# Name:        QtTable
# Purpose:
#
# Author:      AIAA
#
# Created:     10-11-2011
# Copyright:   (c) AIAA 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
import sip

class oplQtList():

    """
        Following functions are ment for handling Qt List Component.
    """

    def __init__(self,uiMain):
        self.uiMain = uiMain
        self.widget = QtGui.QListWidget() #Dummy Object to get properties of
                                            # list component.

    def getAllItem(self, widget):
        self.widget = widget
        items = []
        for c in xrange(0, self.widget.count()):
            items.append(self.widget.item(c))
        return items

    def populate(self, widget, datas=[], append=False, checkable=False):
        self.widget = widget
        if not append: self.widget.clear()
        ret = []
        for each in datas:
            if type(each)==type(()) or type(each)==type([]):
                item = self.addItem(self.widget, str(each[0]),str(each[1]),checkable)
            else:
                item = self.addItem(self.widget, str(each),'',checkable)
            ret.append(item)
        return ret

    def addItem(self, widget, text, data='', checkable=False, checkstate=QtCore.Qt.Unchecked):
        self.widget = widget
        item = QtGui.QListWidgetItem()
        item.setText(text)
        item.setData(32,QtCore.QVariant(data))
        if checkable: item.setCheckState(checkstate)
        widget.addItem(item)
        return item
