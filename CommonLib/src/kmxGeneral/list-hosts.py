#!/usr/bin/env python
##Copyright (C) 2010 Louis Taylor
## _    ___ _____
##| |  | _ \_   _|
##| |__|  _/ | |
##|____|_|   |_| *programus optimus est*
##This program is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program.  If not, see http://www.gnu.org/licenses/
import os, sys, re

class connected:
    '''
    class for looking at the connected machines on the network.
    Can give the same output available on the network router

    Must be run under root, this is necessary because of nmap
    depends on:
    * nmap
    * python 2.6
    * ping
    '''
    def __init__(self):
        self.ipregex = re.compile('\(.*?\)')
        self.hostregex = re.compile('Host\.*is up')

        self.cmd = 'nmap -sP 192.168.1.1-255'

        self.peopleConnected = []
        self.ipConnected = []
        self.MACConnected = []

        self.database = []
        self.current = 0

##        if not os.getuid() == 0:
##            #raise Exception, 'must be run as root' #uncomment and use this if you want
##                                                    #it to be run as part of a larger
##                                                    #program
##            print 'must be run as root'
##            sys.exit(1)
##        else:
##            pass

    def output(self, cmd):
        '''outputs the text from cmd'''
        self.outputtext=os.popen(cmd).read().split('\n')
        return self.outputtext

    def refresh(self):
        '''refreshes the list of machines connected to the network
        You must call this function every time you expect the values to change
        and want to read these changes'''

        ishost = False
        hasMAC = True

        for line in self.output(self.cmd):
            splitline = line.split(' ')
            if splitline[0] == 'Host':
                if not hasMAC:
                    self.MACConnected += ['unknown']

                self.peopleConnected += [splitline[1].replace('.home', '')]
                ipAddress = self.ipregex.search(line)
                self.ipConnected += [ipAddress.group().replace('(', '').replace(')', '')]

                ishost = True
                hasMAC = False

            #check if the line begins with 'MAC' and is after a host line
            elif ishost and splitline[0] == 'MAC':
                brackets = self.ipregex.search(line)
                brackets = brackets.group()
                line = line.replace(brackets, '').replace('MAC Address: ', '')
                self.MACConnected += [line]
                hasMAC = True
                ishost = False
        current = -1
        self.database = []

        for name in self.peopleConnected:
            current += 1
            self.database.append(name)
            self.database.append([self.ipConnected[current], self.MACConnected[current]])

    def ip(self, name):
        '''returns the ip address of the given computer name
        returns 000.000.000.000 if none found e.g. computer not connected'''
        try:
            index = self.database.index(name)+1 #get the index of the item
                                                #add 1 to get to the next index
        except ValueError:
            return '000.000.000.000'
        return self.database[index][0]

    def mac(self, name):
        '''returns the MAC address of the given computer name
        returns 00:00:00:00:00:00 if none found e.g. computer not connected'''
        try:
            index = self.database.index(name)+1 #get the index of the item
                                                #add 1 to get to the next index
        except ValueError:
            return '00:00:00:00:00:00'
        return self.database[index][1]

    def os(self, name):
        '''will try to find the name and version of the os that the ip is running.
        v. slow, so run in multithreaded or prepare for a freeze
        * name can be an ip address or the bssid

        Warning! this function does not work, do not use'''

        cmd = 'sudo nmap -O %s' % name
        output = self.output(cmd)

    def up(self, ip):
        '''returns True if the ip address replies to a ping request'''
        cmd = 'ping -q -c 1 %s' % ip
        output = os.popen(cmd).read()
        if 'ping: unknown host' in output:
            #trys to see if the ip address entered is invalid.
            return False
        elif '1 received' in output:
            #try to see if the computer has receved any packets.
            return True
        else:
            #return false because there is nothing else to do if the
            #output is in a different format than usual.
            return False

    def names(self):
        '''returns the names of the computers connected to the network'''
        return self.peopleConnected

if __name__ == '__main__':
    '''small self test/example of use'''
    people = connected()
    people.refresh()
    for name in people.names():
        print name
        print '... MAC:', people.mac(name)
        print '... ip:', people.ip(name)