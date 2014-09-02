'''
Created on Aug 25, 2014

@author: Mukundan
'''

from PyQt5 import uic
import sys
import os

class CompileUItoPYCls(object):
    '''
    classdocs
    '''

    def convertCore(self, uiFile, pyFile):
        print ("UI File: " + uiFile)
        print ("PY File: " + pyFile)
        
        uiFileHdl = open(uiFile,'r')
        pyFileHdl = open(pyFile,'w')
        
        uic.compileUi(uiFileHdl, pyFileHdl)
        print ("UI->PY Completed!")
        
        uiFileHdl.close()
        pyFileHdl.close()
            
    def getPyFileName(self, uiFile):
        dirpath=str(os.path.dirname(uiFile))
        filename=str(os.path.basename(uiFile))
        filename=filename.replace(".ui", ".py").replace(".UI", ".py") 
        pyFile=os.path.join(dirpath,filename) 
        return pyFile    

    def doConvert(self,uiFile):
        uiFile=str(uiFile).strip()
        if os.path.exists(uiFile):
            pyFile = self.getPyFileName(uiFile)
            self.convertCore(uiFile,pyFile)
        else:
            print("File doesn't exist - " + uiFile)
        print ("Convert Done!")
        
if __name__ == '__main__':
    inputFile = 'F:/Kumaresan/Code/Python/UI2PY/src/qtui/MainUI.ui'
    ui2py = CompileUItoPYCls() 
    ui2py.doConvert(inputFile)
        