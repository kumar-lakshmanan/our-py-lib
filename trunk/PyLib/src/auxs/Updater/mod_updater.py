import sys
import os
import console
import PyInterface
from PyQt4 import QtGui

def runUpdater(arg):
    installMod = arg[0] if len(arg)>0 else ''
    autoStart = arg[1] if len(arg)>1 else ''
    autoStart = int(autoStart) if autoStart.isdigit() else 1
    if installMod:
        windowTitle = 'INSTALL %s' % str(installMod).upper()
        app=QtGui.QApplication(arg)
        ui = console.Console()
        ui.chkClose.setChecked(autoStart)
        ui.setWindowTitle(windowTitle)
        _doCoreInstall(installMod)
        ui.btnClose.setEnabled(1)
        if ui.chkClose.isChecked():
            _doStartApp(installMod)
            ui.close()
            sys.exit(0)
        app.exec_()
    else:
        print 'No Install module found %s ' % installMod


def runApp(arg):
    installMod = arg[0] if len(arg) else ''
    if installMod:
        _doStartApp(installMod)
    else:
        print 'No Install module found %s ' % installMod

def runSilentUpdater(arg):
    installMod = arg[0] if len(arg)>0 else ''
    autoStart = arg[1] if len(arg)>1 else ''
    autoStart = int(autoStart) if autoStart.isdigit() else 1
    if installMod:
        _doCoreInstall(installMod)
        if autoStart:
            _doStartApp(installMod)
    else:
        print 'No Install module found %s ' % installMod

def isInstalled(arg):
    installMod = arg[0] if len(arg) else ''
    if installMod:
        _isInstalled(installMod)
    else:
        print 'No Install module found %s ' % installMod

def getCurrentVersion(arg):
    installMod = arg[0] if len(arg) else ''
    if installMod:
        _doGetVersion(installMod, 1)
    else:
        print 'No Install module found %s ' % installMod

def getLocalVersion(arg):
    installMod = arg[0] if len(arg) else ''
    if installMod:
        _doGetVersion(installMod, 2)
    else:
        print 'No Install module found %s ' % installMod


def getConfigInfo(arg):
    installMod = arg[0] if len(arg)>0 else ''
    config = arg[1] if len(arg)>1 else ''
    if installMod and config:
        _doGetConfigInfo(installMod, config)
    else:
        print 'No Install module found %s ' % installMod

def isRecentVersion(arg):
    installMod = arg[0] if len(arg)>0 else ''
    version = arg[1] if len(arg)>1 else ''
    if installMod:
        print _doCheckIsRecentVersion(installMod, version)
    else:
        print 'No Install module found %s ' % installMod

def _isInstalled(module):
    try:
        mod = __import__(module,globals(),locals())
        print mod.doIsInstalled()
    except:
        print 'process error: %s ' % PyInterface.errorReport()

def _doGetConfigInfo(module, config):
    try:
        mod = __import__(module,globals(),locals())
        print mod.doGetConfigInfo(config)
    except:
        print 'process error: %s ' % PyInterface.errorReport()

def _doGetVersion(module, loc):
    try:
        mod = __import__(module,globals(),locals())
        if loc==1:
            mod.doGetServerVersion()
        else:
            mod.doGetInstalledVerison()
    except:
        print 'process error: %s ' % PyInterface.errorReport()

def _doCheckIsRecentVersion(module, version):
    try:
        mod = __import__(module,globals(),locals())
        return mod.doCheckIsRecentVersion(version)
    except:
        print 'process error: %s ' % PyInterface.errorReport()

def _doCoreInstall(module):
    mod = None
    try:
        mod = __import__(module,globals(),locals())
        mod.doCopy()
    except:
        print 'process error: %s ' % PyInterface.errorReport()

def _doStartApp(module):
    mod = None
    try:
        mod = __import__(module,globals(),locals())
        mod.doStartApplication()
    except:
        print 'process error: %s ' % PyInterface.errorReport()

