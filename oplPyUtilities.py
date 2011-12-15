#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      AIAA
#
# Created:     14-12-2011
# Copyright:   (c) AIAA 2011
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import inspect
import datetime
from time import strftime
import itertools

class oplPyUtilities():

    def getAttributes(self,cls):
        boring = dir(type('dummy', (object,), {}))
        mems = [item for item in inspect.getmembers(cls)
                if item[0] not in boring]
        res = []
        for mem in mems:
            if (str(mem[1].__class__)!="<type 'instancemethod'>" and
                str(mem[1].__class__).find("<class")==-1 and
                str(type(mem[1])).find("'instance'")==-1 ) :
                res.append(mem)
        return res

    def getVariableName(self, var):
         return [tpl[0] for tpl in
         itertools.ifilter(lambda x: var is x[1], globals().items())]

    def getDateTime(self, format = "%Y-%m-%d %H:%M:%S"):
        """
        "%Y-%m-%d %H:%M:%S"
        Directive Meaning Notes
        %a Locale's abbreviated weekday name.
        %A Locale's full weekday name.
        %b Locale's abbreviated month name.
        %B Locale's full month name.
        %c Locale's appropriate date and time representation.
        %d Day of the month as a decimal number [01,31].
        %H Hour (24-hour clock) as a decimal number [00,23].
        %I Hour (12-hour clock) as a decimal number [01,12].
        %j Day of the year as a decimal number [001,366].
        %m Month as a decimal number [01,12].
        %M Minute as a decimal number [00,59].
        %p Locale's equivalent of either AM or PM. (1)
        %S Second as a decimal number [00,61]. (2)
        %U Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0. (3)
        %w Weekday as a decimal number [0(Sunday),6].
        %W Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0. (3)
        %x Locale's appropriate date representation.
        %X Locale's appropriate time representation.
        %y Year without century as a decimal number [00,99].
        %Y Year with century as a decimal number.
        %Z Time zone name (no characters if no time zone exists).
        %% A literal "%" character.
        """
        return strftime(format)

if __name__ == "__main__":
    import mRTaskStatus as mrt
    o = oplPyUtilities()
    z =  o.getAttributes(mrt)
    for i in z[0:len(z)-4]:
        print i
