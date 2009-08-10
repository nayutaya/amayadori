# -*- coding: utf-8 -*-

import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch

import model
import jmalib
import amayadori

def fetcher(url):
  logging.info("fetch " + url)
  result = urlfetch.fetch(url)
  if result.status_code == 200:
    return result.content
  else:
    # TODO: raise exception
    return None

def get_current_observed_time():
  return amayadori.get_radar_time()

def get_current_predictive_time():
  return amayadori.get_nowcast_time()

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
