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

# at this point if I could figure out how to put this as a form/multipart I
# would repro the bug, but requests sucks for doing this, and apparently
# form/multipart is so arcane that I can't find a single Python library for
# doing it. So fuck python.