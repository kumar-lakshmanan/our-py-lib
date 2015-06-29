import sys
import os

##Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()

uid = 'lkumaresan'



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
                      rootFolder + '\lib',
                      rootFolder + '\lib\controls',
                      rootFolder + '\ui',
                      rootFolder + '\ui\common',
                      rootFolderParent  + '\UI_DB_lib'
                      'D:\REPO\SOURCE\SCRIPTS\PYTHON\PULSE_GREEN\lib\controls'
                     ]

    for modulePath in modulePathList:
        if modulePath not in sys.path:
            if os.path.exists(modulePath):
                sys.path.append(modulePath)


ps = uid
import urllib2,urllib
import socket
import cookielib

class HyperTextAgent(object):

    def __init__(self):
        self.cookie = cookielib.CookieJar()
        self.redirector = urllib2.HTTPCookieProcessor(self.cookie)
        self.opener = urllib2.build_opener(self.redirector)
        self.opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib2.install_opener(self.opener)
        socket.setdefaulttimeout(30)

    def urlOpen(self, url, paramDict={}):

        req = urllib2.Request(url, data=urllib.urlencode(paramDict)) if paramDict else urllib2.Request(url)
        data = self.opener.open(req)
        allline = data.read()
        return allline

    def test_toHtml(self,data):
        f = open('d:/result.html','w')
        f.write(str(data))
        f.close()

def getRoot(agent, url,param={}):

    data = hp.urlOpen(url,param)
    toHtml(data)
    root = etree

    doc = html.fromstring(data)
    root = doc.getroottree()
    return root

def toHtml(data=''):
    f = open('d:/result.html','w')
    f.write(str(data))
    f.close()

def FindTable(root, SearchText = 'Assigned to Me (Unresolved)'):

    tables = cssselect.CSSSelector('table table')
    rowAndAncors = cssselect.CSSSelector('tr a')
    for table in tables(root):
        for ancor in rowAndAncors(table):
            if ancor.text == str(SearchText):
                return table

def nodeInfo(node):
    print 'Attribute: ' + str(node.attrib)
    print 'Tag: ' + str(node.tag)
    print 'Text: ' + str(node.text)
    try:
        print 'TextContent: \n'
        print node.text_content()
        print '\n'
    except: pass
    print 'Value: ' + str(node.values())
    print 'Keys: ' + str(node.keys())

def TableRows(table):
    rows = cssselect.CSSSelector('tr')(table)
    tableInfo = []
    for eachRow in rows:
        ancors = cssselect.CSSSelector('a')(eachRow)
        ancor = ancors[0] if len(ancors)>=1 else ''
        tds = cssselect.CSSSelector('td')(eachRow)
        td = tds[1] if len(tds)==2 else ''

        Link = str(ancor.attrib['href']).strip() if str(ancor) else None
        Title = (str(ancor.attrib['title']).strip() if ancor.attrib.has_key('title') else None) if str(ancor) else None
        MainInfo =  str(td.text).strip() if str(td) else None
        if Title:
            tableInfo.append([MainInfo,Title,Link])

    return tableInfo


def BugNotes(root):
    rows = cssselect.CSSSelector('div table tr')(root)
    bugNotes = []
    for eachRow in rows:
        attribs = eachRow.attrib
        if attribs.has_key('class'):
            for eachAttr in attribs:
                if attribs[eachAttr] == 'bugnote':
                #BugNotes alone
                    tds = cssselect.CSSSelector('td')(eachRow)
                    if len(tds)==2:
                        bugNotes.append((tds[0],tds[1]))
    return bugNotes

def BugNoteInfo(BugNotesNode):

    noteHead = TextContent(BugNotesNode[0])
    noteContent = TextContent(BugNotesNode[1])
    noteHead = noteHead.replace('\n\t\t\t\t',' | ')
    noteHead = noteHead.replace('\n\t\t',' | ')
    noteHead = noteHead.replace('\t\t',' | ')
    return (noteHead, noteContent)

def lastBugNote(bugPageUrl='view.php?id=275'):
    url = baseUrl + bugPageUrl
    root = getRoot(hp, url)
    bugNode = BugNotes(root)
    info = BugNoteInfo(bugNode[len(bugNode)-1])
    print info[0]
    print info[1]

def TextContent(node):
    try:
        data = str(node.text_content()).strip().replace('\r','')
    except:
        print 'Spl Characters'
        data = ''
    return data


from lxml import *
from lxml import etree
from lxml import html
from lxml import cssselect
baseUrl = 'http://mantis/'
hp = HyperTextAgent()


url = baseUrl + 'login.php'
param = {"username":uid, "password":ps}
root = getRoot(hp, url,param)

print '\nAssigned to me: '
print '------------------'
assignedToMeTable = FindTable(root,'Assigned to Me (Unresolved)')
info = TableRows(assignedToMeTable)

for eachRow in info:
    print
    print eachRow[1]
    print '---------------------------------------------------------------'
    print
    lastBugNote(eachRow[2])
    print







##print '\nAssigned to me: '
##print '------------------'
##assignedToMeTable = FindTable(root,'Assigned to Me (Unresolved)')
##info = TableRows(assignedToMeTable)
##
##for eachRow in info:
##    print eachRow[1]



##print '\nReported by me: '
##print '------------------'
##reportedByMeTable = FindTable(root,'Reported by Me')
##info = TableRows(reportedByMeTable)
##
##for eachRow in info:
##    print eachRow[1]
##


##url = baseUrl + 'view.php?id=275'
##root = getRoot(hp, url)
##bugNode = BugNotes(root)
##for eachBugNode in bugNode:
##    print BugNoteInfo(eachBugNode)
##



##
##

##
##
##
##
##
##
##
##
##print '\nResolved: '
##print '------------------'
##reportedByMeTable = FindTable(root,'Resolved')
##info = TableRows(reportedByMeTable)
##
##for eachRow in info:
##    print eachRow[1]








































##