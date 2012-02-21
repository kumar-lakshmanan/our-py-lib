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

class oplQtWins():

    """
        Following functions are ment for handling Qt Windows
    """

    def __init__(self, uiMain):
        self.uiMain = uiMain


    def createDock(self, widget=None):
        if widget:
            self.win = QtGui.QDockWidget(self.uiMain)
            uName = str(widget).replace(' ','').replace('<','').replace('>','').replace('.','')
            uName = uName.split('at')[0]
            self.win.setObjectName(uName)
            base = QtGui.QWidget()
            widget.setupUi(base)
            widget.win = self.win
            self.win.setWidget(base)
            self.uiMain.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.win)
            return self.win
