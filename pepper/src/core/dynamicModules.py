'''
Created on Jul 13, 2015

@author: MUKUND
'''

from core.devPlugs import nodes
import pkgutil
import inspect

class DynamicModules():
    
    def __init__(self, package):
        self.package = package
        self.reParseModules()

    def reParseModules(self):
        self.classes = []
        prefix = self.package.__name__ + "."
        for importer, modname, ispkg in pkgutil.iter_modules(self.package.__path__, prefix):
            #print ("Found submodule %s (is a package: %s, importer %s)" % (modname, ispkg, importer))  
            module = __import__(modname, fromlist="dummy")

            if (not ispkg):
                for each in inspect.getmembers(module, inspect.isclass):
                    className = each[0]
                    classObj = each[1]
                    self.classes.append((className, module.__name__))     
                    
    def getVariables(self, className, moduleName):
        return self._getVariablesCore(self.getClassInstance(className, moduleName))
    
    def getInVariables(self, className, moduleName):
        lst = self._getVariablesCore(self.getClassInstance(className, moduleName))
        ret = []
        for each in lst:
            if "in" in each:
                ret.append(each)
        return ret
    
    def getOutVariables(self, className, moduleName):
        lst = self._getVariablesCore(self.getClassInstance(className, moduleName))
        ret = []
        for each in lst:
            if "out" in each:
                ret.append(each)
        return ret
            
    def getClassInstance(self, className, moduleName):
           
        if (not moduleName or moduleName==''):
            return None   
        module = __import__(moduleName, fromlist="dummy")
        for each in inspect.getmembers(module, inspect.isclass):
            eachClassName = each[0]
            eachClassObj = each[1]
            if (eachClassName==className):                
                return eachClassObj()
        return None
                        
    def _getVariablesCore(self, cls, exclude_methods=True):
        base_attrs = dir(type('dummy', (object,), {}))
        this_cls_attrs = dir(cls)
        res = []
        for attr in this_cls_attrs:
            if base_attrs.count(attr) or (callable(getattr(cls,attr)) and exclude_methods):
                continue
            res += [attr]
        return res            

if __name__ == '__main__':
    d = DynamicModules(nodes)    
    print(d.getVariables('Add', 'core.devPlugs.nodes.add'))