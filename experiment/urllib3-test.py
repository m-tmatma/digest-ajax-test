import urllib3
import urllib3.fields

server = "localhost"
http = urllib3.HTTPConnectionPool(server, maxsize=10)
#http = urllib3.PoolManager()

for i in range(11):
	r = http.request('GET', 'http://' + server + '/', fields={'arg': 'value', 'arg2': '@value'})
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
