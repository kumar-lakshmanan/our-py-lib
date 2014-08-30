#Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    import sys
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()
import sys
import os
#Search Paths...
currentFolder = os.getcwd()
parentFolder = os.path.dirname(currentFolder)
modulePathList = [
                 parentFolder,
                 currentFolder,
                 parentFolder   + '/Common/pyServersLib/Common',
                 ]

for modulePath in modulePathList:
    modulePath = os.path.normpath(modulePath)
    if modulePath not in sys.path and os.path.exists(modulePath):
        sys.path.append(modulePath)
import software_versioning as sv





xmlFile = 'ReleaseLog.xml'
appName = 'lnp'
rtype = 2

log = [
      'New app version system',
      'Work Version download/open/modified'
      ]


##            rtype         1   -   for Major release
##                          2   -   for Minor release
##                          3   -   for Patch release
##                          4   -   for incremental release


s = sv.versioning(xmlFile,appName)
if s and 0<rtype<5 and log:
    if s.releaseNewVersion(rtype,log):
        print 'New version added!'
        print s.getRecentVersion()
    else:
        print 'Not updated!'
        print s.getRecentVersion()
else:
    print s.getRecentVersion()
    print 'Invalid ReleaseType'