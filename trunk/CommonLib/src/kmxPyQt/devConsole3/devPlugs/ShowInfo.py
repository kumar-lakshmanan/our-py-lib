'''
Created on Oct 14, 2014

@author: Mukundan
'''
import devPluginBase

class ShowInfo(devPluginBase.PluginBase):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        self.parent = parent
        self.uiName = "ShowInfo.ui"
        super(ShowInfo, self).__init__(parent, self.uiName)
        print ("Loaded!")

    def myFunc(self, *arg):
        self.parent.showAttrs(eval(self.lineEdit.text()))