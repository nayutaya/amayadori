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

def get_radar_time(current_time = None):
  current_time = current_time or get_current_time()

  cache_key  = "radar_time_" + current_time.strftime("%Y%m%d%H%M")
  radar_time = memcache.get(cache_key)

  if radar_time == None:
    radar_time = jmalib.get_current_radar_time(fetcher)
    memcache.add(cache_key, radar_time, 60)

  return radar_time

def get_nowcast_time(current_time = None):
  current_time = current_time or get_current_time()
  cached_time  = cachemanager.get_nowcast_time(current_time)

  if cached_time == None:
    cached_time = cachemanager.create_nowcast_time(
      current_time = current_time,
      nowcast_time = jmalib.get_current_nowcast_time(fetcher))

  return cached_time.nowcast_time

def get_image(area, time, ordinal):
  cached_image = cachemanager.get_image(area, time, ordinal)

  if cached_image == None:
    cached_image = cachemanager.create_image(
      area    = area,
      time    = time,
      ordinal = ordinal,
      image   = jmalib.get_image(area, time, ordinal, fetcher))

  return cached_image.image

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
