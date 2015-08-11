import urllib.parse
from urllib.parse import urlparse
import json

p='http://localhost:9000/?bis=3&foo=1&bar=2'
query = urlparse(p).query
query_components = dict(qc.split("=") for qc in query.split("&"))
print(query_components)