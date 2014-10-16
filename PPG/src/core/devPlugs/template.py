'''
Created on Oct 14, 2014

@author: Mukundan
'''
import devPluginBase

class template(devPluginBase.PluginBase):
    '''
    classdocs
    '''

    def __init__(self, parent):
        '''
        Constructor
        '''
        # Parent is DEV <DEVCONSOLEPLUG>
        self.parent = parent
        self.uiName = "template.ui"
        super(template, self).__init__(parent, self.uiName)
        print ("Loaded!")

        # Connections
        self.pushButton_2.clicked.connect(self.myFunc1)
        self.pushButton_3.clicked.connect(self.myFunc2)

    def myFunc1(self, *arg):
        print(self.lineEdit.text())

    def myFunc2(self, *arg):
        print(self.lineEdit_2.text())

# src = 'C:/Users/Mukundan/Desktop/Test/Set1/'
# dst = 'C:/Users/Mukundan/Desktop/Test/Set2/'
# dev.ttls.copyFolder(src,dst)
