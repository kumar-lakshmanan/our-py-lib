'''
Created on Oct 15, 2014

@author: Mukundan
'''
import os

from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi

class PluginBase(QDialog):
    '''
    classdocs
    '''

    def __init__(self, parent, uiFile):
        '''
        Constructor
        '''
        super(PluginBase, self).__init__(parent)
        self.who = str(self.__class__.__name__)
        self.parent = parent
        self.parentName = str(self.parent.__class__.__name__)
        self.uiFile = uiFile
        print ("Initializing Plugin... " + self.who + " parent: " + self.parentName)
        self.setupUI(self.uiFile)

    def setupUI(self, uiFile):
        prepath = os.path.abspath(os.curdir)
        prepath = os.path.join(prepath, "devPlugs")
        uiFile = os.path.join(prepath, uiFile)
        loadUi(uiFile, self)
        self.setWindowTitle(self.who)

