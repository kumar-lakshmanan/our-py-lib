import urllib.request as req
from urllib.request import Request

proxy = req.ProxyHandler({'http': r'http://aur\p729465:Jul4132!@10.7.33.71:8080','https': r'http://aur\p729465:Jul4132!@10.7.33.71:8080'})
hdr = {'User-Agent':'Mozilla/5.0'}
auth = req.HTTPBasicAuthHandler()
opener = req.build_opener(proxy, auth, req.HTTPHandler)
req.install_opener(opener)

url='https://secure.orbitremit.com/api/rates/AUD:INR.json'
reqst = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
webpage = req.urlopen(reqst).read()
print(webpage)
#conn = req.urlopen()
#return_str = conn.read()
#print(return_str)