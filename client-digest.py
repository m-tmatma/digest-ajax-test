import urllib.request
import urllib

try:
	# http://vps.lolipop.jp/urllib%E3%81%A7Basic%E8%AA%8D%E8%A8%BC%E3%82%84Digest%E8%AA%8D%E8%A8%BC%E3%82%92%E4%BD%BF%E3%81%86%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB
	# https://github.com/loop333/github_traffic/blob/ab937e28a763a9ebb4c5e69ec21801d31ed70c4a/traffic.py

	user='foo'
	password='bar'
	url = 'http://localhost:8000/login/'

	http_handler = urllib.request.HTTPHandler()
	req = urllib.request.Request(url)
	pass_mgr = urllib.request.HTTPPasswordMgrWithPriorAuth()
	pass_mgr.add_password(None, url, user, password, is_authenticated=True)

#	auth_handler = urllib.request.HTTPBasicAuthHandler(pass_mgr)
	auth_handler = urllib.request.HTTPDigestAuthHandler(pass_mgr)
	opener = urllib.request.build_opener(http_handler, auth_handler)

	res = opener.open(url)
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
