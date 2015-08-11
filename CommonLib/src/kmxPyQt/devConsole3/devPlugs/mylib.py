import requests
import urllib.request as req
from urllib.request import Request
from bs4 import BeautifulSoup
import json
import os
os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), "cacert.pem")
#For DevConsole

def readUrl(url):
        proxy = req.ProxyHandler({'http': r'http://aur\p729465:Jul4132!@10.7.33.71:8080','https': r'http://aur\p729465:Jul4132!@10.7.33.71:8080'})
        hdr = {'User-Agent':'Mozilla/5.0'}
        auth = req.HTTPBasicAuthHandler()
        opener = req.build_opener(proxy, auth, req.HTTPHandler)
        req.install_opener(opener)

        reqst = Request(url, headers=hdr)
        webContent = req.urlopen(reqst).read()
        return webContent


                
