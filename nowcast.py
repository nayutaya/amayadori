# -*- coding: utf-8 -*-

import datetime
import re
import logging
from google.appengine.ext import db
from google.appengine.api import urlfetch

import model


def get_jst_now():
  return datetime.datetime.utcnow() + datetime.timedelta(hours = 9)

def get_per_minute_time(time):
  return datetime.datetime(time.year, time.month, time.day, time.hour, time.minute)

def get_current_observed_time():
  current_time = get_per_minute_time(get_jst_now())
  logging.info("current time: %s", current_time)

  caches = db.GqlQuery("SELECT * FROM ObservedTimeCache WHERE current_time = :1", current_time)

  if caches.count() > 0:
    logging.info("cache hit")

    return caches[0].observed_time

  else:
    logging.info("cache miss")

    result = urlfetch.fetch("http://www.jma.go.jp/jp/radnowc/hisjs/radar.js")
    if result.status_code == 200:
      list = re.compile(r"\d{12}-\d{2}\.png").findall(result.content)
      list.sort()

      match = re.compile(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})").match(list[-1])
      # TODO: if not match, raise exception

      observed_time = datetime.datetime(
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)),
        int(match.group(5)))

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
  logging.info("current time: %s", current_time)

  caches = db.GqlQuery("SELECT * FROM PredictiveTimeCache WHERE current_time = :1", current_time)

  if caches.count() > 0:
    logging.info("cache hit")

    return caches[0].predictive_time

  else:
    logging.info("cache miss")

    result = urlfetch.fetch("http://www.jma.go.jp/jp/radnowc/hisjs/nowcast.js")
    if result.status_code == 200:
      list = re.compile(r"\d{12}-\d{2}\.png").findall(result.content)
      list.sort()

      match = re.compile(r"(\d{4})(\d{2})(\d{2})(\d{2})(\d{2})").match(list[-1])
      # TODO: if not match, raise exception

      predictive_time = datetime.datetime(
        int(match.group(1)),
        int(match.group(2)),
        int(match.group(3)),
        int(match.group(4)),
        int(match.group(5)))

      cache = model.PredictiveTimeCache(
        current_time    = current_time,
        predictive_time = predictive_time,
        expire_time     = current_time + datetime.timedelta(minutes = 20))
      cache.put()

      return predictive_time
    #else:
      # TODO: raise exception

def create_observed_image_url(area, time):
  url  = "http://www.jma.go.jp/jp/radnowc/imgs/radar/"
  url += ("%03i" % area)
  url += "/"
  url += time.strftime("%Y%m%d%H%M")
  url += "-00.png"
  return url

def create_predictive_image_url(area, time, no):
  url = "http://www.jma.go.jp/jp/radnowc/imgs/nowcast/"
  url += ("%03i" % area)
  url += "/"
  url += time.strftime("%Y%m%d%H%M")
  url += "-"
  url += ("%02i" % no)
  url += ".png"
  return url

def create_image_url(area, time, no):
  if no == 0:
    return create_observed_image_url(area, time)
  else:
    return create_predictive_image_url(area, time, no)

def get_image(area, time, ordinal):
  logging.info("get_image")

  caches = db.GqlQuery("SELECT * FROM ImageCache WHERE area = :1 AND time = :2 AND ordinal = :3", area, time, ordinal)

  if caches.count() > 0:
    logging.info("cache hit")
    cache = caches[0]
  else:
    logging.info("cache miss")
    url = create_image_url(area, time, ordinal)
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
