# -*- coding: utf-8 -*-

import datetime
import logging

import amayadori
import areamanager

logging.getLogger().setLevel(logging.DEBUG)


print "Content-Type: text/plain"
print ""


current_time = amayadori.get_current_time()
radar_time   = amayadori.get_radar_time()
nowcast_time = amayadori.get_nowcast_time()
print current_time
print radar_time
print nowcast_time

table = amayadori.get_time_table()
for x in table: print x


#lnglat = (35.0, 135.0)
xy = (182,200)
area = 201

for (time, ordinal), present_time in table:
  image    = amayadori.get_image(area, time, ordinal)
  x, y = xy
  rainfall = amayadori.get_rainfall(image, x, y)

  print (time, ordinal, present_time, rainfall)
