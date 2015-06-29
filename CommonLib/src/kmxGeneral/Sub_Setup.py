
#Cutpaste this code to a new file and save it near the main python file (C:\Documents and Settings\balaji\My Documents\Python2\Render2\00RM-S10-Timer\RenderSubmit\RenderSubmit.py)
#Put a Icon file named AppIcon.ico near (C:\Documents and Settings\balaji\My Documents\Python2\Render2\00RM-S10-Timer\RenderSubmit\RenderSubmit.py)
#After that save and run the cutpasted file with arguments as shown below.. (Else Use the tool to do it ...)
#Python.exe setup.py py2exe --includes sip

from py2exe.build_exe import py2exe
from distutils.core import setup
import py2exe
MAINFILE = "Render3.py"
MICON = "MSN.ico"

setup(
    name=MAINFILE,
    author='Kumaresan',
    options = {
        'py2exe': {'bundle_files': 1}
        },
    windows = [
        {
            "script": MAINFILE,
            "icon_resources": [(0, MICON)]
        }
    ],
)



#This is for Python2Exe Convertor!

