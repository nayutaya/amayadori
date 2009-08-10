# -*- coding: utf-8 -*-

import datetime
import re
import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch

import model
import jmalib
import timeutil


def fetcher(url):
  logging.info("fetch " + url)
  result = urlfetch.fetch(url)
  if result.status_code == 200:
    return result.content
  else:
    # TODO: raise exception
    return None

def get_current_observed_time():
  current_time = timeutil.get_per_minute_time(timeutil.get_jst_now())

  caches = db.GqlQuery("SELECT * FROM ObservedTimeCache WHERE current_time = :1", current_time)

  if caches.count() > 0:
    return caches[0].observed_time

  else:
    observed_time = jmalib.RadarNowCast.get_current_radar_time(fetcher)

    cache = model.ObservedTimeCache(
      current_time  = current_time,
      observed_time = observed_time)
    cache.put()

    return observed_time

def get_current_predictive_time():
  current_time = timeutil.get_per_minute_time(timeutil.get_jst_now())

  caches = db.GqlQuery("SELECT * FROM PredictiveTimeCache WHERE current_time = :1", current_time)

  if caches.count() > 0:
    return caches[0].predictive_time

  else:
    predictive_time = jmalib.RadarNowCast.get_current_nowcast_time(fetcher)

    cache = model.PredictiveTimeCache(
      current_time    = current_time,
      predictive_time = predictive_time)
    cache.put()

    return predictive_time

def get_image(area, time, ordinal):
  caches = db.GqlQuery("SELECT * FROM ImageCache WHERE area = :1 AND time = :2 AND ordinal = :3", area, time, ordinal)

  if caches.count() > 0:
    cache = caches[0]
  else:
    image = jmalib.RadarNowCast.get_image(area, time, ordinal, fetcher)

    cache = model.ImageCache(
      area        = area,
      time        = time,
      ordinal     = ordinal,
      image       = db.Blob(image))
    cache.put()

  return cache.image
