'''
Created on Jul 4, 2015

@author: MUKUND
'''

from kmxPyQt.qne.qneport import QNEPort

class kmxNodeBlock(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.nodeTag = ''
        self.Name = ''
        self.Node = None
        self.inPort = None
        self.outPort = None
        self.additionalTags = ''
        
        #newNode = (nodeName,name,node,inPort,outPort)
    def getPos(self):
        self.Node.pos()
    
    def setPos(self,x,y):
        self.Node.setPos(x,y)      