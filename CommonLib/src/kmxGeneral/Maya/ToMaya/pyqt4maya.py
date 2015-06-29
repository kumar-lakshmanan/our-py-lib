import os
import sys

def isExecInMaya():
    '''
    Returns True if app running inside maya else False
    '''
    modules = sys.modules.keys()
    if 'maya' in modules and 'maya.cmds' in modules:
        import maya.cmds as cmds
        res = cmds.about(a=True)
        return res=='maya'
    return False

def getMayaWindowWidget():
    if isExecInMaya() and '2011' in getMayaVersion():
        from PyQt4 import QtCore
        import sip
        import maya.OpenMayaUI as mui
        ptr = mui.MQtUtil.mainWindow()
        return sip.wrapinstance(long(ptr), QtCore.QObject)
    else:
        return None

def getMayaVersion():
    '''
    Returns maya version
    eg:
        2008 Extension 2, 2011
    '''
    if isExecInMaya():
        import maya.cmds as cmds
        res = cmds.about(v=True)
        return res
    return ''

def getMayaArch():
    '''
    Returns 64 or 32
    '''
    if isExecInMaya():
        import maya.cmds as cmds
        return '64' if cmds.about(is64=True) else '32'

def get32BitLib():
    path = 'Z:/REPO/SOURCE/APPS/pyqt/32Bit'
    path = os.path.normpath(path) if path and os.path.exists(path) else ''
    if path not in sys.path: sys.path.append(path)
    return isPyQt4Ready()

def get64BitLib():
    path = 'Z:/REPO/SOURCE/APPS/pyqt/64Bit'
    path = os.path.normpath(path) if path and os.path.exists(path) else ''
    if path not in sys.path: sys.path.append(path)
    return isPyQt4Ready()

def get2011Lib():
    path = 'Z:/REPO/SOURCE/APPS/pyqt/maya2011'
    path = os.path.normpath(path) if path and os.path.exists(path) else ''
    if path not in sys.path: sys.path.append(path)
    return isPyQt4Ready()

def getPyQtLib():
    if isExecInMaya():
        if '2011' in getMayaVersion():
            get2011Lib()
        else:
            if getMayaArch()=='64':
                get64BitLib()
            else:
                get32BitLib()
    return isPyQt4Ready()

def isPyQt4Ready():
    try:
        from PyQt4 import QtGui
        ready=1
    except:
        ready=0
    return ready

pmth=None
app=None
def pumpThread():
    global pmth
    global app
    if not pmth:
        import threading
        rapp = QtGui.QApplication(sys.argv)
        pmth=threading.Thread(target=__pumpQt,args=())
        pmth.start()

def __pumpQt():
    import maya.utils as utils
    import time
    global app
    while 1:
        time.sleep(0.01)
        utils.executeDeferred(app.processEvents)
