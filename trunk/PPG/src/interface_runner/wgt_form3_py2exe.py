'''
Created on Sep 4, 2014

@author: Mukundan
'''

from user_interface import wgt_form3_py2exe as formCode
from PyQt5 import QtCore, QtGui, QtWidgets
from general import PyQt
import sip
import core.lib


class Form(object):
    '''
    classdocs
    '''
    # parent = PyProjGen.PyProjGen()
    # ppjCopy = core.lib.ppg()
    parent = None
    mainWidget = None
    form = None

    def __init__(self, winHandle, currentObj, ppjCopy):
        '''
        Constructor
        '''

        self.mainWindow = winHandle
        self.ppjCopy = ppjCopy
        self.tools = PyQt.Tools(self.mainWindow)
        self.form = formCode.Ui_Form()
        self.curObj = currentObj
        self.load()

    def populateUI(self):
        # self.tools.setValue(self.form.lineEdit, self.curObj.mainWindowTitle)
        pass

    def getUpdatedUIValues(self):
        # self.curObj.mainWindowTitle = self.tools.getValue(self.form.lineEdit)
        return self.curObj
    
    def load(self):
        # Load objects to core UI
        self.mainWidget = QtWidgets.QWidget(self.mainWindow)
        self.form.setupUi(self.mainWidget)
        self.mainWindow.gridLayout_5.addWidget(self.mainWidget, 0, 0, 1, 1)
        self.populateUI()

        # Condition Checks
        self.mainWidget.setEnabled(self.ppjCopy.general.projectType == 'pyqtwindows')

    def unload(self):
        # Unload objects from core UI
        self.mainWindow.gridLayout_5.removeWidget(self.mainWidget)
        sip.delete(self.mainWidget)

