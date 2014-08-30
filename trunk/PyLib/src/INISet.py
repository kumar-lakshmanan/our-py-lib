#from Sub_INIReader import *
import ConfigParser

def INISetValue(inifile,section,option,value):

    """
    INISetValue(inifile,section,option,value):
    """

    if not os.path.exists(inifile):
        f = open(inifile,"a")
        f.write("")
        f.close()

    if os.path.exists(inifile):
        config = ConfigParser.RawConfigParser()

        if not config.has_section(section):
            config.add_section(section)
            config.set(section,option,value)
        else:
            config.set(section,option,value)

        configfile = open(inifile)
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



    return r



