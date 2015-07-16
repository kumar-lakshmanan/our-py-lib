'''
Created on Jul 9, 2015

@author: MUKUND
'''

class Printer(object):
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
    
    def action(self):
        print("\nInput 1: "+str(self.inInput1))
        print("\nInput 2: "+str(self.inInput2))
        print("\nInput 3: "+str(self.inInput3))
        print("\nInput 4: "+str(self.inInput4))