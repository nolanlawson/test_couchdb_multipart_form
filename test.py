#!/usr/bin/env python

import requests, json, httplib

couch = 'http://localhost:5984/test_multipart';

print requests.delete(couch).json();
print requests.put(couch).json();

doc = json.loads("""{"_id":"doc","_rev":"2-x",
  "_attachments":{
    "foo.txt":{"content_type":"text/plain","data":"Zm9v"}
    },"_revisions":{"start":2,"ids":["x","a"]}}""")

print requests.post(couch + '/_bulk_docs', \
  headers={'content-type': 'application/json'}, \
  data=json.dumps({"docs": [doc], "new_edits": False})).json();

print requests.get(couch + '/doc').json();

# same doc (no error)
print requests.post(couch + '/_bulk_docs', \
  headers={'content-type': 'application/json'}, \
  data=json.dumps({"docs": [doc], "new_edits": False})).json();

# same doc, but with stubs instead of full attachments (error)
doc_with_stubs = requests.get(couch + '/doc').json();
print requests.post(couch + '/_bulk_docs', \
  headers={'content-type': 'application/json'}, \
  data=json.dumps({"docs": [doc_with_stubs], "new_edits": False})).json();
  
# same doc with stubs, but using multipart instead of just json (no error)
doc_multipart = requests.get(couch + '/doc').json();
doc_multipart['_attachments']['foo.txt']['follows'] = True;

BOUNDARY = '----------some-cool-boundary$'
CRLF = '\r\n'
L = []
L.append('--' + BOUNDARY)
L.append('content-type: application/json')
L.append('')
L.append(json.dumps(doc_multipart))
L.append('--' + BOUNDARY)
L.append('Content-Disposition: attachment; filename="foo.txt"')
L.append('Content-Length: 3')
L.append('Content-Type: text/plain')
L.append('')
L.append('foo')
L.append('--' + BOUNDARY + '--')
L.append('')
body = CRLF.join(L)
content_type = 'multipart/form-data; boundary=%s' % BOUNDARY

h = httplib.HTTP('127.0.0.1:5984')
h.putrequest('PUT', '/test_multipart/doc?new_edits=false')
h.putheader('content-type', content_type)
h.putheader('content-length', str(len(body)))
h.endheaders()
h.send(body)
errcode, errmsg, headers = h.getreply()
print h.file.read()