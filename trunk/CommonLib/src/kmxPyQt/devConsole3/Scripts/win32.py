#sd
import time
import win32com
import win32com.client
shell = win32com.client.Dispatch('WScript.Shell')

#shell.Run('notepad')
shell.AppActivate('notepad')
#shell.SendKeys("Hello World", 0)
#shell.SendKeys("{Enter}", 0)
shell.SendKeys("{F5}", 0)   # F5 prints the time/date