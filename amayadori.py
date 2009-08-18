# -*- coding: utf-8 -*-

import logging
import datetime
from google.appengine.api import urlfetch

import cachemanager
import jmalib
import imglib
import timeutil
import png

CacheManager = cachemanager.CacheManager

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

def get_radar_time(current_time = get_current_time()):
  cached_time = CacheManager.get_radar_time(current_time)

  if cached_time == None:
    cached_time = CacheManager.create_radar_time(
      current_time = current_time,
      radar_time   = jmalib.get_current_radar_time(fetcher))

  return cached_time.radar_time

def get_nowcast_time(current_time = get_current_time()):
  cached_time = CacheManager.get_nowcast_time(current_time)

  if cached_time == None:
    cached_time = CacheManager.create_nowcast_time(
      current_time = current_time,
      nowcast_time = jmalib.get_current_nowcast_time(fetcher))

  return cached_time.nowcast_time

def get_image(area, time, ordinal):
  cached_image = CacheManager.get_image(area, time, ordinal)

  if cached_image == None:
    cached_image = CacheManager.create_image(
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

def get_time_table(current_time = get_current_time()):
  radar_time   = get_radar_time(current_time)
  nowcast_time = get_nowcast_time(current_time)

  table = [((radar_time, 0), radar_time)]

  for i in range(6):
    present_time = nowcast_time + datetime.timedelta(minutes = i * 10)
    if present_time > radar_time:
      table.append(((nowcast_time, i + 1), present_time))

  return table

def expire_cache():
  expire_time = get_current_time() - datetime.timedelta(minutes = 30)
  CacheManager.clear_radar_time(expire_time)
  CacheManager.clear_nowcast_time(expire_time)
  CacheManager.clear_image(expire_time)
  return None
