import os
import random
import sys
import subprocess as sp
import socket
from optparse import OptionParser
import commandLine
from project_globals import ProjectGlobals


class AppShared():

    def __init__(self):
        self.curUser = os.environ.get("USERNAME").upper()
        self.curMachine = socket.gethostname().upper()
        self.curPythonVer = '2.5.1'
        self.curOS = 'Win NT 6.0'
        self.curProject = 'ZZP'
        self.arguments = self.__arguments()
        self.optionParse()

    def optionParse(self):

        usageInfo = '''
                LNP - Light and Pray - Part of PULSE AMS

                Use following flags to set startup information
                usage: lnpApplication.exe -[Option] [value]

                    Option    Value           Description
                    -p      projectcode     Project to make use of.
                    -d                      Detect project from mapped drive.
                    -m      app mode        Internal use only
                '''


        parser = OptionParser(usage = usageInfo, description = 'LNP - Commandline')
        parser.add_option("-m", "--lnp_mode",  help="Application run mode - DEVELOPER/DEBUG/USERS")
        parser.add_option("-p", "--lnp_project", help="Project to make use of.")
        parser.add_option("-d", "--lnp_detectProject", help="Detect project from mapped drive.")
        self.opts = parser.parse_args()[0]

        self.curProject = ''
        self.projFoundFrom = 'Project loaded from no where'
        if self.opts.lnp_project:
            self.projFoundFrom = 'Project loaded from CommandLine'
            self.curProject = self.opts.lnp_project
        elif self.opts.lnp_detectProject:
            self.curProject = self.detectProject()

        if not self.curProject:
            self.curProject = self.detectProject()

        self.devmode = 1#self.opts.lnp_mode

    def detectProject(self):
        cmd = commandLine.commandLineParser('net use')
        result = cmd.executeCommand(cleanResult=1)

        path = ''
        projectName = ''
        foundDrive = False
        foundPath = False
        for line in result:
            if not foundDrive and not foundPath:
                for word in line:
                    actWord = str(word.upper())
                    if not foundDrive and actWord == 'W:':
                        foundDrive = True
                    if not foundPath and foundDrive and actWord.find('\WORK')>0:
                        foundPath = True
                        path = actWord
            else:
                break

        if foundDrive and foundPath:
            if path == '' :
                return ''
            index = path.find('\WORK')
            projpath = path[:index].replace("\\", '/')
            pg = ProjectGlobals()
            projData = pg.getProjectPaths()
            for each in projData.keys() :
                if projData[each].upper() == projpath.upper() :
                    return each
        return ''

    def __arguments(self):

        args = sys.argv
        lst = []
        self.starter = str(args[0])
        for arg in xrange(1,len(args)):
            lst.append(str(args[arg]))
        return lst

    def errorReport(self, prittyPrint=1):
        TrackStack = sys.exc_traceback
        ErrorReport = []
        while TrackStack:
        	FileName = TrackStack.tb_frame.f_code.co_filename
        	FunctionName = TrackStack.tb_frame.f_code.co_name
        	ErrorLine =TrackStack.tb_lineno
        	TrackStack = TrackStack.tb_next
        	ErrorReport.append([FileName,FunctionName,ErrorLine])
        ErrorReport.append([sys.exc_info()[0],sys.exc_info()[1],0])
        if prittyPrint:
            ErrorInfo=''
            tabs = ''
            for eachErrorLevel in ErrorReport:
                ErrorInfo+= '\n' + tabs + 'File: "' + str(eachErrorLevel[0]) + '", line ' + str(eachErrorLevel[2]) + ', in ' + str(eachErrorLevel[1])
            return ErrorInfo
        else:
            return ErrorReport

    def codePosition(self):
        import inspect
        print inspect.stack.func_code

        #print func_name
##        TrackStack = sys.exc_info()
##        ErrorReport = []
##    	FileName = TrackStack.tb_frame.f_code.co_filename
##    	FunctionName = TrackStack.tb_frame.f_code.co_name
##    	ErrorLine =TrackStack.tb_lineno
##        return '\nLocation:\nFile: %s\nFunction: %s\nLineNo: %s'%(FileName,FunctionName,ErrorLine)

##
##a = AppShared()
##print a.detectProject()