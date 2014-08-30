import os
import popen2
import subprocess as sp

class PythonClient(object):
    '''
    PythonClient (pycl) is simple class to communicate with PyServer.exe

    pycl can be invoked in two modes runServerGetData, runServer.

    runServerGetData will invokes PyServer in hidden thread with arguments you pass and
    waits till PyServer completes its operation.
    Once server completes its operation. It grabs all its std outputs (Print statments)
    and returns to client. So, If your PyServer is running as console mode with lots of
    std outputs printed which can be deliverd to client for furthur process
    after its completion.

    runServer will invokes PyServer and leaves unattended from client.
    This helps you in making PyServer to start some UI based logics. In which
    stdouts and user interactions can be handled seperatly in ui and server side logics.

    '''

    def __init__(self, serverPath=''):
        '''
        serverPath - PyServer.exe path will be invoked by runServerGetData,runServer
        '''

        self.serverPath = ''
        self.isEmpty = lambda line='': True if str(line).strip()=='' else False
        if serverPath and os.path.exists(serverPath) and os.path.isfile(serverPath):
            serverPath = serverPath.strip()
            serverPath = os.path.normpath(serverPath)
            self.serverPath = serverPath
        else:
            return None

    def runServerGetData(self, args):
        '''
        runServerGetData will invokes PyServer in hidden thread with arguments you pass and
        waits till PyServer completes its operation.
        Once server completes its operation. It grabs all its std outputs (Print statments)
        and returns to client. So, If your PyServer is running as console mode with lots of
        std outputs printed which can be deliverd to client for furthur process
        after its completion.
        '''

        arg = ' '.join(args)
        path = os.path.dirname(self.serverPath)
        cmd = '%s %s' % (self.serverPath,arg)
        print 'Executing... %s' % cmd
        temp = os.getcwd()
        os.chdir(path)
        (filesys,filein) = popen2.popen4(cmd)
        datas = filesys.readlines()
        filesys.close()
        os.chdir(temp)
        return self.__refineResult(datas)

    def runServer(self, args):
        '''
        runServer will invokes PyServer and leaves unattended from client.
        This helps you in making PyServer to start some UI based logics. In which
        stdouts and user interactions can be handled seperatly in ui and server side logics.
        '''

        arg = ' '.join(args)
        path = os.path.dirname(self.serverPath)
        cmd = '%s %s' % (self.serverPath,arg)
        print 'Starting... %s' % cmd
        sp.Popen(cmd,cwd=path,shell=False)
        print 'Execution Started!'
        return []

    def __refineResult(self, data):
        '''
        Refining datas captured from std outs
        '''
        DataLines = []
        for eachLine in data:
            if not self.isEmpty(eachLine):
                DataLines.append(eachLine.strip())
        return DataLines


if __name__ == '__main__':
    server = 'Z:\REPO\PulseServer\PyServer\PyServer.exe'
    #arguments = ['mod_updater', 'runUpdater', 'pulse_beat']
    #arguments = ['mod_updater', 'runSilentUpdater', 'pulse_beat']
    #arguments = ['mod_updater', 'getCurrentVersion', 'pulse_beat']
    #arguments = ['mod_updater', 'getConfigInfo', 'pulse_beat', 'lclAppFile']
    arguments = ['third', 'testFunction']
    client = PythonClient(server)
    result = client.runServer(arguments)
    for res in result:
        print res
