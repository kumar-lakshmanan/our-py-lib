url = 'http://localhost:9000/'
parm = {'foov' : 145, 'bar' : 2,'bis' : 3}
import json

print("-------")
print(str(json.dumps(parm)))
print("-------")


import requests
r = requests.get(url,params=parm)

query = urlparse(r.url).query
query_components = dict(qc.split("=") for qc in query.split("&"))

print("Request...")
print(query_components)
print("Response...")
print(r.text)

#arams = urllib.urlencode(post_dict)
#post_req = urllib2.Request(url)
#post_req.add_data(params)

#response = urllib2.urlopen(post_req)
#response_data = response.read()
#response.close()
#print (response_data)