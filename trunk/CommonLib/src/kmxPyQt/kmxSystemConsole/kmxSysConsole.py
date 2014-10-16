#-------------------------------------------------------------------------------
# Name:        module1
#
# Author:      lkumaresan
#
# Created:     13/01/2011
# Copyright:   (c) lkumaresan 2011
# Licence:     Personal
#
# Description:
#
#
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import base64
import inspect
import os
import sys
import time

from PyQt5 import QtGui, QtCore, QtWidgets
from kmxPyQt.kmxSystemConsole.console_ui import Ui_MainWindow
#
# # #Remove cached custom modules from memory except preloaded IDE modules
# if __name__ == '__main__':
#     if globals().has_key('InitialModules'):
#          for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
#             del(sys.modules[CustomModule])
#     else:
#         InitialModules = sys.modules.keys()



# Global Lib

# Application Lib

class SysOut():

    def __init__(self, widget):
        sys.stdout = self
        sys.stderr = self
        self.widget = widget
        self.runningApp = QtWidgets.QApplication.instance()
        self.widget.setText('')
        if self.runningApp:self.runningApp.processEvents()

    def write(self, x):
        x = x.strip()
        txt = str(self.widget.toPlainText())
        newTxt = '%s\n%s' % (txt, x) if txt else x
        self.widget.setText(newTxt)
        vsb = self.widget.verticalScrollBar()
        vsb.setValue(vsb.maximum())
        if self.runningApp:self.runningApp.processEvents()


class Console(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        self.btnClose.clicked.connect(self.close)
        self.sysout = SysOut(self.textEdit)
        self.btnClose.setEnabled(1)
        # self.show()
        # self.runningApp = QtWidgets.QApplication.instance()

    def addStatusBarButton(self, StatusBar):
        if StatusBar:
            self.stsBtnDebugger = QtWidgets.QToolButton()
            self.stsBtnDebugger.setText('Console')
            self.stsBtnDebugger.setToolTip('DevConsole')
            self.stsBtnDebugger.setAutoRaise(1)
            self.stsBtnDebugger.setMaximumHeight(18)
            StatusBar.addPermanentWidget(self.stsBtnDebugger, 0)
            self.stsBtnDebugger.clicked.connect(self.show)
        else:
            self.stsBtnDebugger = None

    def runScript(self, script):
        z = ImportModule(script)
        self.runningApp = QtWidgets.QApplication.instance()
        self.btnClose.setEnabled(1)
        return z

    def __del__(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr

def ImportModule(script):

    '''

    Imports and returns you the module.

    userMod = ImportModule('RunMe.py')
    userMod.myclass()

    '''
    imported = 0
    temp = os.getcwd()
    try:
        if script:
            script = str(script).strip()
            if os.path.exists(script):
                ext = os.path.splitext(script)[-1][1:].upper()
                if ext and ext == 'PY':
                    fileName = os.path.basename(script)[:-3]
                    filePath = os.path.dirname(script)
                    filePath = filePath if filePath else os.getcwd()
                    if not '.' in fileName:
                        if filePath and os.path.exists(filePath):
                            temp
                            os.chdir(filePath)
                            __addToSysPath(filePath)
                            userModule = __import__(fileName)
                            if inspect.ismodule(userModule):
                                os.chdir(temp)
                                return userModule
                            else:
                                print ('Not a module')
                        else:
                            print ('Path does not exist!')
                    else:
                        print ('More then one ext!')
                else:
                    print ('Not a PY file!')
            else:
                print ('Script does not exit!')
        else:
            print ('No Script Given!')
    except:
        print('err')
        # print (errorReport())
    os.chdir(temp)
    return None

def __addToSysPath(path):
    if path and os.path.exists(path):
        path = os.path.normpath(path)
        if path not in sys.path:
            sys.path.append(path)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ui = Console()
    app.exec_()
    del(ui)
    del(app)
    sys.exit(0)
