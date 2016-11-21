'''
#For DevConsole
'''

class myClassCls():
	
	def __init__(self,parent):
		self.parent=parent
		self.tools=self.parent.ttls		
		self.qtTools=self.parent.qtTools
		print("myClassCls is ready!")

	def initialize(self):
		print("myClassCls is working fine")

if __name__ == '__main__':
	dev.myClassClsObj = myClassCls(dev)
	dev.myClassClsObj.initialize()
