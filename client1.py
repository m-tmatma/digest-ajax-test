import urllib.request

urls = [
	'http://localhost:8000',
	'http://localhost:8000/login/',
]

for url in urls:
	try:
		req = urllib.request.Request(url)
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
