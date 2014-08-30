import os
import ConfigParser

class configINI():

    filestatus = 0
    filename = ""

    def __init__(self,openfile):
        self.filename = openfile
        if os.path.exists(self.filename):
            self.filestatus = 1
            print self.filename
            print "SETTINGS FILE OPENED"
        else:
            self.filestatus = 0
            print self.filename
            print "SETTINGS FILE NOT FOUND"


    def write_settings(self, sec, listdicto, mode):

        config = ConfigParser.RawConfigParser()
        config.add_section(sec)

        for i in listdicto.keys():
            config.set(sec, i, str(listdicto[i]))

        configfile = open(self.filename, mode)
        config.write(configfile)



    def read_settings(self,sec):

        if self.filestatus==0: return None

        r=[]
        d={}

        config = ConfigParser.RawConfigParser()
        config.read(self.filename)

        if config.has_section(sec):

            for o in config.items(sec):
                r.append(o)

            for x in r:
                d[x[0]]=x[1]
        else:
            d = None

        return d
