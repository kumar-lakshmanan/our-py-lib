'''
#For DevConsole
'''

class newPlugCls():
	
	def __init__(self,parent):
		self.parent=parent
		self.tools=self.parent.ttls		
		self.qtTools=self.parent.qtTools
		print("newPlugCls is ready!")

	def doRun(self):
		print("newPlugCls is working fine")

if __name__ == '__main__':
	dev.newPlugClsObj = newPlugCls(dev)
	dev.newPlugClsObj.doRun()
