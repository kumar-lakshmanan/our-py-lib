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
        self.Module = ''
        self.variables=[]
        
        #newNode = (nodeName,name,node,inPort,outPort)
    def setVariables(self, variableLst):
        self.variables = variableLst

    def getVariables(self):
        return self.variables
                
    def getPos(self):
        self.Node.pos()
    
    def setPos(self,x,y):
        self.Node.setPos(x,y)      