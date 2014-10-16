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

from distutils.core import setup
import os
import shutil
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

# PY2EXE CONFIGURATION
MAIN_SCRIPT_FILE = 'DevConsolePlug.py'
APPNAME = 'KPython'
DESCRIPTION = 'KPython - Standalone Python Interactive Interpreter'
COMPANY_NAME = 'Kumar Studios'
COPYRIGHT = 'Kumar Studios'
VERSION = '0.0.1'
USE_ICON = False
ICON_FILE = 'AppIcon.ico'
FOLDER_SUFFIX = 'BIN'
RELEASE_OWNER = 'LKUMARESAN'
BUNDLE_LEVEL = 1  # Can be 1 - For Full Package, 2 - Python Included, 3 - Normal
DO_COMPRESS = True
DO_CONSOLE_SCREEN = False
INCLUDE_SOURCE_ZIP = False
INCLUDES = ['sip', 'gzip', 'PyQt5.QtPrintSupport']
PACKAGES = []

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
