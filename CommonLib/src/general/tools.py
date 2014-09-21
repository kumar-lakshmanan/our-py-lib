'''
Created on Sep 6, 2014

@author: Mukundan
'''

import os
import pickle
import inspect
import sys
import shutil

class MySettings(object):
    var1 = "aa"
    var2 = "ba"
    var3 = 1
    var4 = 20312312331231
    var5 = -3
    var6 = False
    var7 = True
    var8 = None

class infoStyle(object):
    errorLevel = 2  # -1-No Print, 0-Simple Message, 1-Calling Fn + Message, 2-Complete Info (Complete Path+Message)
    infoLevel = 2  # -1-No Print, 0-Simple Message, 1-Calling Fn + Message, 2-Complete Info (Complete Path+Message)

class basic(object):
    '''
    classdocs
    '''


    def __init__(self, infoStyle=None):
        '''
        Constructor

        '''
        if(infoStyle is None):
            self.infoStyle = infoStyle()
        else:
            self.infoStyle = infoStyle

    def error(self, message):
        if(self.infoStyle.errorLevel == 0):
            print("Error: {}".format(message))
        elif(self.infoStyle.errorLevel == 1):
            print("{} Error: {}".format(self._buildCallerPath(1), message))
        elif(self.infoStyle.errorLevel == 2):
            print("{} Error: {}".format(self._buildCallerPath(), message))

    def info(self, message):
        if(self.infoStyle.infoLevel == 0):
            print("{}".format(message))
        elif(self.infoStyle.infoLevel == 1):
            print("{} Info: {}".format(self._buildCallerPath(1), message))
        elif(self.infoStyle.infoLevel == 2):
            print("{} Info: {}".format(self._buildCallerPath(), message))

    def copyFile(self, src, dst):
        shutil.copy(src, dst)

    def _buildCallerPath(self, parentOnly=0):
        stack = inspect.stack()
        path = ""
        for eachStack in stack:
            if("self" in eachStack[0].f_locals.keys()):
                the_class = eachStack[0].f_locals["self"].__class__.__name__
                the_method = eachStack[0].f_code.co_name
                if(the_class != "basic"):
                    if(parentOnly):
                        path = "{}.{}()->".format(the_class, the_method)
                    else:
                        path += "{}.{}()->".format(the_class, the_method)
        return path

    def makePathForFile(self, file):
        base = os.path.dirname(file)
        self.makePath(base)

    def makePath(self, path):
        if(not os.path.exists(path) and path != ''):
            os.makedirs(path)
        else:
            self.error("Unable to read " + path)

    def isPathOK(self, path):
        return os.path.exists(path) and path != '' and path is not None

    def pickleSaveObject(self, obj, file=""):
        if(obj is None):
            self.error("Pass me valid object to save" + obj)
        className = obj.__class__.__name__
        if(file is None or file == ""):
            file = className + ".txt"
        base = os.path.dirname(file)
        if(not os.path.exists(base) and base != ''):
            os.makedirs(base)
        f = open(file, "wb")
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        f.close()
        self.info("Saved!" + className + "-" + file)

    def pickleLoadObject(self, file):
        x = None
        if(file is None or file == ""):
            self.error("Pass me file name to read and pass the object")
        if(os.path.exists(file)):
            try:
                f = open(file, "rb")
                x = pickle.load(f)
                f.close()
                self.info ("File read and obj returned " + file + " obj: " + x.__class__.__name__)
            except:
                self.error ("Error loading the pickle. Passing default!")
        else:
            self.error ("Error! File doesn't exist " + file)
        return x

class another(object):

    def __init__(self):
        pass

    def myFun(self):
        tls = basic()
        tls.error('s')

if __name__ == '__main__':

#     print("Saving...")
#     file = 'texxsts.txt'
#     tls = tools()
#     objx = MySettings()
#     objx.var1 = "Kumaresan"
#     tls.saveObject(objx, file)
# 
#     print("Loading...")
#     file = 'texxsts.txt'
#     tls = tools()
#     xx = tls.loadObject(file)
#     print("Value " + xx.var1)
#     
    
        an = another()
        an.myFun()
