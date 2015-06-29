#-------------------------------------------------------------------------------
# Name:        module1
#
# Author:      lkumaresan
#
# Created:     12/01/2011
# Copyright:   (c) lkumaresan 2011
# Licence:     Personal
#
# Description:
#
#
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import os
import sys

##Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()


#Module Search Path
currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)
parentFolder1 = os.path.dirname(parentFolder)
parentFolder2 = os.path.dirname(parentFolder1)
parentFolder3 = os.path.dirname(parentFolder2)
modulePathList = [
                  parentFolder,
                  currentFolder,
                  parentFolder1   + '/UI_DB_lib',
                  parentFolder1   + '/UI_DB_lib/controls',
                  parentFolder1   + '/UI_DB_lib/PythonEngine',
                  parentFolder1   + '/Common',

                    ]
for modulePath in modulePathList:
    modulePath = os.path.normpath(modulePath)
    if modulePath not in sys.path and os.path.exists(modulePath):
        sys.path.append(modulePath)

#Global Lib
from PyQt4 import QtGui, QtCore
import time
import base64
import os
import sys
import filecmp
import shutil

#Application Lib
import PyInterface
import qt_common
import override
import list_box
import combo_box
import table
import iniConfigReadWrite
import commandLine
import inspect
import threading

if __name__ == '__main__':
    status = 1
    logicFile = 'server_logic.py'
    if os.path.exists(logicFile):
        logicMod = PyInterface.ImportModule(logicFile)
        if logicMod: status = logicMod.process(sys.argv)
    else:
        print 'server_logic.py not found!'
    sys.exit(status)

