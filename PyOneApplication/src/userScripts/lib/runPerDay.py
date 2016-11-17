'''
#For DevConsole
'''
import os
class RunperdayCls():
	
	def __init__(self,parent):
		self.parent=parent
		self.today=self.parent.ttls.getDateTime('%Y-%m-%d')
		print("RunperdayCls is ready!")
	
	def doRun(self,runThisFuncionOnceForToday):
		print("Checking todays run status...")
		if(os.path.exists('today')):
			if(self.parent.ttls.fileContent('today')==self.today):
				print("Already executed for today!")
			else:
				self.executeForToday(runThisFuncionOnceForToday)
		else:
			self.executeForToday(runThisFuncionOnceForToday)
					
	def executeForToday(self, fn):
		self.parent.ttls.writeFileContent('today',self.today)
		fn(self.parent)
		print("Executed once for today!")

	def forgetTodaysRun(self):
		self.parent.ttls.writeFileContent('today','')
		print("Forgot todays run!")		

def doThisOnce(arg):
	print("Done for today!")

if __name__ == '__main__':
	dev.RunperdayClsObj = RunperdayCls(dev)
	dev.RunperdayClsObj.doRun(doThisOnce)
	#dev.RunperdayClsObj.forgetTodaysRun()
