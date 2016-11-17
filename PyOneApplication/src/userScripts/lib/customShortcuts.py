'''
#For DevConsole
#Kumaresan
'''

from PyQt5 import QtCore, QtGui, QtWidgets

import sip
import mysqlite
import amILucky
import objBrowser
import myCalc

class customShotcutsCls():
	
	def __init__(self,parent):
		self.parent=parent
		self.settings=self.parent.settings		
		self.shortcutPair = {}

	def initializeRequiredObjects(self):
		print("customShotcutsCls is ready!")
		self.parent.newToolBar = QtWidgets.QToolBar('Custom Tools',self.parent) 
		self.parent.addToolBar(self.parent.newToolBar)
		self.parent.updateTrayMenu('|')

		if(not hasattr(self.parent,'AmiluckyClsObj')):		
			self.parent.AmiluckyClsObj = amILucky.AmiluckyCls(self.parent)	 
		if(not hasattr(self.parent,'objBrowserClsObj')):		
			self.parent.objBrowserClsObj = objBrowser.objBrowserCls(self.parent)	
		if(not hasattr(self.parent,'myCalcClsObj')):	   
			self.parent.myCalcClsObj = myCalc.myCalcCls(self.parent)
		
		# CHeck this url for icon names:
		# http://dev.vizuina.com/farmfresh/ 
		
		self.doQuickShortcut('ObjBrowser', self.call_objBrowser,2)	
		self.doQuickShortcutWithIcon('Notes', self.call_Note,'note.png')		
		self.doQuickShortcutWithIcon('SQLite', self.call_Sqlite,'database_go.png') 
		self.timer_tgl = self.doQuickShortcutWithIcon('Toggle Timer', None ,'time.png')   
		self.timer_tgl.toggled.connect(self.call_ToggleTimer)
		self.timer_tgl.setCheckable(True)		
		self.timer_tgl.setChecked(self.settings.autoStartTimer)		
		self.devToggle = self.doQuickShortcutWithIcon('toggleDevMode', None, 'bios.png')
		self.devToggle.toggled.connect(self.toggleDevMode)
		self.devToggle.setCheckable(True)
		self.doQuickShortcutWithIcon('Calc', self.call_Calc,'calculator.png')		
		
	def toggleDevMode(self, state):
		self.parent.devMode = state
		print('Developer mode state: ' + str(state))

	def call_Calc(self):
		self.parent.myCalcClsObj.show()
		self.parent.myCalcClsObj.raise_()
		
	def call_Note(self):
		self.parent.NotesClsObj.show()
		self.parent.NotesClsObj.raise_()
		
	def call_ToggleTimer(self, state):
		if(hasattr(self.parent,'qtime')):
			if state:
				self.parent.qtime.start(1000 * self.settings.timerInterval)
				print("Timer started (For ever " + str(self.settings.timerInterval) + " sec)")
			else:
				self.parent.qtime.stop()
				print("Timer stopped")			
		
	def call_QuickTools(self):
		import QuickTools		
		if(not hasattr(self.parent,'QuickToolsClsObj') or sip.isdeleted(self.parent.QuickToolsClsObj)):	   
			   self.parent.QuickToolsClsObj = QuickTools.QuickToolsCls(self.parent)		
		self.parent.QuickToolsClsObj.show()
		self.parent.QuickToolsClsObj.raise_()
		
	def call_objBrowser(self):
		self.parent.objBrowserClsObj.show()
		self.parent.objBrowserClsObj.raise_()
		
	def call_splitAndJoin(self, *arg):
		self.parent.SplitsAndCompressClsObj.show()
		self.parent.SplitsAndCompressClsObj.raise_()

	def call_Sqlite(self, *arg):
		self.parent.SqliteClsObj.show()

	def call_Amilucky(self, *arg):
		self.parent.AmiluckyClsObj.show()

	def doQuickShortcut(self, label, callBackFn, type_=1):
		if(type_==1):
			return self._doShortcut(label, 'bullet_star.png', callBackFn, self.parent.newToolBar)   
		elif(type_==2):
			return self._doShortcut(label, 'bullet_red.png', callBackFn, self.parent.newToolBar)			   
		elif(type_==3):
			return self._doShortcut(label, 'bullet_purple.png', callBackFn, self.parent.newToolBar)			   
		elif(type_==4):
			return self._doShortcut(label, 'bullet_pink.png', callBackFn, self.parent.newToolBar)
			
	def doQuickShortcutWithIcon(self, label, callBackFn, icon):
		return self._doShortcut(label, icon, callBackFn, self.parent.newToolBar)
		
	def _doShortcut(self, label='text', icon='bullet_star.png', callBackFn=None, toolBar=None):
		if (label=='|'):
			self.parent.addSeparator()
			self.parent.updateTrayMenu('|')
		else:
			action = QtWidgets.QAction(self.parent)
			action.setText(label)
			if callBackFn is not None: action.triggered.connect(callBackFn)
			self.parent.qtIcon.setIcon(action, icon)
			toolBar.addAction(action)
			
			if callBackFn is not None:
				self.shortcutPair[label]=callBackFn
				self.parent.updateTrayMenu(label,self._actionContextItemClicked)	
			return action		
			
	def _actionContextItemClicked(self, *arg):
		obj = self.parent.sender()
		caller = str(obj.text())
		print("Call from " + caller)
		callBackFn = self.shortcutPair[caller]
		if(callBackFn):
			callBackFn()		
			
if __name__ == '__main__':
	dev.customShotcutsClsObj = customShotcutsCls(dev)
	#dev.customShotcutsClsObj.initializeRequiredObjects()
