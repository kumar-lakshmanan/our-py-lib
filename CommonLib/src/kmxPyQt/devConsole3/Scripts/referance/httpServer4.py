import http.client
import json

connection = http.client.HTTPSConnection('localhost:8080')

headers = {'Content-type': 'application/json'}

foo = {'text': '12'}
json_foo = json.dumps(foo)

connection.request('POST', '/add', json_foo, headers)

response = connection.getresponse()
print(response.read().decode())