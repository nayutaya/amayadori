# -*- coding: utf-8 -*-

import logging
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

def get_radar_time():
  current_time = timeutil.get_per_minute_time(timeutil.get_jst_now())
  cached_time  = CacheManager.get_radar_time(current_time)

  if cached_time == None:
    cached_time = CacheManager.create_radar_time(
      current_time = current_time,
      radar_time   = jmalib.RadarNowCast.get_current_radar_time(fetcher))

  return cached_time.radar_time

def get_nowcast_time():
  current_time = timeutil.get_per_minute_time(timeutil.get_jst_now())
  cached_time  = CacheManager.get_nowcast_time(current_time)

  if cached_time == None:
    cached_time = CacheManager.create_nowcast_time(
      current_time = current_time,
      nowcast_time = jmalib.RadarNowCast.get_current_nowcast_time(fetcher))

  return cached_time.nowcast_time
