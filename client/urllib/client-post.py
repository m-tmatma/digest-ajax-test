import urllib.request
import os

path = os.path.abspath(__file__)
name = os.path.basename(path)
data = open(path, "rb").read()
print (data)

urls = [
	'http://localhost:8000/post/?param1=%311&param2=2%31',
]

for url in urls:
	try:
		req = urllib.request.Request(url, method="POST", data=data)
		req.add_header('User-Agent', 'Test')

		# https://docs.python.org/ja/3/library/urllib.request.html#urllib.request.Request
		print (req.header_items())

		with urllib.request.urlopen(req) as res:
			headers = res.info()
			body = res.read()
			print (headers)
			print (body.decode('utf-8'))
	except urllib.error.HTTPError as e:
		# https://docs.python.org/ja/3/library/urllib.error.html#module-urllib.error
		print (e.code)
		print (e.reason)
		print (e.headers)
	except urllib.error.URLError as e:
		print (e.reason)
