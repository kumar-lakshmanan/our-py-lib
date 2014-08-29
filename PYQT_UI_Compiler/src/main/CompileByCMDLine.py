'''
Created on Aug 23, 2014

@author: Mukundan
'''
from core.CompileUItoPY import CompileUItoPYCls
import sys
import os

if __name__ == '__main__':    
    if(len(sys.argv)>1):
        uiFile = str(sys.argv[1]).strip()
        cmp = CompileUItoPYCls()
        cmp.doConvert(uiFile)        