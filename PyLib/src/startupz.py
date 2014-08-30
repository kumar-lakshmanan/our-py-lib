#-------------------------------------------------------------------------------
# Name:        Python Editor Startup
#
# Author:      lkumaresan
#
# Created:     20/09/2010
# Copyright:   (c) lkumaresan 2010
# Licence:     Personal
#
# Description:
#       For Initalizing Module Search Paths
#
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import os
import sys

modulePaths = [
                    'C:/Python25',
                    'C:/Python25/Lib',
                    'C:/Python25/DLLs',
                    'C:/Python25/Lib/lib-tk',
                    'C:/Python25/Lib/site-packages',
                    'C:/Python25/lib/site-packages/PIL',
                    'C:/WINDOWS/system32/python25.zip',
                    'D:/Kumaresan/Lib',
                    'D:/REPO/SOURCE/SCRIPTS/PYTHON/Common',
                    'D:/REPO/SOURCE/SCRIPTS/PYTHON/UI_DB_lib',
                    'D:/REPO/SOURCE/SCRIPTS/PYTHON/PULSE_GREEN',
                    'D:/REPO/SOURCE/SCRIPTS/PYTHON/SceneAccessManager',
                    'D:/REPO/SOURCE/SCRIPTS/PYTHON/LSAM',
                 ]

#sys.path = [] #CAUTION - MAKE SURE YOU HAVE GIVEN ALL PATH INCLUDING SYSTEM PATHS
syspaths = [os.path.realpath(path) for path in sys.path]
modpaths = [os.path.realpath(path) for path in modulePaths]

for eachModulePath in modpaths:
    if eachModulePath not in syspaths:
        if os.path.exists(eachModulePath):
            sys.path.append(eachModulePath)