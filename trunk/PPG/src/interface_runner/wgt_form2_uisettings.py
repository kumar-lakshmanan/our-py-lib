'''
Created on Sep 4, 2014

@author: Mukundan
'''

from PyQt5 import QtCore, QtGui, QtWidgets
import sip

from kmxPyQt import kmxQtCommonTools
from user_interface import wgt_form2_uisettings as formCode
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
        self.tools = kmxQtCommonTools.CommonTools(self.mainWindow)
        self.form = formCode.Ui_form()
        self.curObj = currentObj
        self.load()

    def populateUI(self):
        self.tools.setValue(self.form.lineEdit, self.curObj.mainWindowTitle)
        self.tools.setValue(self.form.lineEdit_5, self.curObj.windowIcon)
        self.mainWidget.setEnabled(self.ppjCopy.general.projectType == 'pyqtwindows')

    def getUpdatedUIValues(self):
        self.curObj.mainWindowTitle = self.tools.getValue(self.form.lineEdit)
        self.curObj.windowIcon = self.tools.getValue(self.form.lineEdit_5)
        return self.curObj

    def load(self):
        # Load objects to core UI
        self.mainWidget = QtWidgets.QWidget(self.mainWindow)
        self.form.setupUi(self.mainWidget)
        self.mainWindow.gridLayout_5.addWidget(self.mainWidget, 0, 0, 1, 1)
        self.populateUI()

    def unload(self):
        # Unload objects from core UI
        self.mainWindow.gridLayout_5.removeWidget(self.mainWidget)
        sip.delete(self.mainWidget)

