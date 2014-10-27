'''
Created on Oct 14, 2014

@author: Mukundan
'''
import devPluginBase

class CopyDevPlugs(devPluginBase.PluginBase):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        # Parent is DEV <DEVCONSOLEPLUG>
        self.parent = parent
        self.uiName = "copyCodesToProjs.ui"
        super(CopyDevPlugs, self).__init__(parent, self.uiName)
        print ("Loaded!")

        # Connections
        self.pushButton_2.clicked.connect(self.myFunc1)
        self.pushButton_3.clicked.connect(self.myFunc2)

    def myFunc1(self, *arg):
        self.copyFolders(self.lineEdit.text())

    def myFunc2(self, *arg):
        self.copyFolders(self.lineEdit_2.text())

    def copyFolders(self, dst):
        src = "F:/Kumaresan/Code/Python/CommonLib/src/kmxPyQt/devConsole3/devPlugs/"
        self.parent.ttls.copyFolder(src, dst, 0, 1, 1)

