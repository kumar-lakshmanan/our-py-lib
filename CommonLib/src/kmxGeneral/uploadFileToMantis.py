import urllib2
import urllib
import socket
import httplib
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

import cookielib
cj = cookielib.CookieJar()
cookie = urllib2.HTTPCookieProcessor(cj)
socket.setdefaulttimeout(30)
opener = register_openers()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
opener.add_handler(cookie)
urllib2.install_opener(opener)


def urlData(link,param='',splHeader=''):

    if param:
        if splHeader:
            req = urllib2.Request(link, param, splHeader)
        else:
            req = urllib2.Request(link, data=urllib.urlencode(param))
    else:
        req = urllib2.Request(link)

    data = opener.open(req)
    allline = data.read()
    lines = allline.split('\n')
    return lines

def toHtml(lines=[]):
    f = open('d:/result.html','w')
    f.write('\n'.join(lines))
    f.close()


def uploadToMantis(fileName ='', bug_id=227, userName='lkumaresan', password='lkumaresan', max_file_size=5000000):

    #Login Url
    url = 'http://mantis/login.php'
    url2 = 'http://mantis/bug_file_add.php'

    param = {
                'username':userName,
                'password':password,
                'max_file_size':max_file_size,
                'bug_id':bug_id,
                'file':open(fileName,'rb')
            }

    #Login

    lines = urlData(url,param)

    #Upload File
    params, header = multipart_encode(param)
    lines = urlData(url2,params,header)
    #toHtml(lines)
    return '\n'.join(lines)


