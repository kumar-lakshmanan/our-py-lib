import urllib2
import urllib
import pyparsing
import socket
import httplib

socket.setdefaulttimeout(30)
param = {
            "loginname":"lkumaresan",
            "password":"lkumaresan",
            '.cgifields':'httpcompress=1'
        }
















def getUrls(lines=[]):

    grammer = ''

    astart,aend = pyparsing.makeHTMLTags('a')
    grammer = astart + pyparsing.SkipTo(aend) + aend.suppress()

    urls = []
    for x1,x2,x3 in grammer.scanString(''.join(lines)):
        urls.append(str(x1[1][1]))
    return urls


def urlData(link,param=''):


    if param:
        urldata = urllib.urlencode(param)
        data = urllib.urlopen(link,urldata)
        allline = data.read()
    else:
        #data = urllib2.urlopen(str(link))
##        req = urllib2.Request(str(link))
##        data = urllib2.urlopen(req)
##        allline = data.read()
##        url = link

        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None,url,'lkumaresan','lkumaresan')
        auth= urllib2.HTTPBasicAuthHandler(passman)
        openr = urllib2.build_opener(auth)
        urllib2.install_opener(openr)
        page = urllib2.urlopen(url)
        allline = page.read()

    lines = allline.split('\n')
    return lines

def checkInLine(lines,text):
    ret = False
    for eachLine in lines:
        if eachLine.find(text)>=0:
            ret = True
    return ret



import cookielib
cj = cookielib.CookieJar()


ur = 'http://mail/cgi-bin/openwebmail/openwebmail.pl'
ur2 = 'http://mail/cgi-bin/openwebmail/openwebmail.pl'
#ur2 = 'http://mantis/my_view_page.php'
#ur2 = 'http://mantis/login_page.php'
##
redirect = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(redirect)
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib2.install_opener(opener)

req = urllib2.Request(ur2,data=urllib.urlencode(param))
res = opener.open(req)
cookie = res.headers.getheader('Set-Cookie')
sesid = cookie[cookie.index('=')+1:cookie.index(';')]
header = {'Cookie':'session_id='+sesid}

req = urllib2.Request(ur2,headers =header, data=urllib.urlencode(param))
res = opener.open(req)
data = res.read()
urls = getUrls(data)
nextLink = 'http://mail' + urls[0]
print nextLink
##import webbrowser
##webbrowser.open(nextLink)

print opener.open(nextLink).read()
#print urllib2.urlopen(nextLink).read()




##cookie = urllib2.urlopen(ur2).headers.getheader('Set-Cookie')
##sess = cookie[cookie.index('=')+1:cookie.index(';')]
##head = {'Cookie':'session_id='+sess}
##
##k = urllib2.urlopen(urllib2.Request)
##
####
##opener = urllib2.build_opener()
##opener.addheaders = [('User-agent', 'Mozilla/5.0')]
##f = opener.open(ur2)
##
##urllib2.Request(ur2, param)
##

##urx = 'http://mantis/my_view_page.php'
##
##import httplib, urllib
##params = urllib.urlencode(param)
##headers = {"Content-type": "application/x-www-form-urlencoded",
##            "Accept": "text/plain"}
##conn = httplib.HTTPConnection("mail:80")
##conn.request("POST", "/cgi-bin/openwebmail/openwebmail-main.pl", params, headers)
##response = conn.getresponse()
##print response.status, response.reason
##data = response.read()
##print data
##conn.close()



##ur = 'mail:80'
##urlenc = urllib.urlencode(param)
##head = {'Content-type':'application/x-www-form-urlencoded','Accept':'text/plain'}
##
##con = httplib.HTTPConnection(ur)
##con.request('POST','/cgi-bin/openwebmail/openwebmail-main.pl',urlenc,head)
##res = con.getresponse()
##print res.read()
##con.close()
##









##if checkInLine(lines, 'Password incorrect!'):
##    print 'Password Error!'
##else:
##    print 'Proceeding'
##    urls = getUrls(lines)
##    nextLink = urls[1].rstrip('/') + urls[0]
##    lines = urlData(nextLink)
##    print lines










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




