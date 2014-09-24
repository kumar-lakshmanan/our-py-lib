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
        # self.curObj = core.lib.Py2Exe()
        self.load()

    def populateUI(self):

        self.form.groupBox.setChecked(not self.curObj.isEnabled)
        self.form.groupBox.setChecked(self.curObj.isEnabled)

        self.tools.setValue(self.form.lineEdit, self.curObj.appName)
        self.tools.setValue(self.form.lineEdit_2, self.curObj.description)
        self.tools.setValue(self.form.lineEdit_3, self.curObj.company_name)
        self.tools.setValue(self.form.lineEdit_4, self.curObj.copyrights)
        self.tools.setValue(self.form.lineEdit_5, self.curObj.version)

        pass

    def getUpdatedUIValues(self):
        # self.curObj.mainWindowTitle = self.tools.getValue(self.form.lineEdit)

        self.curObj.appName = self.tools.getValue(self.form.lineEdit)
        self.curObj.description = self.tools.getValue(self.form.lineEdit_2)
        self.curObj.company_name = self.tools.getValue(self.form.lineEdit_3)
        self.curObj.copyrights = self.tools.getValue(self.form.lineEdit_4)
        self.curObj.version = self.tools.getValue(self.form.lineEdit_5)

        self.curObj.isEnabled = self.form.groupBox.isChecked()

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

