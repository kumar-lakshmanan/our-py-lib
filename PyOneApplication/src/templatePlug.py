'''
#For DevConsole
'''

class myClassCls():
	
	def __init__(self,parent):
		self.parent=parent
		self.settings=self.parent.settings
		self.tools=self.parent.customTools
		print("myClassCls is ready!")

	def doRun(self):
		print("myClassCls is working fine")

if __name__ == '__main__':
	dev.myClassClsObj = myClassCls(dev)
	dev.myClassClsObj.doRun()
