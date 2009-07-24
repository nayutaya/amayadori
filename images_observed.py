# -*- coding: utf-8 -*-

# http://localhost:8080/images/000/observed.png
# http://localhost:8080/images/201/observed.png
# http://localhost:8080/images/219/observed.png

import logging
import os
import re

import nowcast


logging.getLogger().setLevel(logging.DEBUG)


request_path = os.environ["PATH_INFO"]
match = re.compile(r"/images/(\d+)/observed\.png").match(request_path)
area  = int(match.group(1))

time  = nowcast.get_current_observed_time()
image = nowcast.get_image(area, time, 0)

print "Content-Type: image/png"
print ""
print image
