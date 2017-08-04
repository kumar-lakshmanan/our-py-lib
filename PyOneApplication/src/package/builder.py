'''
Created on Oct 22, 2015

@author: MUKUND-update-yes
'''

import version
import logging
from kmxGeneral import kmxTools
from PyInstaller.building import build_main
import PyInstaller.configure as configure
from logging import getLogger, INFO, WARN, DEBUG, ERROR, FATAL

specFile = 'pyOne.spec'
workpath = 'temp'
distpath = '.'
logFormt = '%(relativeCreated)d %(levelname)s: %(message)s'
logLevel = logging.DEBUG
 
#Ready logger
logging.basicConfig(format=logFormt, level=logLevel)
logger=getLogger(__name__)

#Support
kttls = kmxTools.Tools()

#Backup old settings
src = './PyOne/settings.ini'
dst = './additionalFiles/settings.ini'
logger.debug('Backup Copy: %s',src)
if(kttls.isPathOK(src)): kttls.copyFile(src, dst)

src = './PyOne/config.ini'
dst = './additionalFiles/config.ini'
logger.debug('Backup Copy: %s',src)
if(kttls.isPathOK(src)): kttls.copyFile(src, dst)

#Versioning
BUILD_TYPE = int(input('Enter Build type: # Can be 0 - For test build, 1 - For Fix build, 2 - For Minor build, 3 - For Major build: \n') or '0')
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
curDate = kttls.getDateTime() 
curSystem = kttls.getSystemName() 
curOwner = kttls.getCurrentUser()

if (changeHistory):
    curHistory = str(history + '\n<br>Version: ' + curVersion + '  -  Date: ' + curDate + '<br>-------<br>' + changeHistory + '<br>')
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
data += '__buildHistory__="""{0}"""\n'.format(curHistory)

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

# Start Building
logger.debug("Starting build process...")
build_main.main(None, specFile, noconfirm=True, ascii=True, distpath=distpath, workpath=workpath, clean_build=True)
logger.debug("Completed!")

