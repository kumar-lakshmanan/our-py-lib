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
MAIN_SCRIPT_FILE = 'PulseLightNPray.py'
ICON_FILE = 'images/LITEZ.ico'
RELEASE_TYPE = 2                        # 1 - For Major and 2 - For Minor Release
RELEASE_OWNER = 'ABX'
FOLDER_SUFFIX = 'Win64'
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

if sys.argv[1] == 'py2exe':


    if RELEASE_TYPE==1:
        RELEASE_TYPE = 'MAJOR'
    else:
        RELEASE_TYPE = 'MINOR'

    print "\n\nHandling Version Log...\n"

    AppName = MAIN_SCRIPT_FILE[0:len(MAIN_SCRIPT_FILE)-3]
    AppVerFile = AppName+'_Version.ini'
    AppVerSection = 'Release_Info'
    AppVerBinName = 'Binary_Name'
    AppVerMjrVer = 'Built_Major_Version'
    AppVerMinVer = 'Built_Minor_Version'
    AppVerOwner = 'Built_Release_Owner'
    AppVerType = 'Built_Release_Type'
    AppVerDate = 'Built_Date'
    Value_Date = str(xtools.nowdatetime())

    bin_Name = xtools.INIReadValue(AppVerFile,AppVerSection,AppVerBinName,1,(AppName+'.EXE'))
    minor_ver = int(xtools.INIReadValue(AppVerFile,AppVerSection,AppVerMinVer,1,001))
    major_ver = int(xtools.INIReadValue(AppVerFile,AppVerSection,AppVerMjrVer,1,000))
    ver_data = xtools.INIReadValue(AppVerFile,AppVerSection,AppVerDate,1,Value_Date)
    owner = xtools.INIReadValue(AppVerFile,AppVerSection,AppVerOwner,1,RELEASE_OWNER)
    rtype = xtools.INIReadValue(AppVerFile,AppVerSection,AppVerType,1,RELEASE_TYPE)


    if RELEASE_TYPE=='MAJOR':
        major_ver+=1
        minor_ver=0

    if RELEASE_TYPE=='MINOR':
        minor_ver+=1

    print "\n\n\n"
    print "Release Type: ", RELEASE_TYPE
    print "Release Major Version: ", major_ver
    print "Release Minor Version: ", minor_ver
    print "\n\n\n"

    xtools.INISetValue(AppVerFile,AppVerSection,AppVerMinVer,minor_ver)
    xtools.INISetValue(AppVerFile,AppVerSection,AppVerMjrVer,major_ver)
    xtools.INISetValue(AppVerFile,AppVerSection,AppVerDate,Value_Date)
    xtools.INISetValue(AppVerFile,AppVerSection,AppVerOwner,RELEASE_OWNER)
    xtools.INISetValue(AppVerFile,AppVerSection,AppVerType,RELEASE_TYPE)

    info = 'This file is auto generated on official ' + RELEASE_TYPE + ' release of ' + AppName + '. Do not edit any part of this file.'

    xtools.INISetValue(AppVerFile,AppVerSection,'INFO',info)



    Desti = currentFolder  + '/' + str(MAIN_SCRIPT_FILE[0:len(MAIN_SCRIPT_FILE)-3])+'_'+FOLDER_SUFFIX
    if not os.path.exists(Desti):
        os.makedirs(Desti)

    SourceFile = currentFolder + '/' + AppVerFile
    DestiFile = Desti + '/' + AppVerFile

    if os.path.exists(SourceFile) and os.path.exists(Desti):
        shutil.copy(SourceFile,DestiFile)


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
                        "dist_dir":str(MAIN_SCRIPT_FILE[0:len(MAIN_SCRIPT_FILE)-3])+'_'+FOLDER_SUFFIX,
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