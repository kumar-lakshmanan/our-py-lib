'''
Created on Oct 14, 2014

@author: Mukundan
'''
import os

import devPluginBase


class QuickTools(devPluginBase.PluginBase):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        # Parent is DEV <DEVCONSOLEPLUG>
        self.parent = parent
        self.uiName = "QuickTools.ui"
        super(QuickTools, self).__init__(parent, self.uiName)
        print ("Loaded!")

        # Connections
        self.pushButton_2.clicked.connect(self.myFunc1)
        self.pushButton_4.clicked.connect(self.myFunc2)

    def myFunc1(self, *arg):
        fileToOpen = 'F:/Kumaresan/Code/Python/devPlugGenerator/src/core/devPlugGenerator_bin/devPlugGenerator.exe'
        self.startExec(fileToOpen)

    def myFunc2(self, *arg):
        fileToOpen = 'F:/Kumaresan/Code/Python/PPG/src/core/PyProjGen_bin/PyProjGen.exe'
        self.startExec(fileToOpen)

    def startExec(self, fileToOpen):
        os.system(fileToOpen)
