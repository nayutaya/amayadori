# -*- coding: utf-8 -*-

import datetime
import logging

import amayadori
import png
import areamanager
import radar

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
xy = (200,300)
area_code = 211

for (time, ordinal), present_time in table:
  image = amayadori.get_image(area_code, time, ordinal)
  rimage = radar.RadarImage.from_binary(image)
  rainfall = rimage.get_ballpark_rainfall(xy)
  print present_time, rainfall
