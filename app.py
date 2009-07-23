# -*- coding: utf-8 -*-

import datetime
import logging
import StringIO
import struct
import binascii
import zlib

import nowcast
import png




#print get_current_observed_time()
#print get_current_predictive_time()
#print create_image_url(211, datetime.datetime.now(), 0)
#print create_image_url(211, datetime.datetime.now(), 1)

#print "Content-Type: image/png"
#print ""
#time = get_current_observed_time()
#print get_image(211, time, 0)
#time = get_current_predictive_time()
#print get_image(211, time, 1)

print "Content-Type: text/plain"
print ""


time  = nowcast.get_current_observed_time()
image = nowcast.get_image(211, time, 0)

png = png.Png8bitPalette.load(image)
print png
#for line in png.bitmap.bitmap:
#  print ",".join(["%02X" % x for x in line])
