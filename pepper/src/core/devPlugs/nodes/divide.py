'''
Created on Jul 9, 2015
#For DevConsole
@author: MUKUND
'''

class Divide(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.inInput1=1
        self.inInput2=2
        self.inInput3=3
        self.inInput4=4
        
        self.outOutput1=1
        self.outOutput2=2
    
    def action(self):
        self.outOutput1 = self.inInput1 / self.inInput2
        self.outOutput2 = self.inInput3 / self.inInput4
        