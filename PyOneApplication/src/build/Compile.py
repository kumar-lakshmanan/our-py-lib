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
import requests
import requests.certs
import ssl

# Search Paths...
currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)
modulePathList = [
                  parentFolder,
                  currentFolder,
                  parentFolder + '/Common',
                    ]
for modulePath in modulePathList:
    modulePath = os.path.normpath(modulePath)
    if modulePath not in sys.path and os.path.exists(modulePath):
        sys.path.append(modulePath)

sys.path.append('J:\our-py-lib\PyOneApplication')
sys.path.append('J:\our-py-lib\PyOneApplication\src')
sys.path.append('J:\our-py-lib\PyOneApplication\core')
sys.path.append('J:\our-py-lib\PyOneApplication\build')
sys.path.append('J:\our-py-lib\PyOneApplication\resources')
sys.path.append('J:\our-py-lib\PyOneApplication\interfaces')

dllpath = r'C:\Windows\winsxs\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.30729.4148_none_5090ab56bcba71c2'

sys.path.append(dllpath)
DATAS = [
    ## Instruct setup to copy the needed DLL files into the build directory
    ("Microsoft.VC90.CRT", glob(dllpath + r'\*.*')),
    ('',[requests.certs.where()]),
    #('',['J:\our-py-lib\CommonLib\src\kmxPyQt\devConsole3\certs\*.*']),
]

# PY2EXE CONFIGURATION
MAIN_SCRIPT_FILE = 'J:\our-py-lib\PyOneApplication\src\PyOne.py'
APPNAME = 'PyOne'
DESCRIPTION = 'PyOne - Python based automation for windows'
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
INCLUDES = ['sip', 'PyQt5.QtPrintSupport', 'PyQt5', 'win32com.client','numpy','bs4','requests','json','urllib3','xmlutils','lxml','simplejson','dict2xml','xml','pythoncom','logging','PyQt5.Qsci','matplotlib','pylab','robobrowser']
PACKAGES = ['kmxPyQt.devConsole3', 'PyQt5', 'win32com','requests','lxml','simplejson','dict2xml','xml','matplotlib','simplenote']
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
                     },
            "build_exe":{
                            "include_files":[(requests.certs.where(),'cacert.pem')]
                         }
          }

if DO_CONSOLE_SCREEN:
    if INCLUDE_SOURCE_ZIP:
        setup(console=[appVariable], options=opVars, zipfile=1, data_files=DATAS, version="0.0.0.1", author='LKUMARESAN')
    else:
        setup(console=[appVariable], options=opVars, data_files=DATAS, version="0.0.0.1", author='LKUMARESAN')
else:
    if INCLUDE_SOURCE_ZIP:
        setup(windows=[appVariable], options=opVars, data_files=DATAS, zipfile=1)
    else:
        setup(windows=[appVariable], options=opVars, data_files=DATAS)

print ("\n\nEvery thing is fine!")


