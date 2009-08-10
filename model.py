# -*- coding: utf-8 -*-

from google.appengine.ext import db

class ImageCache(db.Model):
  area        = db.IntegerProperty(required=True)
  time        = db.DateTimeProperty(required=True)
  ordinal     = db.IntegerProperty(required=True)
  image       = db.BlobProperty(required=True)

class Task(db.Model):
  path = db.StringProperty(required=True)
  time = db.DateTimeProperty(required=True)
