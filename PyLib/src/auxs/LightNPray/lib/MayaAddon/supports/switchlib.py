import os
import sys


class switchLib():

    def isInMaya():
        return True if 'maya' in sys.modules else False

    def isMaya2011():
        if isInMaya():
            import maya.OpenMayaUI as mui
            return hasattr(mui,'MQtUtil')
        else:
            return False

    def isPyQTLoaded():
        return True if 'PyQt4' in sys.modules else False

