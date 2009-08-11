# -*- coding: utf-8 -*-

import os
import urllib2
import time

import jmalib



def fetch(url):
  print "fetch " + url
  req = urllib2.Request(url)
  io = urllib2.build_opener().open(req)
  data = io.read()
  io.close()
  return data

def create_path(area, time, ordinal):
  return "tmp/" + ("%03i" % area) + "-" + time.strftime("%Y%m%d%H%M") + "-" + ("%02i" % ordinal) + ".png"


radar_time   = jmalib.RadarNowCast.get_current_radar_time(fetch)
nowcast_time = jmalib.RadarNowCast.get_current_nowcast_time(fetch)
print radar_time
print nowcast_time

area_codes = [i + 201 for i in range(19)]
#area_codes = [201, 202]

for area in area_codes:
  #image_time    = radar_time
  image_time    = nowcast_time
  image_ordinal = 1
  path = create_path(area, image_time, image_ordinal)
  print path
  if not os.path.exists(path):
    image = jmalib.RadarNowCast.get_image(area, image_time, image_ordinal, fetch)
    outfile = open(path, "wb")
    outfile.write(image)
    outfile.close()
    time.sleep(1.0)
