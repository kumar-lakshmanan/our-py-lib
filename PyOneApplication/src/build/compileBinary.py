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

import socket
import version
from kmxGeneral import kmxTools

####################### PY2EXE CONFIGURATION ##############################
###########################################################################

currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)
parentFolder2 = os.path.dirname(parentFolder)
modulePathList = [
                    parentFolder2,
                    parentFolder,
                    currentFolder,
                    parentFolder + '/core',
                    parentFolder + '/interfaces',
                    parentFolder + '/resources',
                    ]

#BASIC CONFIG
BUILD_TYPE = int(input('Enter Build type: # Can be 0 - For test build, 1 - For Fix build, 2 - For Minor build, 3 - For Major build: \n') or '0')
MAIN_SCRIPT_FILE = r'F:\PythonWorkspace\our-py-lib\PyOneApplication\src\PyOne.py'
DESTINATION_DIR = r'F:\PythonWorkspace\our-py-lib\tools\PYONE\pack'
USE_ICON = True
ICON_FILE = 'appicon.ico'
BUNDLE_LEVEL = 3  # Can be 1 - For Full Package, 2 - Python Included, 3 - Normal
DO_COMPRESS = False
DO_CONSOLE_SCREEN = False
INCLUDE_SOURCE_ZIP = False
INCLUDES = ['sip', 'PyQt5.QtPrintSupport', 'PyQt5', 'bs4','requests','json','urllib3','xmlutils','xml','logging','PyQt5.Qsci']
PACKAGES = ['PyQt5','requests','xml']
EXCLUDES = []

#FILES TO COPY
listOfFiles = []
listOfFiles.append(('Microsoft.VC90.CRT', glob(r'C:\Windows\winsxs\x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.30729.4148_none_5090ab56bcba71c2\*.*')))
listOfFiles.append(('platforms', glob(r'F:\PythonWorkspace\our-py-lib\PyOneApplication\src\bin\platforms\*.*')))
listOfFiles.append(('', glob(r'F:\PythonWorkspace\our-py-lib\PyOneApplication\src\template*.*')))
listOfFiles.append(('', glob(r'F:\PythonWorkspace\our-py-lib\PyOneApplication\src\help.*')))
listOfFiles.append(('', glob(r'F:\PythonWorkspace\our-py-lib\PyOneApplication\src\devSystem.*')))
listOfFiles.append(('', [requests.certs.where()]))

###########################################################################

for modulePath in modulePathList:
    modulePath = os.path.normpath(modulePath)
    print("Search Path Includes...." + str(modulePath))
    if modulePath not in sys.path and os.path.exists(modulePath):
        sys.path.append(modulePath)

k=kmxTools.Tools()

majorNumber = version.__buildNumber__.split('.')[0]
minorNumber = version.__buildNumber__.split('.')[1]
fixNumber = version.__buildNumber__.split('.')[2]
testNumber = version.__buildNumber__.split('.')[3]
history = version.__buildHistory__
changeHistory = ''

if (BUILD_TYPE==0):
    print("--------------------Performing test build--------------------")
    testNumber = int(testNumber)+1
elif (BUILD_TYPE==1):
    print("--------------------Performing fix build--------------------")    
    fixNumber = int(fixNumber)+1
    testNumber = 0
elif (BUILD_TYPE==2):
    print("--------------------Performing minor build--------------------")
    changeHistory=str(input("Change History: ") or 'Default minor release')    
    minorNumber = int(minorNumber)+1
    fixNumber = 0
    testNumber = 0
elif (BUILD_TYPE==3):
    print("--------------------Performing major build--------------------")
    changeHistory=str(input("Change History: ") or 'Default major release')
    majorNumber = int(majorNumber)+1
    minorNumber = 0    
    fixNumber = 0
    testNumber = 0    
else:
    print("--------------------Performing test build--------------------")
    testNumber = int(testNumber)+1
    
curAppName = version.__buildAppName__
curAppDescription = version.__buildAppDescription__
curCompanyName = version.__buildCompanyName__
curCopyrights = version.__buildCopyrights__
curProductName = version.__buildProductName__

curVersion = str('{0}.{1}.{2}.{3}'.format(majorNumber, minorNumber, fixNumber, testNumber))
curDate = k.getDateTime() 
curSystem = k.getSystemName() 
curOwner = k.getCurrentUser()

if (changeHistory):
    curHistory = str(history + '<br>Version: ' + curVersion + '  -  Date: ' + curDate + '<br>-------<br><br>' + changeHistory + '<br>')
else:
    curHistory = str(history)
    
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
data += '__buildHistory__="{0}"\n'.format(curHistory)

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

# PY2EXE PROCESS...
if len(sys.argv)<=1: sys.argv.append('py2exe')
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
                        "dist_dir":DESTINATION_DIR,
                     },
            "build_exe":{
                            "include_files":[(requests.certs.where(),'cacert.pem')]
                         }
          }

if DO_CONSOLE_SCREEN:
    if INCLUDE_SOURCE_ZIP:
        r=setup(console=[appVariable], options=opVars, zipfile=1, data_files=listOfFiles, version=version.__buildNumber__, author=version.__buildOwner__)
    else:
        r=setup(console=[appVariable], options=opVars, data_files=listOfFiles, version=version.__buildNumber__, author=version.__buildOwner__)
else:
    if INCLUDE_SOURCE_ZIP:
        r=setup(windows=[appVariable], options=opVars, data_files=listOfFiles, zipfile=1 ,version=version.__buildNumber__, author=version.__buildOwner__)
    else:
        r=setup(windows=[appVariable], options=opVars, data_files=listOfFiles, version=version.__buildNumber__, author=version.__buildOwner__)

print ("\nEvery thing is fine!")