# -*- coding: utf-8 -*-

from google.appengine.ext import db


class RadarTime(db.Model):
  current_time = db.DateTimeProperty(required=True)
  radar_time   = db.DateTimeProperty(required=True)


class NowcastTime(db.Model):
  current_time = db.DateTimeProperty(required=True)
  nowcast_time = db.DateTimeProperty(required=True)


class Image(db.Model):
  area    = db.IntegerProperty(required=True)
  time    = db.DateTimeProperty(required=True)
  ordinal = db.IntegerProperty(required=True)
  image   = db.BlobProperty(required=True)


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
  def create_image(cls, area, time, ordinal, image):
    record = Image(
      area    = area,
      time    = time,
      ordinal = ordinal,
      image   = db.Blob(image))
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

  @classmethod
  def get_image(cls, area, time, ordinal):
    records = db.GqlQuery("SELECT * FROM Image WHERE area = :1 AND time = :2 AND ordinal = :3", area, time, ordinal)
    if records.count() > 0:
      return records[0]
    else:
      return None

  @classmethod
  def clear_radar_time(cls, current_time):
    records = db.GqlQuery("SELECT * FROM RadarTime WHERE current_time <= :1", current_time)
    db.delete(records)
    return None

  @classmethod
  def clear_nowcast_time(cls, current_time):
    records = db.GqlQuery("SELECT * FROM NowcastTime WHERE current_time <= :1", current_time)
    db.delete(records)
    return None

  @classmethod
  def clear_image(cls, time):
    records = db.GqlQuery("SELECT * FROM Image WHERE time <= :1", time)
    db.delete(records)
    return None
