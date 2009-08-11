# -*- coding: utf-8 -*-

import logging
import datetime
from google.appengine.api import urlfetch

import cachemanager
import jmalib
import timeutil

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

def get_radar_time():
  current_time = get_current_time()
  cached_time  = CacheManager.get_radar_time(current_time)

  if cached_time == None:
    cached_time = CacheManager.create_radar_time(
      current_time = current_time,
      radar_time   = jmalib.RadarNowCast.get_current_radar_time(fetcher))

  return cached_time.radar_time

def get_nowcast_time():
  current_time = get_current_time()
  cached_time  = CacheManager.get_nowcast_time(current_time)

  if cached_time == None:
    cached_time = CacheManager.create_nowcast_time(
      current_time = current_time,
      nowcast_time = jmalib.RadarNowCast.get_current_nowcast_time(fetcher))

  return cached_time.nowcast_time

def get_image(area, time, ordinal):
  cached_image = CacheManager.get_image(area, time, ordinal)

  if cached_image == None:
    cached_image = CacheManager.create_image(
      area    = area,
      time    = time,
      ordinal = ordinal,
      image   = jmalib.RadarNowCast.get_image(area, time, ordinal, fetcher))

  return cached_image.image

def get_time_table():
  radar_time   = get_radar_time()
  nowcast_time = get_nowcast_time()

  table = [((radar_time, 0), radar_time)]

  for i in range(6):
    present_time = nowcast_time + datetime.timedelta(minutes = i * 10)
    if present_time > radar_time:
      table.append(((nowcast_time, i + 1), present_time))

  return table
