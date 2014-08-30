import software_versioning as sv
import PyClient as pycl
import quickutils as qk
import os,sys
from PyQt4 import QtCore, QtGui

class VersionClient(object):

    def __init__(self, parentUi, appName='', appVersionXml='', pyServer='K:\Simulate\ZServer\PyServer\PyServer.exe'):
        self.parent = parentUi
        self.pyServer = pyServer
        self.appXml = appVersionXml
        self.appName = appName
        self.dispAppName = appName.upper().replace('_', ' ')

        if not (parentUi and appName and pyServer and os.path.exists(pyServer) and os.path.isfile(pyServer) and
            appVersionXml and os.path.exists(appVersionXml) and os.path.isfile(appVersionXml)):
            print '\n\nProblem getting pulse server or ReleaseLog.xml\n\n'
            self.parent = ''
            self.pyServer = ''
            self.appXml = ''
            self.appName = ''
            self.dispAppName = ''
            return None

    def __getXMLVersionNo(self):

        try:
            s = sv.versioning(self.appXml,self.appName)
            v = s.getRecentVersion()
        except:
            print 'Problem reading version info from appXml'
            print qk.errorReport()
            v = []
        return ''.join(v)

    def isUpdateReady(self, versionNo=''):
        if not versionNo or versionNo.upper()=='NONE':
            versionNo = self.__getXMLVersionNo()
        if versionNo and versionNo.isdigit():
            try:
                cl = pycl.PythonClient(self.pyServer)
                args = ['mod_updater', 'isRecentVersion', self.appName, versionNo]
                res = cl.runServerGetData(args)
                status = len(res)==3 and res[1]=='True'
                if res[0]=='process error:':
                    print 'PyServer Execution Error! Might be no server side configured!'
                    return False
                print 'No update ready!' if status else 'Update ready!'
                return not status
            except:
                print 'Problem finding recent version from server'
                print qk.errorReport()
        else:
            print 'No versionNo given for the application!'
        return False

    def doUpdate(self, silent=1):
        try:
            cl = pycl.PythonClient(self.pyServer)
            args = ['mod_updater', 'runSilentUpdater' if silent else 'runUpdater', self.appName]
            res = cl.runServer(args)
        except:
            print 'Problem updating!'
            print qk.errorReport()


    def doUpdateCheck(self):
        status = 0
        if os.path.exists(self.appXml):
            try:
                status = self.isUpdateReady()
            except:
                print qk.errorReport()

            if status:
                print 'New update found!'
                self.doUpdate()
                self.parent.close()
                sys.exit(10001)
            return status
        else:
            print 'No ReleaseVersionLog found!'
            return status

    def getRecentVersionLog(self):
        try:
            s = sv.versioning(self.appXml,self.appName)
            v = s.getRecentVersion(1)
        except:
            print 'Problem reading version info from appXml'
            print qk.errorReport()
        return v

    def getVersionLog(self):
        try:
            s = sv.versioning(self.appXml,self.appName)
            v = s.getVersions()
            for lst in v:
                print lst
        except:
            print 'Problem reading version info from appXml'
            print qk.errorReport()
        return v


    def getFormattedLog(self):
        lst = []
        try:
            s = sv.versioning(self.appXml,self.appName)
            lst = s.getVersions()
        except:
            print 'Problem reading version info from appXml'
            print qk.errorReport()

        info = ''
        info += '\n%s - Release Log' % self.dispAppName
        info += '\n---------------------------------------------------\n\n'
        for vr in lst:
            date = '%s-%s-%s' % (str(vr[5])[0:4], str(vr[5])[4:6], str(vr[5])[6:8])
            info += '\nVersion: %s.%s.%s' % (str(vr[0]).zfill(1),str(vr[1]).zfill(2),str(vr[2]).zfill(3))
            info += '\nBuild No: %s \tDate: %s' % (str(vr[3]).zfill(4), date)
            info += '\n\nChanges:'
            for log in vr[8]:
                info += '\n* %s' % log
            info += '\n-------------------------------------------------\n'
        return info

    def showReleaseLog(self):
        self.tb = QtGui.QTextBrowser()
        data = self.getFormattedLog()
        self.tb.setText(data)
        self.tb.resize(500,500)
        self.tb.show()

    def showAbout(self):
        vr = self.getRecentVersionLog()
        info = self.dispAppName
        info += '\nVersion: %s.%s.%s' % (str(vr[0]).zfill(1),str(vr[1]).zfill(2),str(vr[2]).zfill(3))
        return info
