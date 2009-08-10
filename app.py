# -*- coding: utf-8 -*-

import datetime
import logging

import nowcast
import png
import areamanager
import radar

logging.getLogger().setLevel(logging.DEBUG)


print "Content-Type: text/plain"
print ""






observed_time = nowcast.get_current_observed_time()
print observed_time
predictive_time = nowcast.get_current_predictive_time()
print predictive_time

list = []
list.append(((observed_time, 0), observed_time))
for i in range(6):
  time = predictive_time + datetime.timedelta(minutes = i * 10)
  if time > observed_time:
    list.append(((predictive_time, i + 1), time))
    print time - observed_time

for x in list: print x

#lnglat = (35.0, 135.0)
xy = (200,300)
area_code = 211

for (image_time, image_ordinal), time in list:
  image = nowcast.get_image(area_code, image_time, image_ordinal)
  rimage = radar.RadarImage.from_binary(image)
  rainfall = rimage.get_ballpark_rainfall(xy)

  print time, rainfall
