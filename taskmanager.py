# -*- coding: utf-8 -*-

import datetime
import logging
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue


class Task(db.Model):
  path = db.StringProperty(required=True)
  time = db.DateTimeProperty(required=True)


class TaskTracker:
  def __init__(self, path):
    self.path      = path
    self.completed = False

  def is_completed(self):
    if not self.completed:
      records = db.GqlQuery("SELECT * FROM Task WHERE path = :1", self.path)
      self.completed = (records.count() == 0)
    return self.completed

  def clear(self):
    records = db.GqlQuery("SELECT * FROM Task WHERE path = :1", self.path)
    db.delete(records)


def create_cache_fetch_task_path(area, time, ordinal):
  url  = "/task/cache/fetch"
  url += "/" + ("%03i" % area)
  url += "/" + time.strftime("%Y%m%d%H%M")
  url += "/" + ("%02i" % ordinal)
  return url

def add_cache_fetch_task(area, time, ordinal):
  path = create_cache_fetch_task_path(area, time, ordinal)
  logging.info("add task " + path)

  task = Task(path = path, time = datetime.datetime.now())
  task.put()

  taskqueue.add(url=path, params={})

  return TaskTracker(path = path)
