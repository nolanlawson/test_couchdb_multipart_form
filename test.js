#!/usr/bin/node

var db = require('nano')({ url : 'http://localhost:5984/test_multipart'});

var doc = {"_id":"doc","_rev":"2-x","_revisions":{"start":2,"ids":["x","a"]}};

db.multipart.insert({ foo: 'bar' }, 
  [{name: 'foo.txt', data: 'foo', content_type: 'text/plain'}], {new_edits: false}, function(err, body) {
        if (err) {
          console.log(err);
        } else {
          console.log(body);
        }
        });