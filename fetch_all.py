# -*- coding: utf-8 -*-

import urllib2

def fetch(url):
  req = urllib2.Request(url)
  io = urllib2.build_opener().open(req)
  data = io.read()
  io.close()
  return data

print fetch("http://www.nayutaya.co.jp/")
