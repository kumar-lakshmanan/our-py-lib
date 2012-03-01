#-------------------------------------------------------------------------------
# Name:        QtTable
# Purpose:
#
# Author:      AIAA
#
# Created:     10-11-2011
# Copyright:   (c) AIAA 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from PyQt4 import QtCore, QtGui
import sip
import inspect
import traceback
import sys
import os

global callingParent
callingParent=None

def ImportModule(parent, script, fromDir='', _globals_=None, _locals_=None):

    '''
    Imports and returns you the module.

    userMod = ImportModule('RunMe.py')
    userMod.myclass()

    '''
    global callingParent
    callingParent=parent
    imported = 0
    try:
        if script:
            script = str(script).strip()
            if os.path.exists(script):
                ext = os.path.splitext(script)[-1][1:].upper()
                if ext and ext=='PY':
                    fileName = os.path.basename(script)[:-3]
                    filePath = os.path.dirname(script)
                    filePath = filePath if filePath else os.getcwd()
                    if not '.' in fileName:
                        if filePath and os.path.exists(filePath):
                            os.chdir(filePath)
                            _addToSysPath(filePath)
                            globals_ = _globals_ if _globals_ else globals()
                            locals_ = _locals_ if _locals_ else locals()
                            userModule = __import__(fileName, globals_, locals_, [fromDir])
                            if inspect.ismodule(userModule):
                                return userModule
                            else:
                                print 'Not a module'
                        else:
                            print 'Path does not exist!'
                    else:
                        print 'More then one ext!'
                else:
                    print 'Not a PY file!'
            else:
                print 'Script does not exit!'
        else:
            print 'No Script Given!'
    except:
        print errorReport()
    return None

def _addToSysPath(path):
    if path and os.path.exists(path):
        path = os.path.normpath(path)
        if path not in sys.path:
            sys.path.append(path)

def errorReport(prittyPrint=1):
    try:
        TrackStack = sys.exc_traceback
        ErrorReport = []
        while TrackStack:
        	FileName = TrackStack.tb_frame.f_code.co_filename
        	FunctionName = TrackStack.tb_frame.f_code.co_name
        	ErrorLine =TrackStack.tb_lineno
        	TrackStack = TrackStack.tb_next
        	ErrorReport.append([FileName,FunctionName,ErrorLine])
        ErrorReport.append([sys.exc_info()[0],sys.exc_info()[1],0])
        if prittyPrint:
            ErrorInfo=''
            for eachErrorLevel in ErrorReport:
                ErrorInfo+= '\nFile: "' + str(eachErrorLevel[0]) + '", line ' + str(eachErrorLevel[2]) + ', in ' + str(eachErrorLevel[1])
            return ErrorInfo
        else:
            return ErrorReport
    except:
        return 'Problem Preparing Error Report'

def crashHandle():
        #Prepare Report
        data = errorReport()
        file_ = os.path.join(currentFolder,'CrashReport.txt')
        chf = open(file_,'w')
        chf.write(str(data))
        chf.close()
