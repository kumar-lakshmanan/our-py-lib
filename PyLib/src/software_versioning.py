import XMLReadWrite
import os
from time import strftime

##class versionNode(object):
##
##    def __init__(self):
##        self.build=0
##        self.majorVno=0
##        self.minorVno=0
##        self.patchVno=0
##        self.releaseDate=20110101
##        self.releaseMachine=''
##        self.releasePerson=''
##        self.majorChangesLog=[]
##        self.minorChangesLog=[]
##        self.patchesLog=[]


##class newVersion(object):
##
##    def __init__(self):
##        self.releaseMajor=0
##        self.releaseFeature=0
##        self.releasePatch=0
##        self.majorChangesLog=['Some major features included in this version.']
##        self.minorChangesLog=['Some minor features included in this version.']
##        self.patchesLog=['Some patches included in this version.']


class versioning(object):

    def __init__(self, versionXml, appName='PULSE'):
        '''
        This class is for maintaining version information about the software and to maintain release and change log.
        specify the XMLfile in which change log will be maintained.
        appName is optional. Will be used only if you are creating new versioningXMLfile

        Important funcitons:

            - releaseNewVersion(releaseType, changeLogList)
            for releasing a new version, mention what type of release it is and list of changes made in it

            - getVersions()
            gives you all version information along with the changelog

            - getRecentVersion()
            gives you recent version information along with the changelog

            - getRecentBuild()
            gives you recent buildId

        '''

        self._appName = appName
        self._xmlFile = versionXml
        self._xml = XMLReadWrite.XMLRW(self._appName)
        self._machinName=os.environ.get('COMPUTERNAME')
        self._userName=os.environ.get('USERNAME')
        self._mode = 'a' if os.path.exists(self._xmlFile) else  'w'
        if self._mode=='a':
            self._xml.loadFile(self._xmlFile,self._appName)
        self._root = self._xml.getRoot()


    def isReady(self):
        return os.path.exists(self._xmlFile)

    def releaseNewVersion(self, releaseType, changeLog=[]):
        '''
        releaseType:
            It can be   1   -   for Major release
                        2   -   for Minor release
                        3   -   for Patch release
                        4   -   for incremental release
        changeLog:
            list of strings, Listing all changes made since last release
        '''

        if releaseType==1:
            res = self._addMajorVersion(changeLog)
        if releaseType==2:
            res = self._addMinorVersion(changeLog)
        if releaseType==3:
            res = self._addPatchVersion(changeLog)
        if releaseType==4:
            res = self._addIncrement(changeLog)

        return res!=None

    def getVersions(self):
        '''
        Returns list of tuples
        [(majorVerNo, minorVerNo, patchVerNo, buildNo, releaseType, releaseData, releaseMachine, releasePerson, releaseLog)]
        '''

        versionNodes = self._xml.getNodeList(self._root)
        versionInfos = []
        for eachVersion in versionNodes:
            versionInfos.append(self._getVersionInfo(eachVersion))
        return versionInfos

    def getAppName(self):
        return str(self._root.tag)

    def getRecentVersion(self, completeInfos=0):
        '''
        Returns tuble of recent version  information

        for completeInfos == 1
        (majorVerNo, minorVerNo, patchVerNo, buildNo, releaseType, releaseData, releaseMachine, releasePerson, releaseLog)

        for completeInfos != 1
        (majorVerNo, minorVerNo, patchVerNo, buildNo)

        '''
        versionNodes = self._xml.getNodeList(self._root)
        lastVersion = versionNodes[len(versionNodes)-1] if versionNodes else None
        info = self._getVersionInfo(lastVersion)
        #info = info if lastVersion!=None else (0,0,0,0,'','','','',[])

        major = info[0]
        minor = info[1]
        patch = info[2]
        build = info[3]
        releaseType = info[4]
        releaseDate = info[5]
        releaseMachine = info[6]
        releasePerson = info[7]
        releaseLogs = info[8]

        if completeInfos:
            return (major,minor,patch,build,releaseType,releaseDate,releaseMachine,releasePerson,releaseLogs)
        else:
            return (major,minor,patch,build)

    def getPackedRecentVersion(self):
        ver = self.getRecentVersion()
        return '%s%s%s%s'%ver

    def getRecentBuild(self):
        major,minor,patch,buildId2 = self.getRecentVersion()
        return int(buildId2)

    def _addMajorVersion(self, releaseLogs):
        if not releaseLogs or type(releaseLogs)!=type([]):
            print 'No release log list provided!'
            return None
        major, minor, patch, buildId = self.getRecentVersion()
        buildId = int(buildId)+1
        releaseType=1 #1 - 'major', 2 - 'minor', 3 - 'patch', 4 - 'internal'
        releaseDate=self._getDataTime()
        releaseMachine=self._machinName
        releasePerson=self._userName
        newVersionNode = self._addVersionNode(int(major)+1,0,0,buildId,releaseType,releaseDate,releaseMachine,releasePerson,releaseLogs)
        return newVersionNode

    def _addMinorVersion(self, releaseLogs):
        if not releaseLogs or type(releaseLogs)!=type([]):
            print 'No release log list provided!'
            return None
        major, minor, patch, buildId = self.getRecentVersion()
        buildId = int(buildId)+1
        releaseType=2 #1 - 'major', 2 - 'minor', 3 - 'patch' 4 - 'internal'
        releaseDate=self._getDataTime()
        releaseMachine=self._machinName
        releasePerson=self._userName
        newVersionNode = self._addVersionNode(major,int(minor)+1,0,buildId,releaseType,releaseDate,releaseMachine,releasePerson,releaseLogs)
        return newVersionNode

    def _addPatchVersion(self, releaseLogs):
        if not releaseLogs or type(releaseLogs)!=type([]):
            print 'No release log list provided!'
            return None
        major, minor, patch, buildId  = self.getRecentVersion()
        buildId = int(buildId)+1
        releaseType=3 #1 - 'major', 2 - 'minor', 3 - 'patch' 4 - 'internal'
        releaseDate=self._getDataTime()
        releaseMachine=self._machinName
        releasePerson=self._userName
        newVersionNode = self._addVersionNode(major,minor,int(patch)+1,buildId,releaseType,releaseDate,releaseMachine,releasePerson,releaseLogs)
        return newVersionNode

    def _addIncrement(self, releaseLogs, doSave=1):
        if not releaseLogs or type(releaseLogs)!=type([]):
            print 'No release log list provided!'
            return None
        major, minor, patch, buildId = self.getRecentVersion()
        buildId = int(buildId)+1
        releaseType=4 #1 - 'major', 2 - 'minor', 3 - 'patch', 4 - 'internal'
        releaseDate=self._getDataTime()
        releaseMachine=self._machinName
        releasePerson=self._userName
        newVersionNode = self._addVersionNode(major,minor,patch,buildId,releaseType,releaseDate,releaseMachine,releasePerson,releaseLogs)
        return newVersionNode

    def _addVersionNode(self, major=0, minor=0, patch=0, buildId=0, releaseType=4, releaseDate='', releaseMachine='', releasePerson='', releaseLogs=[], doSave=1):
        newVersion = self._xml.createNode('version',self._root)
        self._xml.setAttributeVal(newVersion, 'major', str(major))
        self._xml.setAttributeVal(newVersion, 'minor', str(minor))
        self._xml.setAttributeVal(newVersion, 'patch', str(patch))
        self._xml.setAttributeVal(newVersion, 'buildId', str(buildId))
        self._xml.setAttributeVal(newVersion, 'releaseType', str(releaseType))
        self._xml.setAttributeVal(newVersion, 'releaseDate', str(releaseDate))
        self._xml.setAttributeVal(newVersion, 'releaseMachine', str(releaseMachine))
        self._xml.setAttributeVal(newVersion, 'releasePerson', str(releasePerson))
        self._addReleaseLogs(newVersion, releaseLogs)
        if doSave: self._xml.saveFile(self._xmlFile)
        return newVersion

    def _addReleaseLogs(self, newVersion, releaseLogs):
        releaseLogs = [str(releaseLogs)] if type(releaseLogs) != type([]) else releaseLogs
        for eachReleaseLog in releaseLogs:
            newLog = self._xml.createNode('log', newVersion)
            self._xml.setNodeValue(newLog, str(eachReleaseLog))

    def _getVersionInfo(self, xmlnode):
        if xmlnode!=None:
            major = self._xml.getAttributeVal(xmlnode,'major')
            minor = self._xml.getAttributeVal(xmlnode,'minor')
            patch = self._xml.getAttributeVal(xmlnode,'patch')
            build = self._xml.getAttributeVal(xmlnode,'buildId')
            releaseType = self._xml.getAttributeVal(xmlnode,'releaseType')
            releaseDate = self._xml.getAttributeVal(xmlnode,'releaseDate')
            releaseMachine = self._xml.getAttributeVal(xmlnode,'releaseMachine')
            releasePerson = self._xml.getAttributeVal(xmlnode,'releasePerson')
            releaseLog = self._getReleaseLog(xmlnode)
            return (major,minor,patch,build,releaseType,releaseDate,releaseMachine,releasePerson,releaseLog)
        else:
            return ('0','0','0','0','4','','','',[])

    def _getReleaseLog(self, xmlnode):
        logs = []
        if xmlnode != None:
            releaseLogs = self._xml.getNodeList(xmlnode)
            for releaseLog in releaseLogs:
                logs.append(self._xml.getNodeValue(releaseLog))
        return logs

    def _getDataTime(self,format = "%Y%m%d%H%M%S"):
        """
        "%Y-%m-%d %H:%M:%S"
        """
        return strftime(format)


##v = versioning('Z:/REPO/PulseServer/ProgramFiles/SHIP/ReleaseLog.xml', 'PULSEBEAT')
##print v.getAppName()
#print v.releaseNewVersion(3,['XXXXTTTTTTTTTTTXXXXXXX Nothing', 'RTYRYRTYRTY Something','EETYRTYRTYFTYEEEEEEEE Everything'])