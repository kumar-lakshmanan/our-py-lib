#For DevConsole
import requests
import urllib.request as req
from urllib.request import Request
from bs4 import BeautifulSoup
import json
import os
import socket
import customStartups

os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), "cacert.pem")

class commonTools():
	
	def __init__(self, parent):
		self.parent=parent
		self.isInternetAvailable=False

	def doStartupRun(self):
		self.checkInternetAvailability()
		self.parent.customStartupsClsObj=customStartups.customStartupsCls(self.parent)
		self.parent.customStartupsClsObj.doStartup()

	def checkInternetAvailability(self):
		print("Checking internet availability....")
		url='https://secure.orbitremit.com/'
		try:
			print("Trying..." + url)
			data=self.readUrl(url)
			if(data):
				self.isInternetAvailable=True
				print("Available!")
				return
		except:
			pass
		print("Not available!")

	def readUrl(self,url):
		if socket.gethostname()=='NIGSA291604':
			return self.readUrlOffice(url)
		else:
			return self.readUrlHome(url)

	def readUrlOffice(self, url):
		os.environ["HTTP_PROXY"]=os.environ["HTTPS_PROXY"]=self.nabProxy
		proxy = req.ProxyHandler({'http': os.environ["HTTP_PROXY"],'https': os.environ["HTTPS_PROXY"]})
		hdr = {'User-Agent':'Mozilla/5.0'}
		auth = req.HTTPBasicAuthHandler()
		opener = req.build_opener(proxy, auth, req.HTTPHandler)
		req.install_opener(opener)

		reqst = Request(url, headers=hdr)
		webContent = req.urlopen(reqst).read()
		return webContent

	def readUrlHome(self, url):
		webContent = requests.get(url).text
		return webContent
				
	def trayMessage(self, message):
		self.parent.traymessage("Hapy",str(message))
		self.say("Tray: " + str(message))
		
	def say(self, info):
		print("Hapy: "+str(info))