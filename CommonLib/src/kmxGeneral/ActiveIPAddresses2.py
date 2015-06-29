#-------------------------------------------------------------------------------
# Name:        module1
#
# Author:      lkumaresan
#
# Created:     05/10/2010
# Copyright:   (c) lkumaresan 2010
# Licence:     Personal
#
# Description:
#
#
#
#-------------------------------------------------------------------------------
#!/usr/bin/env python


import os
import sys

##Remove cached custom modules from memory except preloaded IDE modules
if __name__ == '__main__':
    if globals().has_key('InitialModules'):
         for CustomModule in [Module for Module in sys.modules.keys() if Module not in InitialModules]:
            del(sys.modules[CustomModule])
    else:
        InitialModules = sys.modules.keys()

#Global Lib
import time
import base64
import commandLine
from threading import Thread
import threading


class AIPThread(Thread):

    def __init__(self, ip, callback):

        Thread.__init__(self)

        self.ip = ip
        self.status = -1
        self.callback = callback
        self.done = False

    def run(self):

        cmd = "ping -n 1 " + self.ip
        #print '\n' + str(cmd)
        pingexe = os.popen(cmd, "r")
        status = 0 		#running but no response yet
        while True:
            line = pingexe.readline()
            if not line:		# if done pinging
            	break
            if line.find(self.ip) and line.find("Reply") > -1: # they exist:
        	   status = 1 # 2=Active

        time.sleep(1)
        self.status = status
        self.done = True
        self.callback(self)
        print 'after'
        exit()



class ActIPs():

    def __init__(self, callBack, ipPrefixes = ['192.168.20.*', '192.168.21.*']):

        self.callBack  = callBack
        self.__allIPs = []

        for IPPrefix in ipPrefixes:
            lastDot = IPPrefix.find('*')
            if lastDot>0:
                for host in range(0,255):
                	self.__allIPs.append(IPPrefix[0:lastDot]+str(host))
            else:
                	self.__allIPs.append(IPPrefix)

        print '\nIps Ready!'

    def ipCount(self):
        return len(self.__allIPs)

    def refreshIPs(self):
        print '\nStarting Threads'
        for ip in self.__allIPs:
            thread = AIPThread(ip, self.__threadEndCallBack)
            thread.start()

    def __threadEndCallBack(self, node):
        if node.isAlive() and node.done:
            ip = node.ip
            status = node.status
            del(node)
            self.callBack([ip, status])
            sys.exit(0)

    def tCount(self):
        return threading.activeCount()


if __name__ == '__main__':

    global n
    n = 0

    def IPListDisplay(arg):
        global n
        ttl = app.ipCount()
        n += 1
        print '\n\nResponse: %s - (%s/%s)' % (str(arg),n,ttl)

    ips = ['192.168.20.*']
    app = ActIPs(IPListDisplay,ips)
    app.refreshIPs()


    print 'End!'