import os
import sys
import shutil
import filecmp
import subprocess as sp
import file_sys
import software_versioning as sv

def doGetCopyInfo():

    appName = 'pulse_green'
    baseSrvPath = 'Z:/REPO/PulseServer/ProgramFiles/GREEN'
    baseLclPath = 'D:/ABX_PULSE/ProgramFiles/GREEN'
    appExeName = 'Pulse.exe'
    shortcutFile = 'PulseGreen.lnk'
    releaseLog = 'ReleaseLog.xml'

    infoDict = {

    'appName' : appName,

    'srvFolder' : baseSrvPath,
    'srvAppFile' : os.path.join(baseSrvPath, appExeName),
    'srvReleaseLog' : os.path.join(baseSrvPath, releaseLog),

    'lclFolder' : baseLclPath,
    'lclAppFile' : os.path.join(baseLclPath, appExeName),
    'lclReleaseLog' : os.path.join(baseLclPath, releaseLog),

    'shortcutFile' : os.path.join(baseSrvPath, shortcutFile),
    'shortcutFolder' : '//ABXroam/Redirections/%s/Desktop' % os.getenv('USERNAME'),

                }
    return infoDict


def doStartApplication():
    #Updater Invoke
    exe = doGetConfigInfo('lclAppFile')
    if os.path.exists(exe):
        cdir = os.path.dirname(exe)
        try:
            import PyInterface
            sp.Popen(exe, cwd=cdir)
        except:
            print 'error: %s ' % PyInterface.errorReport()

def doIsInstalled():
    exe = doGetConfigInfo('lclAppFile')
    print 'Application Installed!' if os.path.exists(exe) else 'Application Not Installed'
    return os.path.exists(exe)

def doGetConfigInfo(config):
    if not config or config =='': print 'Pass argument config to get value'
    info = doGetCopyInfo()
    if info.has_key(config):
        return info[config]

def doGetServerVersion():
    info = doGetCopyInfo()
    file_ = info['srvReleaseLog']
    appName = info['appName']
    version = sv.versioning(file_, appName)
    if version.isReady():
        recentVer = version.getPackedRecentVersion()
        print 'Recent vesion: %s' % recentVer
        return recentVer

def doGetInstalledVerison():
    info = doGetCopyInfo()
    file_ = info['lclReleaseLog']
    appName = info['appName']
    version = sv.versioning(file_, appName)
    if version.isReady():
        recentVer = version.getPackedRecentVersion()
        print 'Installed vesion: %s' % recentVer
        return recentVer

def doCheckIsRecentVersion(versionNo):
    if not versionNo or versionNo =='': print 'Pass version number to check.'
    info = doGetCopyInfo()
    file_ = info['srvReleaseLog']
    appName = info['appName']
    version = sv.versioning(file_,appName)
    if version.isReady():
        recentVer = version.getPackedRecentVersion()
        if versionNo == recentVer:
            print 'Recent version'
            return True
        else:
            print 'Not a recent version'
            return False
        return False

def doCopy():
    '''
    Install cum Updater (Copy) for Pulse Beat
    '''
    f = file_sys.FileSysHandle()

    #Initializing
    info = doGetCopyInfo()
    srvReleaseLog = info['srvReleaseLog']
    lclReleaseLog = info['lclReleaseLog']
    srvAppFile = info['srvAppFile']
    lclAppFile = info['lclAppFile']
    srvFolder = info['srvFolder']
    lclFolder = info['lclFolder']
    shortcutFile = info['shortcutFile']
    shortcutFolder = info['shortcutFolder']


    processFreshCopy = 0
    processUpdate = 0

    flagUpdate = 0


    #Step1 - Gather System Status
    print 'Gathering System Status...'
    if not f.isExist(srvAppFile):
        print '%s not found. Aborting Copy process!' % srvAppFile
    else:
        print 'Ready - %s!' % srvAppFile

    if not f.isExist(srvFolder):
        print '%s not found. Aborting Copy process!' % srvFolder
        return 0
    else:
        print 'Ready - %s!' % srvFolder

    if not f.isExist(lclFolder): f.iaMakeFolder(lclFolder)
    if not f.isExist(lclFolder):
        print '%s not found. Unable to create folder! Aborting Copy process!' % lclFolder
        return 0
    else:
        print 'Ready - %s!' % lclFolder

    if not f.isExist(srvReleaseLog):
        print '%s not found. Aborting Copy process!' % srvReleaseLog
    else:
        print 'Ready - %s!' % srvReleaseLog

    if not f.isExist(lclReleaseLog):
        print '%s not found. Might be fresh Copy process!' % lclReleaseLog
    else:
        print 'Ready - %s!' % lclReleaseLog


    if not f.isExist(shortcutFile):
        print '%s not found. Shortcut wont be updated!' % shortcutFile
    else:
        print 'Ready - %s!' % shortcutFile

    if not f.isExist(shortcutFolder):
        print '%s not found. Shortcut wont be updated!' % shortcutFolder
    else:
        print 'Ready - %s!' % shortcutFolder

    processFreshCopy = not f.isExist(lclAppFile)
    processUpdate = f.isExist(lclAppFile)

    print 'Process: %s' % ('fresh copy' if processFreshCopy and not processUpdate else 'update')

    #Step2 - Call Preprocessing function
    #preprocess()

    #Step3 - Update check
    sameFile = 1
    if processUpdate and not processFreshCopy:
        #sameFile = f.isSame(srvReleaseLog, lclReleaseLog)
        installedVersion = doGetInstalledVerison()
        serverVersion = doGetServerVersion()
        sameFile = installedVersion == serverVersion


    #Step4 - Copy data files
    if not sameFile or processFreshCopy or 1:
        print 'Copying files!'
        f.iaCopyFolder(srvFolder,lclFolder)

    #Step5 - Copy shortcut files
        f.iaCopyFile(shortcutFile,shortcutFolder)
    else:
        print 'No need to copy files!'


    #Step6 - Call Postprocess function
    #postprocess()

    #Step7 - Launch Application
    #if f.isExist(lclAppFile) and f.isExist(lclFolder):
    #    f.executeApp(lclFolder, lclAppFile, 1)

    #print sp
    print 'Copy Process Completed Successfully!!!'
    print 'Use the shortcut or dock to launch the application!!!'


