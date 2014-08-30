#from Sub_INIReader import *
import ConfigParser
import os

def INISetValue(inifile,section,option,value):

    """
    INISetValue(inifile,section,option,value):
    """

    if not os.path.exists(inifile):
        print "Creating file..."
        f = open(inifile,"W")
        f.write("")
        f.close()

    if os.path.exists(inifile):
        config = ConfigParser.RawConfigParser()
        config.read(inifile)

        if not config.has_section(section):
            print "Adding new Section and option in INI..."
            config.add_section(section)
            config.set(section,option,value)
        else:
            print "Adding new option in INI..."
            config.set(section,option,value)

        configfile = open(inifile,"w")
        config.write(configfile)


def INIReadValue(inifile,section,option,createDefault=False,defaultValue=""):

    """
    INIReadValue(inifile,section,option,createDefault=False,defaultValue=""):
    """


    r = defaultValue

    if os.path.exists(inifile):

        config = ConfigParser.RawConfigParser()
        config.read(inifile)

        if config.has_section(section):
            if config.has_option(section,option):
                r = str(config.get(section,option))
            else:
                if createDefault:
                    INISetValue(inifile,section,option,defaultValue)

        else:
            if createDefault:
                INISetValue(inifile,section,option,defaultValue)

    else:
            if createDefault:
                INISetValue(inifile,section,option,defaultValue)



    return r



