



class myDynamicCls():
    def __init__(self, attList):
        self.dynAttr = attrList

        for eachAttr in attList:
            self.__dict__[eachAttr]=''



newobj = myDynamicCls(['attribute1','attribute1','attribute1'])

newobj.dynAttr[0] = 10

print newobj.dynAttr
