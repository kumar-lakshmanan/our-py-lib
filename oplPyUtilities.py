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
