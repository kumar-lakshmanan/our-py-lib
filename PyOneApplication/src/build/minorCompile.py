#-------------------------------------------------------------------------------
# Name:        WINDOWS BINARY COMPILE 
#
# Author:      lkumaresan
#
# Created:     09/12/2010
# Copyright:   (c) lkumaresan 2010
# Licence:     Personal
#
# Description:
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

import socket
import version
from kmxGeneral import kmxTools

k=kmxTools.Tools()

majorNumber = version.__buildNumber__.split('.')[0]
minorNumber = version.__buildNumber__.split('.')[1]
fixNumber = version.__buildNumber__.split('.')[2]
testNumber = version.__buildNumber__.split('.')[3]

print("Minor build compilation..")
minorNumber = int(minorNumber)+1
fixNumber = 0
testNumber = 0

curAppName = version.__buildAppName__
curAppDescription = version.__buildAppDescription__
curCompanyName = version.__buildCompanyName__
curCopyrights = version.__buildCopyrights__
curProductName = version.__buildProductName__

curVersion = str('{0}.{1}.{2}.{3}'.format(majorNumber, minorNumber, fixNumber, testNumber))
curDate = k.getDateTime() 
curSystem = k.getSystemName() 
curOwner = k.getCurrentUser()

data = ''
data += '__buildAppName__="{0}"\n'.format(curAppName) 
data += '__buildProductName__="{0}"\n'.format(curProductName) 
data += '__buildAppDescription__="{0}"\n'.format(curAppDescription) 
data += '__buildCompanyName__="{0}"\n'.format(curCompanyName) 
data += '__buildCopyrights__="{0}"\n'.format(curCopyrights)

data += '__buildNumber__="{0}"\n'.format(curVersion) 
data += '__buildDateTime__="{0}"\n'.format(curDate)
data += '__buildSystem__="{0}"\n'.format(curSystem)
data += '__buildOwner__="{0}"\n'.format(curOwner)

version.__buildNumber__ = curVersion
version.__buildDateTime__ = curDate
version.__buildSystem__ = curSystem
version.__buildOwner__ = curOwner

print('{0}: {1}'.format('AppName'.ljust(20,'.'), version.__buildAppName__))
print('{0}: {1}'.format('ProductName'.ljust(20,'.'), version.__buildProductName__))
print('{0}: {1}'.format('AppDescription'.ljust(20,'.'), version.__buildAppDescription__))
print('{0}: {1}'.format('CompanyName'.ljust(20,'.'), version.__buildCompanyName__))
print('{0}: {1}'.format('Copyrights'.ljust(20,'.'), version.__buildCopyrights__))

print('{0}: {1}'.format('Version'.ljust(20,'.'), version.__buildNumber__))
print('{0}: {1}'.format('Date'.ljust(20,'.'), version.__buildDateTime__))
print('{0}: {1}'.format('System'.ljust(20,'.'), version.__buildSystem__))
print('{0}: {1}'.format('Owner'.ljust(20,'.'), version.__buildOwner__))
print('\n')

f = open('version.py','w')
f.write(data)
f.close()

# PY2EXE CONFIGURATION
MAIN_SCRIPT_FILE = 'J:\our-py-lib\PyOneApplication\src\PyOne.py'
USE_ICON = True
ICON_FILE = 'appicon.ico'
BUNDLE_LEVEL = 3  # Can be 1 - For Full Package, 2 - Python Included, 3 - Normal
DO_COMPRESS = False
DO_CONSOLE_SCREEN = False
INCLUDE_SOURCE_ZIP = False
INCLUDES = ['sip', 'PyQt5.QtPrintSupport', 'PyQt5', 'win32com.client','numpy','bs4','requests','json','urllib3','xmlutils','lxml','simplejson','dict2xml','xml','pythoncom','logging','PyQt5.Qsci','matplotlib','pylab','robobrowser']
PACKAGES = ['kmxPyQt.devConsole3', 'PyQt5', 'win32com','requests','lxml','simplejson','dict2xml','xml','matplotlib','simplenote']
EXCLUDES = []

# PY2EXE PROCESS...
appVariable = {
                'name': version.__buildAppName__,
                'version': version.__buildNumber__,
                'company_name': version.__buildCompanyName__,
                'copyright': version.__buildCopyrights__,
                'description': version.__buildAppDescription__,
                'product_name': version.__buildProductName__
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
                        "dist_dir":"../bin",
                     },
            "build_exe":{
                            "include_files":[(requests.certs.where(),'cacert.pem')]
                         }
          }

if DO_CONSOLE_SCREEN:
    if INCLUDE_SOURCE_ZIP:
        setup(console=[appVariable], options=opVars, zipfile=1, data_files=DATAS, version=version.__buildNumber__, author=version.__buildOwner__)
    else:
        setup(console=[appVariable], options=opVars, data_files=DATAS, version=version.__buildNumber__, author=version.__buildOwner__)
else:
    if INCLUDE_SOURCE_ZIP:
        setup(windows=[appVariable], options=opVars, data_files=DATAS, zipfile=1 ,version=version.__buildNumber__, author=version.__buildOwner__)
    else:
        setup(windows=[appVariable], options=opVars, data_files=DATAS, version=version.__buildNumber__, author=version.__buildOwner__)

print ("\n\nEvery thing is fine!")


