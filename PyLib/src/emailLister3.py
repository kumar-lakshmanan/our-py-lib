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
param = {
            "loginname":"lkumaresan",
            "password":"lkumaresan"
        }


def getUrls(lines=[],sub=0):
    grammer = ''
    astart,aend = pyparsing.makeHTMLTags('a')
    grammer = astart + pyparsing.SkipTo(aend) + aend.suppress()
    urls = []
    for x1,x2,x3 in grammer.scanString(''.join(lines)):
        if sub:
            if len(x1)==5:
                print x1[4]
            if len(x1)==6:
                urls.append(str(x1[5]))
        else:
            urls.append(str(x1[1][1]))

    return urls


def getEmailUrls(lines=[]):
    grammer = ''
    astart,aend = pyparsing.makeHTMLTags('a')
    grammer = astart + pyparsing.SkipTo(aend) + aend.suppress()
    urls = []
    for x1,x2,x3 in grammer.scanString(''.join(lines)):
        if len(x1)==5:
            urls.append(x1[4])


    for eachUrls in urls:
        if eachUrls.find('alt="Search ')>0:
            data = eachUrls[eachUrls.find('alt="Search ')+len('alt="Search '):len(eachUrls)-2]
            print data

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
        if not eachLine.find('IMG SRC')>=0:
            Subjects.append(eachLine)
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
    urls = getEmailUrls(lines)
##    for eachEmail in getNonUrls(urls):
##        print eachEmail











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




