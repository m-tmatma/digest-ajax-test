import urllib3
import urllib3.fields
import logging

rootLogger = logging.getLogger()

# create file handler which logs even debug messages
fh = logging.FileHandler('root.log')
# create console handler with a higher log level
ch = logging.StreamHandler()

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

rootLogger.setLevel(logging.DEBUG)
fh.setLevel(logging.DEBUG)
ch.setLevel(logging.DEBUG)

rootLogger.addHandler(fh)
rootLogger.addHandler(ch)

server = "localhost"
http = urllib3.HTTPConnectionPool(server, maxsize=10)
#http = urllib3.PoolManager()

for i in range(11):
	r = http.request('GET', 'http://' + server + '/', fields={'arg': 'value', 'arg2': '@value'})
#	r = http.request('GET', 'http://' + server + '/')
	for name, value in r.__dict__.items():
	    print(name, type(value))
	    #print("{0}: {1}".format(name, value))
	print(r.headers)
	print(r.reason)

	#print(r.data)


#requestField = urllib3.fields.RequestField("name", "data", filename="test.py", headers=None)
#requestField.make_multipart()
#print(requestField.render_headers())


field = urllib3.fields.RequestField.from_tuples(
    "fieldname",
    ("filen\u00e4me", ("data", "data2"))
)
print(field.render_headers())
print(field.make_multipart(content_disposition="Content-Disposition", content_type="application/octet-stream"))
print(field._render_parts({"name": "value", "filename": "value"}))
