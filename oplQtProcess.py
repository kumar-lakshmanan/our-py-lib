#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      AIAA
#
# Created:     14-12-2011
# Copyright:   (c) AIAA 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import configobj
import oplPyUtilities

'''  self.prc = oplQtProcess.Process(self._exe,
                                self._args,
                                self._onDataComes,
                                self._onErrorComes,
                                self._onCompletion,
                                self._terminationCall)'''

from PyQt4 import QtCore, QtGui

class Process():

    def __init__(self, exe='', args=[], onDataComes=None, onErrorComes=None, onCompletion=None):

        self.prc = QtCore.QProcess()
        self._exe = exe
        self._args = self._argStringList(args)
        self._onDataCames=onDataComes
        self._onErrorComes=onErrorComes
        self._onCompletion=onCompletion

        QtCore.QObject.connect(self.prc,QtCore.SIGNAL("started ()"),self.sigStarted)
        QtCore.QObject.connect(self.prc,QtCore.SIGNAL("stateChanged (QProcess::ProcessState)"),self.sigStateChanged)
        #QtCore.QObject.connect(self.prc,QtCore.SIGNAL("readyReadStandardOutput ()"),self.sigReadStdOutput)
        QtCore.QObject.connect(self.prc,QtCore.SIGNAL("readyReadStandardError ()"),self.sigReadStdError)
        QtCore.QObject.connect(self.prc,QtCore.SIGNAL("readyRead ()"),self.sigReadStdOutput)
        #QtCore.QObject.connect(self.prc,QtCore.SIGNAL("finished (int)"),self.sigFinished)
        QtCore.QObject.connect(self.prc,QtCore.SIGNAL("finished (int,QProcess::ExitStatus)"),self.sigFinished)
        QtCore.QObject.connect(self.prc,QtCore.SIGNAL("error (QProcess::ProcessError)"),self.sigError)

    def _argStringList(self, args=[]):
        lst = QtCore.QStringList()
        for each in args:
            lst.append(each)
        return lst

    def sigStarted(self, *arg):
        #print "Started"
        pass

    def sigStateChanged(self, *arg):
        #print "StateChange - " + str(arg[0])
        pass

    def sigReadStdOutput(self, *arg):
        #print "StdOutput"
        m=self._getMainData()
        #print str(val)
        self._onDataCames(m)

    def sigReadStdError(self, *arg):
        e=self._getErrorData()
        #print "StdError"
        #print self.prc.error()
        #print self.prc.errorString()
        #byt = QtCore.QByteArray()
        #byt = self.prc.readAllStandardError()
        #print str(byt.data())
        self._onErrorComes(e)

    def sigFinished(self, *arg):
        #print "Fin"
        self._onCompletion(arg)

    def sigError(self, *arg):
        print "Error in the Process"
        pass

    def execute(self):
        print "Starting..."
        print self._exe + " " + self.__argsDisp()
        r = self.prc.start(self._exe, self._args, QtCore.QIODevice.ReadWrite|QtCore.QIODevice.Text)
        #r = self.prc.startDetached(self.exe, self.lst)
        #r = self.prc.execute(self.exe, self.lst)

    def __argsDisp(self):
        d = ""
        for i in self._args:
            d += " " + i
        return d

    def terminate(self):
        print "Terminating"
        self.prc.terminate()
        self.cls()

    def cls(self):
        self.prc.close()
        self.prc.kill()

    def _getErrorData(self):
        #byt = QtCore.QByteArray()
        #return ''
        byt = self.prc.readAllStandardError()
        return str(byt.data()).strip()

    def _getMainData(self):
        byt = QtCore.QByteArray()
        byt = self.prc.readAllStandardOutput()
        return str(byt.data()).strip()


        #byt = ''
        #while (self.prc.waitForReadyRead()):
        #    byt += self.prc.readAll();
        #return byt

