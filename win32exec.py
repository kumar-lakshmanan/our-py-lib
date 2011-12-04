import sys
import os
import shutil
import filecmp
import popen2
import subprocess as sp

class win32Execute():
    '''
        Executes windows shell commands and parse shell results.
    '''
    def __init__(self, CommandLine, SpaceOffsets=2, Splitter=''):
        self.__isEmpty = lambda line='': True if str(line).strip()=='' else False
        self.__spaceOffset = SpaceOffsets
        self.__commandLine = CommandLine
        self.Splitter = Splitter

    def executeCommand(self,cleanResult=0):
        dataLines = []
        if self.__commandLine:
            try:
                (filesys,filein) = popen2.popen4(self.__commandLine)
                dataLines = filesys.readlines()
                filesys.close()
            except:
                dataLines = []
        self.recentResult = self.__CLPparse(dataLines)
        if cleanResult: self.recentResult = self.resultCleanUp()
        return self.recentResult

    def resultCleanUp(self, result = ''):
        result = result if result else self.recentResult
        lines = []
        for line in result:
            words = []
            for word in line:
                if word: words.append(str(word).strip())
            lines.append(words)
        return lines

    def __CLPparse(self,ListOfLines=[]):

        DataLines = []
        for eachLine in ListOfLines:
            if not self.__isEmpty(eachLine):
                DataLines.append(eachLine.strip())

        ValidDatas = []
        for eachLine in DataLines:
            ValidDatas.append(self.__CLPreadLine(eachLine))

        return ValidDatas

    def __CLPreadLine(self, Line):

        Spaces = ''
        for spcnt in xrange(self.__spaceOffset):
            Spaces+=' '

        AllWords = Line.split(Spaces)

        NewAllWords = []
        if self.Splitter:
            for eachWord in AllWords:
                splits = eachWord.split(self.Splitter)
                for eachSplit in splits:
                    if not self.__isEmpty(eachSplit):
                        NewAllWords.append(eachSplit)
        else:
            NewAllWords = AllWords

        ValidWords = NewAllWords

        return ValidWords

    def isUNC(self):
        unc = False
        lst = commandLineParser('cls').executeCommand()
        if len(lst)>2:
            if lst[2][0]=='UNC paths are not supported.':
                print '\nNot allowed to work on network!'
                unc = True
        return unc