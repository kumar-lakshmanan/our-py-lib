import urllib2
import urllib
import pyparsing
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



param = {
            'username':'lkumaresan',
            'password':'lkumaresan',
            'max_file_size':5000000,
            'bug_id':227,
            'file':open('D:\kdkk.txt','rb')
        }


#Login
url = 'http://mantis/login.php'
lines = urlData(url,param)

#Upload File
params, header = multipart_encode(param)
url2 = 'http://mantis/bug_file_add.php'
lines = urlData(url2,params,header)
toHtml(lines)


