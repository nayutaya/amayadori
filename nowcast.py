# -*- coding: utf-8 -*-

import datetime
import re
import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch

import model
import jmalib


def get_jst_now():
  return datetime.datetime.utcnow() + datetime.timedelta(hours = 9)

def get_per_minute_time(time):
  return datetime.datetime(time.year, time.month, time.day, time.hour, time.minute)

def get_current_observed_time():
  current_time = get_per_minute_time(get_jst_now())

  caches = db.GqlQuery("SELECT * FROM ObservedTimeCache WHERE current_time = :1", current_time)

  if caches.count() > 0:
    return caches[0].observed_time

  else:
    url = "http://www.jma.go.jp/jp/radnowc/hisjs/radar.js"
    logging.info("fetch " + url)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      parsed_data   = jmalib.RadarNowCast.parse_radar_js(result.content)
      observed_time = jmalib.RadarNowCast.get_latest_time(parsed_data)

      cache = model.ObservedTimeCache(
        current_time  = current_time,
        observed_time = observed_time,
        expire_time   = current_time + datetime.timedelta(minutes = 20))
      cache.put()

      return observed_time
    #else:
      # TODO: raise exception

def get_current_predictive_time():
  current_time = get_per_minute_time(get_jst_now())

  caches = db.GqlQuery("SELECT * FROM PredictiveTimeCache WHERE current_time = :1", current_time)

  if caches.count() > 0:
    return caches[0].predictive_time

  else:
    url = "http://www.jma.go.jp/jp/radnowc/hisjs/nowcast.js"
    logging.info("fetch " + url)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      parsed_data     = jmalib.RadarNowCast.parse_nowcast_js(result.content)
      predictive_time = jmalib.RadarNowCast.get_latest_time(parsed_data)

      cache = model.PredictiveTimeCache(
        current_time    = current_time,
        predictive_time = predictive_time,
        expire_time     = current_time + datetime.timedelta(minutes = 20))
      cache.put()

      return predictive_time
    #else:
      # TODO: raise exception

def create_image_url(area, time, no):
  return jmalib.RadarNowCast.create_image_url(area, time, no)

def get_image(area, time, ordinal):
  caches = db.GqlQuery("SELECT * FROM ImageCache WHERE area = :1 AND time = :2 AND ordinal = :3", area, time, ordinal)

  if caches.count() > 0:
    cache = caches[0]
  else:
    url = create_image_url(area, time, ordinal)
    logging.info("fetch " + url)
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      cache = model.ImageCache(
        area        = area,
        time        = time,
        ordinal     = ordinal,
        image       = db.Blob(result.content),
        expire_time = get_jst_now() + datetime.timedelta(minutes = 20))
      cache.put()
    #else:

  return cache.image
