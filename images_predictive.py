# -*- coding: utf-8 -*-

# http://localhost:8080/images/000/predictive/1.png
# http://localhost:8080/images/000/predictive/6.png
# http://localhost:8080/images/201/predictive/1.png
# http://localhost:8080/images/201/predictive/6.png

import os
import re

import nowcast


request_path = os.environ["PATH_INFO"]
match   = re.compile(r"/images/(\d+)/predictive/(\d)\.png").match(request_path)
area    = int(match.group(1))
ordinal = int(match.group(2))

time  = nowcast.get_current_predictive_time()
image = nowcast.get_image(area, time, ordinal)

print "Content-Type: image/png"
print ""
print image
