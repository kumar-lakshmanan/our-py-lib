#-------------------------------------------------------------------------------
# Name:        WINDOWS BINARY COMPILE - FOR module1
#
# Author:      lkumaresan
#
# Created:     09/12/2010
# Copyright:   (c) lkumaresan 2010
# Licence:     Personal
#
# Description:
#
#
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from glob import glob
from distutils.core import setup
import os
import shutil
import sys
import sys

import py2exe


# Search Paths...
currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)
modulePathList = [
                  parentFolder,
                  currentFolder,
                  parentFolder + '/UI_DB_lib',
                  parentFolder + '/UI_DB_lib/DevConsole3',
                  parentFolder + '/UI_DB_lib/controls',
                  parentFolder + '/Common',
                    ]
for modulePath in modulePathList:
    modulePath = os.path.normpath(modulePath)
    if modulePath not in sys.path and os.path.exists(modulePath):
        sys.path.append(modulePath)

sys.path.append('J:\Python\CommonLib\src')
sys.path.append('J:\Python\CommonLib\src\kmxPyQt')

dllpath = r'C:\Windows\winsxs\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.30729.4148_none_5090ab56bcba71c2'

sys.path.append(dllpath)
data_files = [
    ## Instruct setup to copy the needed DLL files into the build directory
    ("Microsoft.VC90.CRT", glob(dllpath + r'\*.*')),
]

# PY2EXE CONFIGURATION
MAIN_SCRIPT_FILE = 'DevConsolePlug.py'
APPNAME = 'HaPy'
DESCRIPTION = 'HaPy - HAndy PYthon'
COMPANY_NAME = 'Kumar Studios'
COPYRIGHT = 'Kumar Studios'
VERSION = '0.0.1'
USE_ICON = True
ICON_FILE = 'appicon.ico'
FOLDER_SUFFIX = 'BIN'
RELEASE_OWNER = 'LKUMARESAN'
BUNDLE_LEVEL = 3  # Can be 1 - For Full Package, 2 - Python Included, 3 - Normal
DO_COMPRESS = False
DO_CONSOLE_SCREEN = False
INCLUDE_SOURCE_ZIP = False
INCLUDES = ['sip', 'PyQt5.QtPrintSupport', 'PyQt5', 'win32com.client','numpy']
PACKAGES = ['kmxPyQt.devConsole3', 'PyQt5', 'win32com']
EXCLUDES = []

# PY2EXE PROCESS...
appVariable = {
                'name': APPNAME,
                'version': VERSION,
                'company_name': COMPANY_NAME,
                'copyright': COPYRIGHT,
                'description': DESCRIPTION
              }

if MAIN_SCRIPT_FILE: appVariable['script'] = MAIN_SCRIPT_FILE
if USE_ICON: appVariable['icon_resources'] = [(0, ICON_FILE)]

opVars = {
            "py2exe":{
                        "packages":PACKAGES,
                        "includes":INCLUDES,
                        "excludes":EXCLUDES,
                        "bundle_files": BUNDLE_LEVEL,
                        "compressed": DO_COMPRESS,
                        "dist_dir":str(MAIN_SCRIPT_FILE[0:len(MAIN_SCRIPT_FILE) - 3]) + '_' + FOLDER_SUFFIX,
                     }
          }

if DO_CONSOLE_SCREEN:
    if INCLUDE_SOURCE_ZIP:
        setup(console=[appVariable], options=opVars, zipfile=1, version="0.0.0.1", author='LKUMARESAN')
    else:
        setup(console=[appVariable], options=opVars, version="0.0.0.1", author='LKUMARESAN')
else:
    if INCLUDE_SOURCE_ZIP:
        setup(windows=[appVariable], options=opVars, zipfile=1)
    else:
        setup(windows=[appVariable], options=opVars)

print ("\n\nEvery thing is fine!")
