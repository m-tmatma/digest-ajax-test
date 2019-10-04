import urllib3
import os

path = os.path.abspath(__file__)
name = os.path.basename(path)

fields = {
    'foo': 'bar',
    'fakefile': ('foofile.txt', 'contents of foofile'),
    'realfile': (name, open(path).read(), 'text/python'),
    'nonamefile': 'contents of nonamefile field',
}

http = urllib3.PoolManager()
r = http.request(
	'POST',
	'http://localhost:8000',
	fields=fields)
print (r.status)
print (r.data.decode('utf-8'))
print (r.headers)
