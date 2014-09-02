
from distutils.core import setup
import py2exe
import sys
import os
#import shutil

#######Appending Module Search Path########
if __name__ == '__main__':
    currentFolder = os.getcwd()

####Adjust these Parent Folder to reach root folder####
    parentFolder1 = os.path.dirname(currentFolder)
    parentFolder2 = os.path.dirname(parentFolder1)

####Pass parentFolder Level to reach Root folder####
    rootFolder = os.path.dirname(parentFolder2)
    rootFolderParent = os.path.dirname(rootFolder)

####Module Pack folders that will be added to sys search path####
    modulePathList = [
                      currentFolder,
                      parentFolder1,
                      parentFolder1 + '\qtui',
                      parentFolder1 + '\main',
                      parentFolder1 + '\main\commandline',
                      parentFolder1 + '\core'
                      #parentFolder1 + '\lib\Controls',
                      #"C:/Windows/winsxs/x86_microsoft.vc90.crt_1fc8b3b9a1e18e3b_9.0.21022.8_none_bcb86ed6ac711f91"
                     ]

    for modulePath in modulePathList:
        if modulePath not in sys.path:
            if os.path.exists(modulePath):
                sys.path.append(modulePath)


#PY2EXE CONFIGURATION
MAIN_SCRIPT_FILE = 'UI2PY.py'
APPNAME = 'UI2PY'
DESCRIPTION = 'Compile PyQT UI to Py File'
COMPANY_NAME = 'Kaymatrix Studios'
COPYRIGHT = 'Kaymatrix Studios - Technology'
VERSION = '0.0.1'
USE_ICON = False
ICON_FILE = 'AppIcon.ico'
FOLDER_SUFFIX = 'bin'
RELEASE_OWNER = 'LKUMARESAN'
BUNDLE_LEVEL = 1                        # Can be 1 - For Full Package, 2 - Python Included, 3 - Normal
DO_COMPRESS = True
DO_CONSOLE_SCREEN = True
INCLUDE_SOURCE_ZIP = False
INCLUDES = ['sip']
EXCLUDES = []
DLL_EXCLUDES = []
PACKAGES = []

"""
EXCLUDES = ["PyQt5.uic.port_v3", "PyQt5.uic.port_v3.ascii_upper", "PyQt5.uic.port_v3.load_plugin", "PyQt5.uic.port_v3.proxy_base",
"PyQt5.uic.port_v3.encode_utf8", "PyQt5.uic.port_v3.string_io", "PyQt5.uic.port_v3.invoke", "uic.port_v3.ascii_upper",
"uic.port_v3.load_plugin", "uic.port_v3.proxy_base", "uic.port_v3.encode_utf8", "uic.port_v3.string_io",
"uic.port_v3.invoke", "uic.port_v3"]
"""

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
                        "excludes":EXCLUDES,
                        "bundle_files": BUNDLE_LEVEL,
                        "dll_excludes":DLL_EXCLUDES,                        
                        "compressed": DO_COMPRESS,
                        "dist_dir":str(MAIN_SCRIPT_FILE[0:len(MAIN_SCRIPT_FILE)-3])+'_'+FOLDER_SUFFIX,
                     }
          }

if DO_CONSOLE_SCREEN:
    if INCLUDE_SOURCE_ZIP:
        setup(console=[appVariable],options=opVars,zipfile=1)
    else:
        setup(console=[appVariable],options=opVars)
else:
    if INCLUDE_SOURCE_ZIP:
        setup(windows=[appVariable],options=opVars,zipfile=1)
    else:
        setup(windows=[appVariable],options=opVars)

print ("\n\nEvery thing is fine!")
