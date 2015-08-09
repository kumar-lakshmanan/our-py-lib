'''
#For DevConsole

Created on Jul 9, 2015

@author: MUKUND
'''

class Whomtogo(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.inAUD=1
        self.inRaffles=46.25
        self.inMoney2India=46.06
        self.inInput4=4
        
        self.outRaffles=1
        self.outMoneyToIndia=2
    
    def action(self):
        print("helo")
        self.outRaffles = (self.inAUD * self.inRaffles)  - (6 * self.inRaffles)
        self.outMoneyToIndia = (self.inAUD * self.inMoney2India) - 45
        