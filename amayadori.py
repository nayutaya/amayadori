# -*- coding: utf-8 -*-

import logging
import datetime
from google.appengine.api import urlfetch
from google.appengine.api import memcache

import cachemanager
import jmalib
import imglib
import timeutil
import png


def fetcher(url):
  logging.info("fetch " + url)
  result = urlfetch.fetch(url)
  if result.status_code == 200:
    return result.content
  else:
    # TODO: raise exception
    return None

def get_current_time():
  return timeutil.get_per_minute_time(timeutil.get_jst_now())

def cache(key, creator, time):
  value = memcache.get(key)
  if value is None:
    value = creator()
    memcache.add(key, value, time)
  return value

def get_radar_time(current_time = None):
  time = current_time or get_current_time()
  key  = "radar_time_" + time.strftime("%Y%m%d%H%M")
  proc = lambda: jmalib.get_current_radar_time(fetcher)
  return cache(key, proc, 120)

def get_nowcast_time(current_time = None):
  time = current_time or get_current_time()
  key  = "nowcast_time_" + time.strftime("%Y%m%d%H%M")
  proc = lambda: jmalib.get_current_nowcast_time(fetcher)
  return cache(key, proc, 120)

def get_image(area, time, ordinal):
  key = "image_%03i_%s_%02i" % (area, time.strftime("%Y%m%d%H%M"), ordinal)
  proc = lambda: jmalib.get_image(area, time, ordinal, fetcher)
  return cache(key, proc, 60 * 20)

def get_rainfall(image, cxy):
  cx, cy = cxy
  sx = max([0, cx - 2])
  sy = max([0, cy - 2])
  dx = 5
  dy = 5

  pngimg = png.Png8bitPalette.load(image)
  bitmap = imglib.RgbBitmap(dx, dy)
  for y in xrange(dy):
    for x in xrange(dx):
      rgb = pngimg.get_color((sx + x, sy + y))
      bitmap.set_pixel(x, y, rgb)

  return jmalib.get_rainfall_from_bitmap(bitmap)

def get_time_table(radar_time = None, nowcast_time = None):
  return jmalib.get_time_table(
    radar_time   = radar_time   or get_radar_time(),
    nowcast_time = nowcast_time or get_nowcast_time())

def expire_cache():
  expire_time = get_current_time() - datetime.timedelta(minutes = 30)
  cachemanager.clear_radar_time(expire_time)
  cachemanager.clear_nowcast_time(expire_time)
  cachemanager.clear_image(expire_time)
  return None
