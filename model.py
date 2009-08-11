# -*- coding: utf-8 -*-

from google.appengine.ext import db

class Task(db.Model):
  path = db.StringProperty(required=True)
  time = db.DateTimeProperty(required=True)
