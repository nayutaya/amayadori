# -*- coding: utf-8 -*-

from google.appengine.ext import db

class ObservedTimeCache(db.Model):
  current_time  = db.DateTimeProperty(required=True)
  observed_time = db.DateTimeProperty(required=True)

class PredictiveTimeCache(db.Model):
  current_time    = db.DateTimeProperty(required=True)
  predictive_time = db.DateTimeProperty(required=True)

class ImageCache(db.Model):
  area        = db.IntegerProperty(required=True)
  time        = db.DateTimeProperty(required=True)
  ordinal     = db.IntegerProperty(required=True)
  image       = db.BlobProperty(required=True)

class Task(db.Model):
  path = db.StringProperty(required=True)
  time = db.DateTimeProperty(required=True)
