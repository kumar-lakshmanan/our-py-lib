#QuickUtilities
'''
Quick utilites for getting things done faster
'''

import sys
import os

def errorReport(prittyPrint=1):
    '''
    returns recent error infos
    '''

    try:
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
            for eachErrorLevel in ErrorReport:
                ErrorInfo+= '\nFile: "' + str(eachErrorLevel[0]) + '", line ' + str(eachErrorLevel[2]) + ', in ' + str(eachErrorLevel[1])
            return ErrorInfo
        else:
            return ErrorReport
    except:
        return 'Problem Preparing Error Report'

def generateCrashReport(fileName = 'CrashReport.txt'):
        '''
        creates log file with recent error infos
        '''
        data = errorReport()
        f = open(fileName,'w')
        f.write(str(data))
        f.close()

def osjoin(folders):
    '''
    returns path after connecting all the folder strings with the slashes
    -- just for maintaining slash consistancy
    '''
    s = ''
    for folder in folders:
        s = os.path.join(s, folder)
    return s

