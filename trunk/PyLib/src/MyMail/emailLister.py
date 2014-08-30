import urllib2
import urllib
import pyparsing
import socket
import httplib
import cookielib
cj = cookielib.CookieJar()

redirect = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(redirect)
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib2.install_opener(opener)
socket.setdefaulttimeout(30)

def getBoldUrls(lines=[],sub=0):
    abstart,abend = pyparsing.makeHTMLTags('B')
    grammer2 = abstart + pyparsing.SkipTo(abend) + abend.suppress()
    for x1,x2,x3 in grammer2.scanString(''.join(lines)):
        print x1
        print x2
        print x3

def getUrls(lines=[],sub=0):
    grammer = ''
    astart,aend = pyparsing.makeHTMLTags('a')
    grammer = astart + pyparsing.SkipTo(aend) + aend.suppress()
##    grammer2 = abstart + pyparsing.SkipTo(abend) + abend.suppress()
##    for x1,x2,x3 in grammer.scanString(''.join(lines)):
##        print x1
##        print x2
##        print x3



    urls = []
    for x1,x2,x3 in grammer.scanString(''.join(lines)):
        if sub:
            if len(x1)==6:
                mailreadstatus = 1 if str(x1[1]).find('db_chkstatus=1')>0 else 0
                mailsubject = str(x1[5])
                maillink = str(x1[1][1])
                nxtSender=True
            if len(x1)==5 and nxtSender:
                mailsender = ''
                if dict(x1).has_key('title'):
                    mailsender = str(x1['title']).replace('Search ','')
                    nxtTime=True
                    nxtSender=False
            if len(x1)==4 and nxtTime:
                mailtime = x1[3]
                urls.append([mailsubject,mailreadstatus,mailsender,mailtime,maillink])
                nxtSender=False
                nxtTime=False
                mailreadstatus=0
                mailsubject = ''
                mailsender=''
                mailtime = ''
                maillink = ''

        else:
            urls.append(str(x1[1][1]))
            nxtSender=False
            nxtTime=False
    return urls

##
##def getEmails(lines=[]):
##    grammer = ''
##    astart,aend = pyparsing.makeHTMLTags('a')
##    grammer = astart + pyparsing.SkipTo(aend) + aend.suppress()
##    urls = []
##
##    Sub = ''
##    for x1,x2,x3 in grammer.scanString(''.join(lines)):
##
##        if len(x1)==5:
##            if checkInLine(x1[4],'Search Address book'):
##                sender =
##
##        print x1[4] if len(x1)==5 else ''
##        if len(x1)==6:
##            urls.append(str(x1[5]))
##
##    return urls
##
##


def getNonUrls(lines):
    Subjects=[]
    for eachLine in lines:
        if not eachLine[0].find('IMG SRC')>=0:
            Subjects.append([eachLine[0],eachLine[1],eachLine[2],eachLine[3],eachLine[4]])
    return Subjects

def urlData(link,param=''):

    if param:
        req = urllib2.Request(link, data=urllib.urlencode(param))
    else:
        req = urllib2.Request(link)

    data = opener.open(req)
    allline = data.read()
    lines = allline.split('\n')
    return lines

def checkInLine(lines,text):
    ret = False
    for eachLine in lines:
        if eachLine.find(text)>=0:
            ret = True
    return ret














def listMails(login, password):

    param = {
                "loginname":login,
                "password":password
            }


    url = 'http://mail/cgi-bin/openwebmail/openwebmail.pl'

    lines = urlData(url,param)

    if checkInLine(lines, 'Password incorrect!'):
        print 'Password Error!'
    else:
        print 'Proceeding'
        urls = getUrls(lines)
        nextLink = 'http://mail' + urls[0]
        lines = urlData(nextLink)
        urls = getUrls(lines,1)
        return getNonUrls(urls)

    return []











##
##url = 'http://mail/cgi-bin/openwebmail/openwebmail.pl'
##
##passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
##passman.add_password(None,url,'lkumaresan','lkumaresan')
##auth= urllib2.HTTPBasicAuthHandler(passman)
##openr = urllib2.build_opener(auth)
##urllib2.install_opener(openr)
##page = urllib2.urlopen(url)
##print page.read()
##




