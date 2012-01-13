#-------------------------------------------------------------------------------
# Name:        module1
#
# Author:      lkumaresan
#
# Created:     13/01/2011
# Copyright:   (c) lkumaresan 2011
# Licence:     Prana Studios India (pvt) ltd
#
# Description:
#
#
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import os
import sys

##Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()



#Global Lib
import time
import base64
import inspect

#Application Lib
from PyQt4 import QtGui, QtCore,  Qsci
from console_ui import Ui_Form

class SysOut():

    def __init__(self, widget):
        sys.stdout=self
        sys.stderr=self
        self.widget = widget
        self.runningApp = QtGui.QApplication.instance()
        self.widget.setText('')
        if self.runningApp:self.runningApp.processEvents()

    def write(self, newTxt):
        newTxt = newTxt.strip().replace('\r','')
        oldTxt = str(self.widget.text())
        if not oldTxt.endswith('\n'): oldTxt+='\n'
        cText = oldTxt+newTxt
        self.widget.setText(cText)
        vsb = self.widget.verticalScrollBar()
        vsb.setValue(vsb.maximum())
        if self.runningApp:self.runningApp.processEvents()

class Console(QtGui.QWidget, Ui_Form):

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.stdout=sys.stdout
        self.stderr=sys.stderr
        self.connect(self.btnClose,QtCore.SIGNAL('clicked()'), self.close)
        self.connect(self.btnCopy,QtCore.SIGNAL('clicked()'), self._copy)
        self.sysout = SysOut(self.sci)

        self.PLX = Qsci.QsciLexerPython(self)
        self.ABS = Qsci.QsciAPIs(self.PLX)
        self.PLX.setAPIs(self.ABS)

        self.sci.setAutoCompletionSource(Qsci.QsciScintilla.AcsAll)
        self.sci.setLexer(self.PLX)
        self.sci.setAutoCompletionThreshold(1)
        self.sci.setAutoIndent(True)
        self.sci.setAutoCompletionFillupsEnabled(True)
        self.sci.setBraceMatching(Qsci.QsciScintilla.StrictBraceMatch)
        self.sci.setMarginWidth(1,0)
        self.sci.setReadOnly(1)
        print '*** Python %s on %s.***' % (sys.version,sys.platform)

        self.btnCopy.setEnabled(0)

    def _copy(self):
        pass

    def getData(self):
        return str(self.sci.text())
##    def __del__(self):
##        sys.stdout=self.stdout
##        sys.stderr=self.stderr


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ui = Console()
    app.exec_()
    del(ui)
    del(app)
    sys.exit(0)