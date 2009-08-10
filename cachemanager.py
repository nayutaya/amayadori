# -*- coding: utf-8 -*-

from google.appengine.ext import db


class RadarTime(db.Model):
  current_time = db.DateTimeProperty(required=True)
  radar_time   = db.DateTimeProperty(required=True)


class NowcastTime(db.Model):
  current_time = db.DateTimeProperty(required=True)
  nowcast_time = db.DateTimeProperty(required=True)


class CacheManager:
  def __init__(self):
    pass

  @classmethod
  def create_radar_time(cls, current_time, radar_time):
    record = RadarTime(
      current_time = current_time,
      radar_time   = radar_time)
    record.put()
    return record

  @classmethod
  def create_nowcast_time(cls, current_time, nowcast_time):
    record = NowcastTime(
      current_time = current_time,
      nowcast_time = nowcast_time)
    record.put()
    return record

  @classmethod
  def get_radar_time(cls, current_time):
    records = db.GqlQuery("SELECT * FROM RadarTime WHERE current_time = :1", current_time)
    if records.count() > 0:
      return records[0]
    else:
      return None

  @classmethod
  def get_nowcast_time(cls, current_time):
    records = db.GqlQuery("SELECT * FROM NowcastTime WHERE current_time = :1", current_time)
    if records.count() > 0:
      return records[0]
    else:
      return None
