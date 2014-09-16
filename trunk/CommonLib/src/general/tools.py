'''
Created on Sep 6, 2014

@author: Mukundan
'''

import os
import pickle
import inspect
import sys

class MySettings(object):
    var1 = "aa"
    var2 = "ba"
    var3 = 1
    var4 = 20312312331231
    var5 = -3
    var6 = False
    var7 = True
    var8 = None


class basic(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor

        '''
    def error(self, message):
        print("{} Error: {}".format(self._buildCallerPath(), message))

    def info(self, message):
        print("{} Info: {}".format(self._buildCallerPath(), message))

    def _buildCallerPath(self):
        stack = inspect.stack()
        path = ""
        for eachStack in stack:
            if("self" in eachStack[0].f_locals.keys()):
                the_class = eachStack[0].f_locals["self"].__class__.__name__
                the_method = eachStack[0].f_code.co_name
                if(the_class != "basic"):
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
