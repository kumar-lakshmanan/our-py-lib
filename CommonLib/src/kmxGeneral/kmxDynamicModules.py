'''
Created on Jul 18, 2015

@author: MUKUND
'''
import pkgutil
import inspect
import sys

class KMXDynamicModules(object):
    '''
    classdocs
    '''

    def __init__(self, package):
        self.package = package
        self.classes = []        
        ##self.reParseModules()
        
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

    def getDevPlugClasses(self):
        lst=[]
        for eachModule in sys.modules:
            
            if eachModule=='devPlugs':
                module = __import__(eachModule, fromlist="dummy")
                for each in inspect.getmembers(sys.modules['devPlugs'], inspect.isclass):
                    print (each)
                    className = each[0]
                    classObj = each[1]
                    lst.append((className, eachModule))
        return lst
                            
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
    
    def getVaraiables(self, cls, exclude_methods=True):
        base_attrs = dir(type('dummy', (object,), {}))
        this_cls_attrs = dir(cls)
        res = []
        for attr in this_cls_attrs:
            if base_attrs.count(attr) or (callable(getattr(cls,attr)) and exclude_methods):
                continue
            res += [attr]
        return res       
                                                     