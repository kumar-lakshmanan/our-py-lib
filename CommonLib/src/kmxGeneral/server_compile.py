#-------------------------------------------------------------------------------
# Name:        WINDOWS BINARY COMPILE - FOR module1
#
# Author:      lkumaresan
#
# Created:     05/01/2011
# Copyright:   (c) lkumaresan 2011
# Licence:     Personal
#
# Description:
#
#
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from distutils.core import setup
import py2exe
import sys
import os


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


#PY2EXE CONFIGURATION
MAIN_SCRIPT_FILE = 'PyServer.py'
APPNAME = 'PythonServer'
DESCRIPTION = 'Python Scripting Server'
COMPANY_NAME = 'ABX Studios (pvt) ltd'
COPYRIGHT = 'ABX Studios - Technology'
VERSION = '0.0.0'
USE_ICON = False
ICON_FILE = 'AppIcon.ico'
FOLDER_SUFFIX = 'bin'
RELEASE_OWNER = 'LKUMARESAN'
BUNDLE_LEVEL = 1                        # Can be 1 - For Full Package, 2 - Python Included, 3 - Normal
DO_COMPRESS = True
DO_CONSOLE_SCREEN = True
INCLUDE_SOURCE_ZIP = False
INCLUDES = ['sip','lxml','gzip','xml']
PACKAGES = ['lxml','gzip','xml']

#PY2EXE PROCESS...
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
                        "dist_dir":'bin',
                     }
          }

if DO_CONSOLE_SCREEN:
    if INCLUDE_SOURCE_ZIP:
        setup(console=[appVariable],options=opVars,zipfile=1,version="0.0.0.0",author='LKUMARESAN')
    else:
        setup(console=[appVariable],options=opVars,version="0.0.0.0",author='LKUMARESAN')
else:
    if INCLUDE_SOURCE_ZIP:
        setup(windows=[appVariable],options=opVars,zipfile=1)
    else:
        setup(windows=[appVariable],options=opVars)

print "\n\nEvery thing is fine!"
