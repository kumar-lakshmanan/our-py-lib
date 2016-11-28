'''
Created on Oct 24, 2015

@author: MUKUND
'''
from PyQt5.QtCore import (QFile, QFileInfo, QPoint, QSettings, QSignalMapper, QSize, QTextStream, Qt, )
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow, QMdiArea, QMessageBox, QTextEdit, QWidget, )
from PyQt5.QtGui import (QIcon, QKeySequence, QFont, QColor)
from PyQt5.Qsci import (QsciScintilla, QsciLexerPython)
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
from PyQt5.uic import loadUi
#from PyQt5.uic.Compiler.qtproxies import QtWidgets

import os
import sys
import crashSupport

class scriptExecute(object):
    '''
    classdocs
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
        print('Script executer...!')
        
    def mouseLock(self):             
        self.grabMouse(QtCore.Qt.WaitCursor)
        self.grabKeyboard()
        QtWidgets.QApplication.processEvents()        

    def mouseRelease(self):
        self.releaseMouse()
        self.releaseKeyboard()
        QtWidgets.QApplication.processEvents()      

    def executeCurrentScript(self):
        self.mouseLock()
        currentWindow = self.activeMdiChild()
        if(currentWindow and not str(currentWindow.text()) == ''):
            inputs = str(currentWindow.text()).rstrip()
            print("\nExecution Start @ " + self.ttls.getDateTime() + "\n")
            self.runScript(inputs)
            print("\nExecution Completed @ " + self.ttls.getDateTime() + "\n")
        self.mouseRelease()
           
    def execStartUp(self, *arg):
        self.addToSysPath(self.scriptsPath)                
        self.userSetup = os.path.join(self.scriptsPath, 'userSetup.py')
        self.userSetup = self.userSetup if os.path.exists(self.userSetup) else os.path.join(self.scriptsPath, 'userSetup.pyc')
        self.userSetup = self.userSetup if os.path.exists(self.userSetup) else ''
        print("Starting Usersetup script... userSetup.py")
        self.runScriptFile(self.userSetup)

    def addToSysPath(self, path):
        path = os.path.abspath(path)
        if('\.' in path): return None
        if(self.pluginsVerbose):
            print ("Adding path to system... " + path)
        code = r'''import sys,os
path2Add="%s"
if path2Add not in sys.path and os.path.exists(path2Add):
    sys.path.append(path2Add)
''' % (path).replace(os.path.sep,'/')
        self.runScript(code)

    def runScript(self, script):
        try:
            command = str(script).replace('\r\n', '\n')
            locals = self.getUpdatedLocals()
            self.inter.locals.update(locals)
            try:
                res = self.inter.runcode(command)
            except SyntaxError:
                self.inter.showsyntaxerror()
            except:
                print(crashSupport.errorReport())
            QtWidgets.QApplication.processEvents()
            if res is not None:
                print ('\n---------------------------------------\n')
                print(repr(res))
                print ('\n---------------------------------------\n')
        except SystemExit:
            self.inter.showsyntaxerror()
            print(crashSupport.errorReport())
        except:
            print(crashSupport.errorReport())

    def getUpdatedLocals(self):
        try:
            raise None
        except:
            frame = sys.exc_info()[2].tb_frame.f_back
        # evaluate commands in current namespace
        namespace = frame.f_globals.copy()
        namespace.update(frame.f_locals)
        namespace['__name__'] = '__main__'
        return namespace                        

    def runScriptFile(self, scriptFile):
        print ('Trying to execute script file... %s' % scriptFile)
        if scriptFile and os.path.exists(scriptFile):
            data = self.ttls.fileContent(scriptFile)
            self.runScript(data)
        else:
            print ('Script file missing...' + scriptFile)            
            