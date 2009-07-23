# -*- coding: utf-8 -*-

import os
import re

request_path = os.environ["PATH_INFO"]
match = re.compile(r"/images/(\d+)").match(request_path)
area  = int(match.group(1))

print "Content-Type: text/html"
print ""
print """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="ja" xml:lang="ja">
 <head>
  <title>amayadori</title>
 </head>
 <body>"""

print '<div><img src="/images/' + str(area) + '/observed.png" alt="" /></div>'
print '<div><img src="/images/' + str(area) + '/predictive/1.png" alt="" /></div>'
print '<div><img src="/images/' + str(area) + '/predictive/2.png" alt="" /></div>'
print '<div><img src="/images/' + str(area) + '/predictive/3.png" alt="" /></div>'
print '<div><img src="/images/' + str(area) + '/predictive/4.png" alt="" /></div>'
print '<div><img src="/images/' + str(area) + '/predictive/5.png" alt="" /></div>'
print '<div><img src="/images/' + str(area) + '/predictive/6.png" alt="" /></div>'

print """
 </body>
</html>"""
