'''
#For DevConsole
'''
from PyQt5 import QtCore, QtGui, Qsci, QtWidgets
import runPerDay
import socket
import general
import customShortcuts
import os

class customStartupsCls():
	
	def __init__(self,parent):
		self.parent=parent
		self.settings=self.parent.settings
		self.timerIntervalSec=60
		self.ttls = self.parent.customTools
		
	def doStartup(self):
		print("Custom startup started!")
		self.doAlterUI()
		self.doUpdateContextMenu()
		self.doRunOncePerDay()
		self.doShortCuts()
		self.doGeneralSetup()
		self.doTimerSetup()
		print("Custom startup completed!")

	def doTimerSetup(self):
		self.parent.qtime=QtCore.QTimer(self.parent)
		self.parent.qtime.timeout.connect(self._actionTimeOut)   
		if(self.settings.autoStartTimer):
			self.parent.qtime.start(1000 * self.settings.timerInterval)
			print("Timer started (For ever " + str(self.settings.timerInterval) + " sec)")
		self.say("Timer ready!")

	def doGeneralSetup(self):
		if (socket.gethostname()=='NIGSA291604'):
			self.parent.pyDesigner = "C:\Temp\DevTools\PyDev\PyQt5\designer.exe"
			os.environ["HTTP_PROXY"]=os.environ["HTTPS_PROXY"]=self.settings.nabProxy
		if (socket.gethostname()=='MUKUND-PC'):
			self.parent.pyDesigner = "C:\Python34\Lib\site-packages\PyQt5\designer.exe"
		self.say("General done!")			
	
	def doShortCuts(self):
		self.parent.customShortcutsClsObj=customShortcuts.customShotcutsCls(self.parent)
		self.parent.customShortcutsClsObj.initializeRequiredObjects()
		self.say("ShortCuts done!")
		
	def doRunOncePerDay(self):
		self.parent.RunperdayClsObj = runPerDay.RunperdayCls(self.parent)
		self.parent.RunperdayClsObj.doRun(self._actionRunOncePerDay)
		self.say("RunOncePerDay done!")
		
	def doUpdateContextMenu(self):
		#self.parent.updateTrayMenu('|')
		#self.parent.updateTrayMenu('MyCalc',self._actionContextItemClicked)	
		#self.parent.updateTrayMenu('AUDGraph',self._actionContextItemClicked)	
		self.say("UpdateContextMenu done!")
		
	def doAlterUI(self):
		#pass
		self.parent.qtTools.applyStyle('Fusion')				
		self.say("AlterUI done!")
				
	def say(self, info):
		print("Custom: " + str(info))	

	def _actionContextItemClicked(self, *arg):
		obj = self.parent.sender()
		caller = str(obj.text())
		self.say("Call from " + caller)
		if(caller == 'MyCalc'):
			self.parent.customShortcutsClsObj.call_Calc()
		if(caller == 'AUDGraph'):
			self.parent.customShortcutsClsObj.call_Exchangegraph()			
	
	def _actionRunOncePerDay(self, *arg):
		#Updating exchange rate...
		self.parent.AudratesClsObj = AUDRates.AudratesCls(self.parent)
		self.parent.AudratesClsObj.showRates()
		self.parent.AudratesClsObj.updateHistory()
		#self.parent.techMTimeSheetClsObj.submitTimeSheet()

	def _actionTimeOut(self):		
		if(not hasattr(self.parent,'AudratesClsObj')):
			self.parent.AudratesClsObj = AUDRates.AudratesCls(self.parent)
		rate = self.parent.AudratesClsObj.orbitExchangeRate()
		if (float(rate)>48):
			self.parent.traymessage("Exchange Rate","Exchange Rate increased - "+str(rate))	

if __name__ == '__main__':
	dev.customStartupsClsObj = customStartupsCls(dev)
	dev.customStartupsClsObj._actionTimeOut()