from distutils.core import setup
import py2exe
import sys
import os
import shutil

#######Appending Module Search Path########
if __name__ == '__main__':
    currentFolder = os.getcwd()
    parentFolder = os.path.dirname(currentFolder)

####Module Pack folders that will be added to sys search path####
    modulePathList = [
                        currentFolder,
                        parentFolder,
                        parentFolder + '/UI_DB_lib',
                        parentFolder + '/PulseXML',
                        parentFolder + '/Common',
                        'Z:/REPO/PulseServer/Library/Common'
                     ]

    for modulePath in modulePathList:
        modulePath = os.path.normpath(modulePath)
        if modulePath not in sys.path and os.path.exists(modulePath):
            sys.path.append(modulePath)

import xtools
APPNAME = 'LNP'
COMPANY_NAME = 'ABX Studios'
VERSION = '0.0.1'
COPYRIGHT = 'ABX Studios - Technology'
DESCRIPTION = 'LNP - Part of ABX AMS'
MAIN_SCRIPT_FILE = 'LNP.py'
ICON_FILE = 'images/LITEZ.ico'
RELEASE_TYPE = 2                        # 1 - For Major and 2 - For Minor Release
RELEASE_OWNER = 'ABX'
USE_ICON = True
BUNDLE_LEVEL = 1                        # Can be 1 - For Full Package, 2 - Python Included, 3 - Normal
DO_COMPRESS = True
DO_CONSOLE_SCREEN = False
INCLUDE_SOURCE_ZIP = False
INCLUDES=[]
PACKAGES=[]
INCLUDES.append('sip')
INCLUDES.append('lxml')
INCLUDES.append('gzip')
PACKAGES.append('lxml')

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
                        "includes":INCLUDES,
                        "packages":PACKAGES,
                        "bundle_files": BUNDLE_LEVEL,
                        "compressed": DO_COMPRESS,
                        "dist_dir":'bin',
                     }
          }

if not INCLUDE_SOURCE_ZIP:
    zipVariable = None
else:
    zipVariable = 1

if DO_CONSOLE_SCREEN:
    setup(console=[appVariable],options=opVars,zipfile=zipVariable,version="0.1.3.4",author='LKUM')
else:
    setup(windows=[appVariable],options=opVars,zipfile=zipVariable)



print "\n\nEvery thing is fine"