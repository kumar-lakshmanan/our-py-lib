'''
Created on Oct 14, 2014

@author: Mukundan
'''
import devPluginBase

class PlugMe1(devPluginBase.PluginBase):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        super(PlugMe1, self).__init__(parent, "plug_screen.ui")
        print ("Loaded!")

