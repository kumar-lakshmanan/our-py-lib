'''
Created on Oct 24, 2015

@author: MUKUND
'''

import sys
import os

#ErrorReport and CrashHandle - Call CrashHandle within uncontrolled expections
def errorReport(prittyPrint=1):
    TrackStack = sys.exc_info()[2]
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


def handleThis():
    data = errorReport()
    print(data)
    f = open('CrashReport.txt','w')
    f.write(str(data))
    f.close()
    #Quit the program
    sys.exit(0)
