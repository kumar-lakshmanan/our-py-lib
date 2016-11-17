'''
#For DevConsole
'''
import os

class settings():
	
	def __init__(self, parent):
		self.parent = parent

	def doInitialize(self):   
		print("Initializing settings....")
		
		self.path=os.getcwd()
		self.desktopPath=r'C:\Users\MUKUND\Desktop\devCons'
		self.timerInterval=60 #Second
		self.autoStartTimer=True
		self.devConsDB='devSystem.db'
		
		self.techmID='kl98503'
		self.techmPass=self.parent.decrypt('Vj{;8:9,') 
		
		self.exchangeRateFile='exchange.csv'
		
		self.splitJoinReadSize=1024
		self.splitJoinChunkSize=1
		self.splitJoinPartName='Part'

		
		self.nabProxyUID='aur\p729465'
		self.nabProxyPass=self.parent.decrypt('Q|s;8:9(')
		self.nabProxyIP='10.7.33.71:8080'
		self.nabProxy='http://'+self.nabProxyUID+':'+self.nabProxyPass+'@'+self.nabProxyIP
		
		self.dropboxAccesskey = self.parent.decrypt('uht;i;>x!wv>|;@')
		self.dropboxAppSecretCode = self.parent.decrypt('9}87yj"9;spm <h')		
		self.dropboxCode = self.parent.decrypt('?uvfU]Z|O9nHHHHHHHHKhr]:z^7m`^zRZ4=`zZRzO`')   
		self.dropboxAccessToken = self.parent.decrypt('?uvfU]Z|O9nHHHHHHHHKh?XX" {aJki4i_tHki4Uz4i|_|9LvS u@[Ol_a7ZNta')
		
		self.simpleNoteUID='kaymatrix@gmail.com'
		self.simpleNotePass=self.parent.decrypt('ipvjopwz')
		
		self.parent.showNormal()
		self.parent.showMinimized()
