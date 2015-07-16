# import pickle
# with open('filea', 'rb') as handle:
#         data=pickle.load(handle)
# 
import pprint   
#from scipy.cluster.hierarchy import dendrogram
#from html.parser import starttagopen
# pprint.pprint(data)

class kmxNodeGraphReader():
    
    def __init__(self, data, parent):
        self.parent = parent
        self.data = data
        self.restAll()
        
    def restAll(self):
        self.blocks = self.data['blocks']
        self.conn = self.data['conn']
        self.tagCounter = self.data['counter']
        self.processedConns=[]
        self.processedBlocks=[]
        self.stack = []
        self.code = ''
        self.startTag = self._getTagNameForFn('Start')
        self.endTag = self._getTagNameForFn('End')
        self.executionOrder = []
        self._parents = []

    def _getTarget(self, sourceNodeTag):
        for eachConn in self.conn:
            if (sourceNodeTag == eachConn[0]):
                return eachConn[1]
                            
    def  _getFunctionName(self, nodeTag):
        for eachBlock in self.blocks:
            if (nodeTag == eachBlock[0]):
                return eachBlock[1]

    def _getTagNameForFn(self, fn):
        for eachBlock in self.blocks:
            if (fn == eachBlock[1]):
                return eachBlock[0]
                    
    def _stackAllTargets(self, nodeTag):
        for eachConn in self.conn:
            if not eachConn in self.processedConns:          
                src = eachConn[0]
                dst = eachConn[1]
                if nodeTag==src:
                    self.processedConns.append(eachConn)
                    if (not dst in self.stack) and (not dst in self.processedBlocks) and (not dst == self.endTag):
                        self.stack.insert(0,dst)

    def _getDependent(self, nodeTag):
        lst = []
        for eachConn in self.conn:
            src = eachConn[0]
            dst = eachConn[1]
            if nodeTag == dst and not src == self.startTag:
                lst.append(src)
        return lst
                                    
    def _addToCode(self, nodeTag):
        if (not nodeTag == self.endTag or not nodeTag == self.startTag) and not nodeTag in self.processedBlocks:
            dependents = self._getDependent(nodeTag)
            for eachDependent in dependents:
                if not eachDependent in self.processedBlocks:
                    self._addToCode(eachDependent)
            self._stackAllTargets(nodeTag)                    
            self.processedBlocks.append(nodeTag)

    def doExecutionOrder(self):
        self.restAll()
        self._stackAllTargets(self.startTag)
        while len(self.stack)>0:
            nextTag = self.stack.pop()
            self._addToCode(nextTag)
                        
    def genereteCode(self):
        self.doExecutionOrder()
        codeStep=[]        
        headers = []
        
        for each in self.processedBlocks:
            codeStep.append(self.getInstanceCreateCode(each))
            
            instanceName = self.getInstanceName(each)
            nd = self.parent.kgs.getNodeByTag(each)
            className = self._getFunctionName(each)
            moduleName = nd.Module
            hd = self._getHeader(className,moduleName)
            if (not hd in headers):
                headers.append(hd)
           
#Add core.devPlugs.nodes.add
#Printer core.devPlugs.nodes.printer            
            lst = nd.Node.getVariables()
            for each in lst:
                var=each[0]
                val=each[1]
                codeStep.append(instanceName + '.' + var + " = " + val)
            codeStep.append(instanceName + '.action()')
            
        code = ''
        for each in headers:
            code += each +'\n'
        
        code += '\n'
        for each in codeStep:
            code += each +'\n'
            
        return code

    def _getHeader(self, className, moduleName):
        return 'from {0} import {1}'.format(moduleName,className)
    
    def getInstanceName(self, nodeTag):
        varName = nodeTag
        className = self._getFunctionName(nodeTag)
        instanceName = '{0}_{1}'.format(varName,className)
        return instanceName

    def getInstanceCreateCode(self, nodeTag):
        varName = nodeTag
        className = self._getFunctionName(nodeTag)
        instanceName = '{0}_{1} = {2}()'.format(varName,className,className)
        return instanceName
                            
    def getParents(self, nodeTag):
        self._parents = []
        for eachConn in self.conn:     
            src = eachConn[0]
            dst = eachConn[1]
            if (dst == nodeTag and not src == self.startTag):
                self._parents.append(src)
                self._getParentCore(src)
        return self._parents

    def _getParentCore(self, nodeTag):
        for eachConn in self.conn:     
            src = eachConn[0]
            dst = eachConn[1]
            if (dst == nodeTag and not src == self.startTag):
                self._parents.append(src)
                self._getParentCore(src)        
        

if __name__ == '__main__':
    data = {'blocks': [('node00006', 'subtract', 113.0, -59.0),
            ('node00005', 'multiply', -170.0, -64.0),
            ('node00004', 'divide', -51.0, 77.0),
            ('node00003', 'add', -206.0, 77.0),
            ('node00002', 'End', 248.0, 27.0),
            ('node00001', 'Start', -339.0, 14.0)],
 'conn': [('node00004', 'node00006'),
          ('node00003', 'node00004'),
          ('node00004', 'node00002'),
          ('node00006', 'node00002'),
          ('node00005', 'node00006'),
          ('node00001', 'node00005'),
          ('node00001', 'node00003')]}
    k=kmxNodeGraphReader(data)
    order = k.genereteCode()
    print ("-----")
    print(order)
    print ("===")
